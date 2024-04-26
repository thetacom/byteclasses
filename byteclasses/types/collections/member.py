"""Member class for fixed size collections."""

import re
import sys
from collections.abc import Callable
from types import GenericAlias, MappingProxyType, MemberDescriptorType
from typing import TYPE_CHECKING, Any, TypeVar, overload

from ..._enums import ByteOrder
from ...types._fixed_size_type import _FixedSizeType
from ...util import is_byteclass_collection

if TYPE_CHECKING:
    from ._collection_class_spec import _CollectionClassSpec

# Since most per-field metadata will be unused, create an empty
# read-only proxy that can be shared among all fields.
_EMPTY_METADATA: Any = MappingProxyType({})


class _MemberBase:  # pylint: disable=R0903
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


# String regex that string annotations for ClassVar or InitVar must match.
# Allows "identifier.identifier[" or "identifier[".
# https://bugs.python.org/issue33453 for details.
_MODULE_IDENTIFIER_RE = re.compile(r"^(?:\s*(\w+)\s*\.)?\s*(\w+)")

_MEMBER = _MemberBase("_MEMBER")
_MEMBER_CLASSVAR = _MemberBase("_MEMBER_CLASSVAR")


class _MissingType:  # pylint: disable=R0903
    """A sentinel object to detect if a parameter is supplied or not.

    Use a class to give it a better repr.
    """


MISSING = _MissingType()

MbrT = TypeVar("MbrT")


class Member:  # pylint: disable=R0903
    """A member of a fixed size collection.

    Instances of Member are only ever created from within this module,
    and only from the member() function, although Member instances are
    exposed externally as (conceptually) read-only objects.

    name and type are filled in after the fact, not in __init__.
    They're not known at the time this class is instantiated, but it's
    convenient if they're available later.

    When cls._MEMBERS is filled in with a list of Member objects, the name
    and type fields will have been populated.
    """

    __slots__ = (
        "name",
        "type",
        "factory",
        "metadata",
        "member_type",  # Private: not to be used by user code.
    )

    def __init__(
        self,
        factory,
        metadata,
    ):
        """Initialize a Member object."""
        self.name: str | None = None
        self.type: type | None = None
        self.factory: Callable[[bytes, ByteOrder], Any] = factory
        self.metadata = _EMPTY_METADATA if metadata is None else MappingProxyType(metadata)
        self.member_type: _MemberBase | None = None

    def __repr__(self):
        """Return a repr string for this Member."""
        return (
            "Field("
            f"{self.name=!r},"
            f"{self.type=!r},"
            f"{self.factory=!r},"
            f"{self.metadata=!r},"
            f"{self.member_type=}"
            ")"
        )

    def __set_name__(self, owner, name):
        """Set the name of this member.

        This is used to support the PEP 487 __set_name__ protocol in the
        case where we're using a member that contains a descriptor as a
        default value.  For details on __set_name__, see
        https://www.python.org/dev/peps/pep-0487/#implementation-details.

        Note that in _process_class, this Member object is overwritten
        with the default value, so the end result is a descriptor that
        had __set_name__ called on it at the right time.
        """
        func = getattr(self.type, "__set_name__", None)
        if func and isinstance(func, Callable):
            # There is a __set_name__ method on the descriptor, call it.
            func(None, owner, name)  # pylint: disable=E1102

    __class_getitem__ = classmethod(GenericAlias)  # type: ignore


@overload
def member(*, factory: Callable[[Any], MbrT], metadata=None) -> MbrT: ...


@overload
def member(*, factory: Callable[[bytes | ByteOrder], _FixedSizeType], metadata=None) -> _FixedSizeType: ...


@overload
def member(*, factory: _MissingType = MISSING, metadata=None) -> Member: ...


# This function is used instead of exposing Member creation directly,
# so that a type checker can be told (via overloads) that this is a
# function whose type depends on its parameters.
def member(
    *,
    factory=MISSING,
    metadata=None,
) -> Any:
    """Return an object to identify dataclass fields.

    Unlike dataclasses, byteclasses do not accept `default` values.  `factory` is a
    0-argument function called to initialize a member. metadata, if specified,
    must be a mapping which is stored but not otherwise examined by the fixed
    collection.
    """
    return Member(factory, metadata)


def _member_assign(name: str, value: Any, self_name: str) -> str:
    # self_name is what "self" is called in this function: don't
    # hard-code "self", since that might be a field name.
    return f"BUILTINS.object.__setattr__({self_name},{name!r},{value})"


