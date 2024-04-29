"""Byteclass collection internals."""

import inspect
import sys
from abc import update_abstractmethods
from collections.abc import Callable
from copy import deepcopy
from typing import Any, cast

from ..._enums import ByteOrder
from ...constants import _BYTECLASS, _MEMBERS, _PARAMS
from ...util import is_byteclass_collection, is_byteclass_collection_instance
from ._collection_class_spec import _CollectionClassSpec
from ._methods import (
    _build_attach_members_method,
    _build_attach_method,
    _build_bytes_method,
    _build_cmp_method,
    _build_data_property,
    _build_delattr_method,
    _build_getitem_method,
    _build_hash_method,
    _build_len_method,
    _build_repr_method,
    _build_setattr_method,
    _build_setitem_method,
    _build_str_method,
    _raise_hash_exception,
)
from ._params import _Params
from ._util import _set_new_attribute, _set_qualname, _tuple_str
from .byteclass_collection_protocol import ByteclassCollection, ByteclassCollectionError
from .member import _MEMBER, _SUPPORTED_MBR_TYPES, MISSING, Member, _get_member, _MissingType

__all__ = [
    "ByteclassCollectionError",
    "members",
    "collection_as_dict",
    "collection_as_tuple",
    "create_collection",
    "is_byteclass_collection",
    "ByteclassCollection",
]


def create_collection(
    cls: type | None,
    collection_type: str,
    byte_order: bytes | ByteOrder,
    packed: bool,
    methods: dict[str, Callable],
    allowed_types: tuple[type, ...] | None = None,
) -> ByteclassCollection | Callable[[type], ByteclassCollection]:
    """Create custom collection class."""
    byte_order = ByteOrder(byte_order)

    def outer_wrapper(cls: type) -> ByteclassCollection:
        spec = _CollectionClassSpec(
            base_cls=cls,
            collection_type=collection_type,
            byte_order=ByteOrder(byte_order),
            packed=packed,
            methods=methods,
        )
        if allowed_types:
            spec.allowed_types = allowed_types
        new_cls: ByteclassCollection = _process_class(spec)
        return cast(ByteclassCollection, new_cls)

    # See if we're being called as @structure or @structure().
    if cls is None:
        return outer_wrapper  # We're called with parens.
    return outer_wrapper(cls)  # We're called as @structure without parens.


# _fixed_collection_getstate and _fixed_collection_setstate are needed for pickling classes with slots.
# These could be slighly more performant if we generated the code instead of iterating
# over members.
def _fixed_collection_getstate(self):
    """Return the state of a fixed collection instance."""
    return [getattr(self, member_.name) for member_ in members(self)]


def _fixed_collection_setstate(self, state):
    """Set the state of a fixed collection instance."""
    for member_, value in zip(members(self), state):
        object.__setattr__(self, member_.name, value)


def _add_slots(spec: _CollectionClassSpec):
    """Add __slots__ to class.

    Must create a new class, can't set __slots__ after a class has been created.
    """
    # Make sure __slots__ isn't already set.
    if "__slots__" in spec.base_cls.__dict__:
        raise TypeError(f"{spec.base_cls.__name__} already specifies __slots__")

    # Create a new dict for our new class.
    fixed_attributes = tuple(spec.attributes)
    cls_dict = dict(spec.base_cls.__dict__)
    cls_dict["__slots__"] = fixed_attributes
    for item in fixed_attributes:
        # Remove our attributes, if present. They'll still be
        #  available in _MARKER.
        cls_dict.pop(item, None)

    # Remove __dict__ itself.
    cls_dict.pop("__dict__", None)

    # And finally create the class.
    qualname = getattr(spec.base_cls, "__qualname__", None)
    spec.base_cls = type(spec.base_cls)(spec.base_cls.__name__, spec.base_cls.__bases__, cls_dict)
    if qualname is not None:
        spec.base_cls.__qualname__ = qualname

    spec.base_cls.__getstate__ = _fixed_collection_getstate  # type: ignore
    spec.base_cls.__setstate__ = _fixed_collection_setstate  # type: ignore