def _init_members(spec: "_CollectionClassSpec", globals_: dict[str, Any]) -> list[str]:
    """Initialize all class members."""
    body: list[str] = []
    for member_ in spec.members:
        init_line = _init_member(spec, member_, globals_, spec.self_name)
        body.extend(
            [
                init_line,
                "try:",
                f"  {spec.self_name}.{member_.name}.byte_order = {spec.byte_order.value!r}",
                "except AttributeError:",
                "  pass",
            ]
        )
    return body


def _init_member(
    spec: "_CollectionClassSpec",
    member_: Member,
    globals_: dict[str, Any],
    self_name: str,
) -> str:
    # Return the text of the line in the body of __init__ that will
    # initialize this field.

    init_name = f"_init_{member_.name}"
    if member_.factory is not MISSING:
        globals_[init_name] = member_.factory
    else:
        # No factory. Use member type as constructor.
        globals_[init_name] = member_.type
    value = f"{init_name}(byte_order={spec.byte_order})"
    if member_.name is None:
        raise ValueError("Member name cannot be None.")
    # Now, actually generate the member assignment.
    return _member_assign(member_.name, value, self_name)


def _is_type(
    annotation: str,
    cls: type,
    a_module,
    a_type: type,
    is_type_predicate: Callable,
):
    # Given a type annotation string, does it refer to a_type in
    # a_module?  For example, when checking that annotation denotes a
    # ClassVar, then a_module is typing, and a_type is
    # typing.ClassVar.

    # It's possible to look up a_module given a_type, but it involves
    # looking in sys.modules (again!), and seems like a waste since
    # the caller already knows a_module.

    # - annotation is a string type annotation
    # - cls is the class that this annotation was found in
    # - a_module is the module we want to match
    # - a_type is the type in that module we want to match
    # - is_type_predicate is a function called with (obj, a_module)
    #   that determines if obj is of the desired type.

    # Since this test does not do a local namespace lookup (and
    # instead only a module (global) lookup), there are some things it
    # gets wrong.

    # With string annotations, cv0 will be detected as a ClassVar:
    #   CV = ClassVar
    #   @structure|@union|@bitfield
    #   class C0:
    #     cv0: CV

    # But in this example cv1 will not be detected as a ClassVar:
    #   @structure|@union|@bitfield
    #   class C1:
    #     CV = ClassVar
    #     cv1: CV

    # In C1, the code in this function (_is_type) will look up "CV" in
    # the module and not find it, so it will not consider cv1 as a
    # ClassVar.  This is a fairly obscure corner case, and the best
    # way to fix it would be to eval() the string "CV" with the
    # correct global and local namespaces.  However that would involve
    # a eval() penalty for every single field of every dataclass
    # that's defined.  It was judged not worth it.

    match = _MODULE_IDENTIFIER_RE.match(annotation)
    if match:
        namespace = None
        module_name = match.group(1)
        if not module_name:
            # No module name, assume the class's module did
            # "from dataclasses import InitVar".
            namespace = sys.modules.get(cls.__module__).__dict__
        else:
            # Look up module_name in the class's module.
            module = sys.modules.get(cls.__module__)
            if module and module.__dict__.get(module_name) is a_module:
                namespace = sys.modules.get(a_type.__module__).__dict__
        if namespace and is_type_predicate(namespace.get(match.group(2)), a_module):
            return True
    return False


def _get_member(cls: type, a_name: str, a_type: type):
    """Return a Member object for this member name and type.

    ClassVars are also returned, but marked as such (see f._field_type). If the default
    value isn't derived from Member, then it's only a normal default value. Convert it
    to a Member().
    """
    default = getattr(cls, a_name, MISSING)

    if isinstance(default, Member):
        member_ = default
    elif default != MISSING:
        raise ValueError("Collection member cannot have a default value.")
    elif isinstance(default, MemberDescriptorType):
        # This is a member in __slots__, so it has no default value.
        pass
        # default = MISSING
    else:
        member_ = member()

    # Only at this point do we know the name and the type.  Set them.
    member_.name = a_name
    member_.type = a_type

    # Assume it's a normal member until proven otherwise.  We're next
    # going to decide if it's a ClassVar, everything else is just a normal member.
    member_.member_type = _MEMBER

    # Validations for individual fields.  This is delayed until now,
    # instead of in the Field() constructor, since only here do we
    # know the field name, which allows for better error reporting.

    # For real members, disallow any non fixed types
    if member_.member_type is _MEMBER:
        # Verify that the type is fixed.
        if not issubclass(member_.type, _FixedSizeType) and not is_byteclass_collection(member_.type):
            raise TypeError(f"member {member_.name} has invalid type {member_.type!r}")
    return member_