def _process_class(spec: _CollectionClassSpec) -> ByteclassCollection:
    """Process a normal class and turn it into a fixed size collection.

    Now that dicts retain insertion order, there's no reason to use an ordered dict.
    I am leveraging that ordering here, because derived class fields overwrite base
    class fields, but the order is defined by the base class, which is found first.
    collection_type is a string name of the collection type,
    e.g. "structure", "union", "bitfield"
    """
    members_: dict[str, Member] = {}

    if spec.base_cls.__module__ in sys.modules:
        globals_: dict[str, Any] = sys.modules[spec.base_cls.__module__].__dict__
    else:
        # Theoretically this can happen if someone writes
        # a custom string to cls.__module__.  In which case
        # such dataclass won't be fully introspectable
        # (w.r.t. typing.get_type_hints) but will still function
        # correctly.
        globals_ = {}
    setattr(spec.base_cls, _BYTECLASS, True)
    setattr(
        spec.base_cls,
        _PARAMS,
        _Params(spec),
    )
    spec.attributes.extend(["offset", "byte_order", "_length", "_data"])
    # Find our base classes in reverse MRO order, and exclude
    # ourselves.  In reversed order so that more derived classes
    # override earlier member definitions in base classes.
    for base in spec.base_cls.__mro__[-1:0:-1]:
        # Only process classes that have been processed by our
        # decorator.  That is, they have a _MEMBERS attribute.
        base_members = getattr(base, _MEMBERS, None)

        # If the base class has no members, then it's not a fixed size collection.
        if base_members is not None:
            base_params = getattr(base, _PARAMS, None)

            # If the base class has members but no params, then it malformed.
            if base_params is None:
                raise TypeError(f"{base.__name__} is malformed fixed collection class")

            # Check to ensure the base class is of the same fixed collection type.
            if base_params.type != spec.collection_type:
                raise TypeError(
                    f"{spec.collection_type} type fixed collection cannot inherit " f"from {base_params.type} type"
                )
            for member_ in base_members.values():
                members_[member_.name] = member_

    _add_members(spec, members_)
    spec.self_name = "__collection_self__" if "self" in [member_.name for member_ in spec.members] else "self"
    required_attributes: list[str] = []
    # Verify that the calling constructor provided all required attributes.
    if not all(name in spec.methods.keys() for name in required_attributes):
        raise TypeError(
            f"{spec.collection_type} constructor did not provide all required attributes: " f"{required_attributes}"
        )
    # Construct and attach fixed collection type specific methods to the class.
    _add_methods(spec, globals_)
    if not getattr(spec.base_cls, "__doc__"):
        # Create a class doc-string.
        spec.base_cls.__doc__ = spec.base_cls.__name__ + str(inspect.signature(spec.base_cls)).replace(" -> None", "")

    # Include regular fields (so, not ClassVars).
    init_members = [member_ for member_ in members_.values() if member_.member_type is _MEMBER]

    # Add __match_args__ attribute
    _set_new_attribute(spec.base_cls, "__match_args__", tuple(member_.name for member_ in init_members))

    # Set up collection slots
    member_names = tuple(member_.name for member_ in members(spec.base_cls))
    spec.attributes.extend(member_names)
    _add_slots(spec)

    update_abstractmethods(spec.base_cls)  # Python >3.11

    return cast(ByteclassCollection, spec.base_cls)


def _add_members(spec: _CollectionClassSpec, members_: dict[str, Member]) -> None:
    """Add collection members to class."""
    # Annotations that are defined in this class (not in base classes).
    # If __annotations__ isn't present, then this class adds no new annotations.
    # We use this to compute members that are added by this class.
    #
    # Members are found from cls_annotations, which is guaranteed to be ordered.
    # Default values are from class attributes, if a member has a default.  Defaults
    # are only allowed if it is a Member(), then it contains additional info beyond (and
    # possibly including) the factory.  Pseudo-fields like ClassVars and InitVars are
    # not supported at this time.
    cls_annotations = spec.base_cls.__dict__.get("__annotations__", {})

    # Now find members in our class.  While doing so, perform validations and set
    # the default values (as class attributes) where we can.
    cls_members: list[Member] = []
    for name, member_type in cls_annotations.items():
        cls_members.append(_get_member(spec.base_cls, name, member_type))

    for member_ in cls_members:
        if member_.name is None:
            raise ValueError("Member name cannot be None")
        members_[member_.name] = member_
        # If the class attribute (which is the default value for this member) exists
        # and is of type 'Member', replace it with the real default.  This is so that
        # normal class introspection sees a real default value, not a Member.
        try:
            if not isinstance(getattr(spec.base_cls, member_.name), Member):
                raise ValueError("Member's cannot have default values.")
        except AttributeError:
            # Allow missing members to use type annotation as default factory.
            pass
    # Do we have any Members that don't also have annotations?
    for name, value in spec.base_cls.__dict__.items():
        if isinstance(value, Member) and name not in cls_annotations:
            raise TypeError(f"{name!r} is a member but has no type annotation")

    # Remember all of the members on our class (including bases).  This
    # also marks this class as being a fixed collection.
    setattr(spec.base_cls, _MEMBERS, members_)

    # Get the members as a list, and include only real fields.  This is
    # used in all of the following methods.
    member_list: list[Member] = [member_ for member_ in members_.values() if member_.member_type is _MEMBER]
    if not member_list:
        raise ValueError("Collection class must contain at least one member.")
    for member_ in member_list:
        if not member_.type:
            raise TypeError(f"Member {member_.name} type not set")
        if spec.allowed_types:
            if not issubclass(member_.type, spec.allowed_types):
                raise TypeError(f"{member_.name} ({member_.type}) is not a supported member type.")
        else:
            if not (is_byteclass_collection(member_.type) or issubclass(member_.type, _SUPPORTED_MBR_TYPES)):
                raise TypeError(f"{member_.name} ({member_.type}) is not a supported member type.")
    spec.members = member_list


def _add_methods(spec: _CollectionClassSpec, globals_: dict[str, Any]):
    """Add methods to collection class."""
    class_hash = spec.base_cls.__dict__.get("__hash__", MISSING)
    has_explicit_hash = not (class_hash is MISSING or (class_hash is None and "__eq__" in spec.base_cls.__dict__))
    if has_explicit_hash:
        build_hash_method_: Callable = _raise_hash_exception
    else:
        build_hash_method_ = _build_hash_method

    methods: dict[str, Callable | None] = {
        "data": _build_data_property,
        "__bytes__": _build_bytes_method,
        "__hash__": build_hash_method_,
        "__len__": _build_len_method,
        "__str__": _build_str_method,
        "__repr__": _build_repr_method,
        "__getitem__": _build_getitem_method,
        "__setitem__": _build_setitem_method,
        "__delattr__": _build_delattr_method,
        "__setattr__": _build_setattr_method,  # Restrict the class attributes
        "attach": _build_attach_method,
        "_attach_members": _build_attach_members_method,
    }
    methods.update(spec.methods)
    for method_name, func_constructor in methods.items():
        if func_constructor:
            method = _set_qualname(spec.base_cls, func_constructor(spec, globals_))
            setattr(spec.base_cls, method_name, method)

    # Create __eq__ method.  There's no need for a __ne__ method,
    # since python will call __eq__ and negate it.
    self_tuple = _tuple_str(spec.self_name, spec.members)
    other_tuple = _tuple_str("other", spec.members)
    _set_new_attribute(
        spec.base_cls,
        "__eq__",
        _build_cmp_method(spec, "__eq__", "==", self_tuple, other_tuple, globals_=globals_),
    )

    # Create and set the ordering methods.
    self_tuple = _tuple_str(spec.self_name, spec.members)
    other_tuple = _tuple_str("other", spec.members)
    for name, operation in [
        ("__lt__", "<"),
        ("__le__", "<="),
        ("__gt__", ">"),
        ("__ge__", ">="),
    ]:
        if _set_new_attribute(
            spec.base_cls,
            name,
            _build_cmp_method(spec, name, operation, self_tuple, other_tuple, globals_=globals_),
        ):
            raise TypeError(
                f"Cannot overwrite attribute {name} "
                f"in class {spec.base_cls.__name__}. Consider using "
                "functools.total_ordering"
            )


def _get_members(cls) -> list[Member]:
    """Get the members for the class."""
    members_: dict[str, Member] | _MissingType = getattr(cls, _MEMBERS, MISSING)
    if isinstance(members_, _MissingType):
        return []
    return [member_ for member_ in members_.values() if member_.member_type == "_MEMBER"]


def _get_params(cls):
    """Get the parameters for the class."""
    return getattr(cls, _PARAMS, MISSING)


def _set_params(spec: _CollectionClassSpec):
    """Set the parameters for the class."""
    setattr(
        spec.base_cls,
        _PARAMS,
        _Params(spec),
    )


def members(class_or_instance):
    """Return a tuple describing the members of this dataclass.

    Accepts a fixed collection or an instance of one. Tuple elements are of
    type Member.

    Might it be worth caching this, per class?
    """
    try:
        members_ = getattr(class_or_instance, _MEMBERS)
    except AttributeError as err:
        raise TypeError("must be called with a fixed collection type or instance") from err

    # Exclude pseudo-fields.  Note that fields is sorted by insertion
    # order, so the order of the tuple is as the fields were defined.
    return tuple(member_ for member_ in members_.values() if member_.member_type is _MEMBER)


def collection_as_dict(obj, *, dict_factory=dict):
    """Return fixed collection instance members as a dict mapping.

    Example usage:

      @structure|@union|@bitfield
      class C:
          x: int
          y: int

      c = C(1, 2)
      assert as_dict(c) == {'x': 1, 'y': 2}

    If given, 'dict_factory' will be used instead of built-in dict.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    if not is_byteclass_collection_instance(obj):
        raise TypeError("as_dict() should be called on fixed collection instances")
    return _as_dict_inner(obj, dict_factory)


def _as_dict_inner(obj, dict_factory):
    if is_byteclass_collection_instance(obj):
        result = []
        for member_ in members(obj):
            value = _as_dict_inner(getattr(obj, member_.name), dict_factory)
            result.append((member_.name, value))
        return dict_factory(result)
    if isinstance(obj, tuple) and hasattr(obj, "_members"):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_as_dict_inner(v, dict_factory) for v in obj])
    if isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_as_dict_inner(v, dict_factory) for v in obj)
    if isinstance(obj, dict):
        return type(obj)((_as_dict_inner(k, dict_factory), _as_dict_inner(v, dict_factory)) for k, v in obj.items())
    return deepcopy(obj)


def collection_as_tuple(obj, *, tuple_factory=tuple):
    """Return the members of a fixed collection instance as a tuple of member values.

    Example usage::

      @structure|@union|@bitfield
      class C:
          x: int
          y: int

    c = C(1, 2)
    assert astuple(c) == (1, 2)

    If given, 'tuple_factory' will be used instead of built-in tuple.
    The function applies recursively to member values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    if not is_byteclass_collection_instance(obj):
        raise TypeError("astuple() should be called on fixed collection instances")
    return _as_tuple_inner(obj, tuple_factory)


def _as_tuple_inner(obj, tuple_factory):
    if is_byteclass_collection_instance(obj):
        result = []
        for member_ in members(obj):
            value = _as_tuple_inner(getattr(obj, member_.name), tuple_factory)
            result.append(value)
        return tuple_factory(result)
    if isinstance(obj, tuple) and hasattr(obj, "_members"):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).
        return type(obj)(*[_as_tuple_inner(v, tuple_factory) for v in obj])
    if isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_as_tuple_inner(v, tuple_factory) for v in obj)
    if isinstance(obj, dict):
        return type(obj)(
            (
                _as_tuple_inner(k, tuple_factory),
                _as_tuple_inner(v, tuple_factory),
            )
            for k, v in obj.items()
        )
    return deepcopy(obj)
