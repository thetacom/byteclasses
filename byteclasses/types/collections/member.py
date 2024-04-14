"""Member class for fixed size collections."""

import re
import sys
from collections.abc import Callable
from types import GenericAlias, MappingProxyType, MemberDescriptorType
from typing import TYPE_CHECKING, Any

from ...types._fixed_size_type import _FixedSizeType

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


# The name of an attribute on the class where we store the Member objects.
# Also used to check if a class is a Fixed Size Collection Class.
_MEMBERS = "__collection_members__"

# The name of an attribute on the class that stores the parameters to
# fixed collection.
_PARAMS = "__collection_params__"

# String regex that string annotations for ClassVar or InitVar must match.
# Allows "identifier.identifier[" or "identifier[".
# https://bugs.python.org/issue33453 for details.
_MODULE_IDENTIFIER_RE = re.compile(r"^(?:\s*(\w+)\s*\.)?\s*(\w+)")

_MEMBER = _MemberBase("_MEMBER")
_MEMBER_CLASSVAR = _MemberBase("_MEMBER_CLASSVAR")


class _HasDefaultFactoryClass:  # pylint: disable=R0903
    def __repr__(self):
        return "<factory>"


_HAS_DEFAULT_FACTORY = _HasDefaultFactoryClass()


class _MissingType:  # pylint: disable=R0903
    """A sentinel object to detect if a parameter is supplied or not.

    Use a class to give it a better repr.
    """


MISSING = _MissingType()


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
        "default",
        "default_factory",
        "metadata",
        "member_type",  # Private: not to be used by user code.
    )

    def __init__(
        self,
        default,
        default_factory,
        metadata,
    ):
        """Initialize a Member object."""
        self.name: str | None = None
        self.type: type | None = None
        self.default: Any = default
        self.default_factory: Callable = default_factory
        self.metadata = _EMPTY_METADATA if metadata is None else MappingProxyType(metadata)
        self.member_type: _MemberBase | None = None

    def __repr__(self):
        """Return a repr string for this Member."""
        return (
            "Field("
            f"{self.name=!r},"
            f"{self.type=!r},"
            f"{self.default=!r},"
            f"{self.default_factory=!r},"
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
        func = getattr(type(self.default), "__set_name__", None)
        if func:
            # There is a __set_name__ method on the descriptor, call
            # it.
            func(self.default, owner, name)

    __class_getitem__ = classmethod(GenericAlias)  # type: ignore


# This function is used instead of exposing Member creation directly,
# so that a type checker can be told (via overloads) that this is a
# function whose type depends on its parameters.
def member(
    *,
    default=MISSING,
    default_factory=MISSING,
    metadata=None,
) -> Member:
    """Return an object to identify dataclass fields.

    default is the default value of the field.  default_factory is a
    0-argument function called to initialize a member's value. metadata, if specified,
    must be a mapping which is stored but not otherwise examined by the fixed
    collection.

    It is an error to specify both default and default_factory.
    """
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    return Member(default, default_factory, metadata)


def _member_assign(name: str, value: Any, self_name: str) -> str:
    # self_name is what "self" is called in this function: don't
    # hard-code "self", since that might be a field name.
    return f"BUILTINS.object.__setattr__({self_name},{name!r},{value})"


def _init_members(spec: "_CollectionClassSpec", globals_: dict[str, Any]) -> list[str]:
    """Initialize all class members."""
    body: list[str] = []
    for member_ in spec.members:
        line = _init_member(member_, globals_, spec.self_name)
        if line:
            body.extend(
                [
                    line,
                    "try:",
                    f"  {spec.self_name}.{member_.name}.byte_order = {spec.byte_order.value!r}",
                    "except AttributeError:",
                    "  pass",
                ]
            )
    return body


def _init_member(
    member_: Member,
    globals_: dict[str, Any],
    self_name: str,
) -> str:
    # Return the text of the line in the body of __init__ that will
    # initialize this field.

    default_name = f"_dflt_{member_.name}"
    if member_.default is not MISSING:
        globals_[default_name] = member_.default
        value = member_.name
    else:
        if member_.default_factory is not MISSING:
            globals_[default_name] = member_.default_factory
        else:
            # No default factory. Use member type as constructor.
            globals_[default_name] = member_.type
        value = f"{default_name}() " f"if {member_.name} is _HAS_DEFAULT_FACTORY " f"else {member_.name}"
    if member_.name is None:
        raise ValueError("Member name cannot be None.")
    # Now, actually generate the member assignment.
    return _member_assign(member_.name, value, self_name)


def _init_param(member_: Member) -> str:
    # Return the __init__ parameter string for this field.  For
    # example, the equivalent of 'x: int = 3' (except instead of 'int',
    # reference a variable set to int, and instead of '3', reference a
    # variable set to 3).
    if member_.default is not MISSING:
        # There's a default, this will be the name that's used to look
        # it up.
        default = f"=_dflt_{member_.name}"
    else:
        # Name used when default factory is provided or inferred.
        default = "=_HAS_DEFAULT_FACTORY"
    return f"{member_.name}:_type_{member_.name}{default}"


def _is_classvar(a_type, typing) -> bool:
    """Test is the provided type is a ClassVar.

    This test uses a typing internal class, but it's the best way to test if this
    is a ClassVar.
    """
    return a_type is typing.ClassVar or (
        type(a_type)  # pylint: disable=unidiomatic-typecheck
        is typing._GenericAlias  # pylint: disable=protected-access
        and a_type.__origin__ is typing.ClassVar
    )


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
    else:
        if isinstance(default, MemberDescriptorType):
            # This is a member in __slots__, so it has no default value.
            default = MISSING
        member_ = member(default=default)

    # Only at this point do we know the name and the type.  Set them.
    member_.name = a_name
    member_.type = a_type

    # Assume it's a normal member until proven otherwise.  We're next
    # going to decide if it's a ClassVar, everything else is just a normal member.
    member_.member_type = _MEMBER

    # In addition to checking for actual types here, also check for
    # string annotations.  get_type_hints() won't always work for us
    # (see https://github.com/python/typing/issues/508 for example),
    # plus it's expensive and would require an eval for every string
    # annotation.  So, make a best effort to see if this is a ClassVar
    # using regex's and checking that the thing referenced
    # is actually of the correct type.

    # For the complete discussion, see https://bugs.python.org/issue33453

    # If typing has not been imported, then it's impossible for any
    # annotation to be a ClassVar.  So, only look for ClassVar if
    # typing has been imported by any module (not necessarily cls's
    # module).
    typing = sys.modules.get("typing")
    if typing:
        if _is_classvar(a_type, typing) or (
            isinstance(member_.type, str) and _is_type(member_.type, cls, typing, typing.ClassVar, _is_classvar)
        ):
            member_.member_type = _MEMBER_CLASSVAR

    # Validations for individual fields.  This is delayed until now,
    # instead of in the Field() constructor, since only here do we
    # know the field name, which allows for better error reporting.

    # Special restrictions for ClassVar and InitVar.
    if member_.member_type is _MEMBER_CLASSVAR:
        if member_.default_factory is not MISSING:
            raise TypeError(f"member {member_.name} cannot have a default factory")

    # For real members, disallow any non fixed types
    if member_.member_type is _MEMBER:
        # Verify that the type is fixed.
        if not issubclass(member_.type, _FixedSizeType) and not is_fixed_collection(member_.type):
            raise TypeError(f"member {member_.name} has invalid type {member_.type!r}")
        # Verify the default is the same type as the field.
        if member_.default is not MISSING and not isinstance(member_.default, member_.type):
            raise TypeError(
                f"member {member_.name} ({type(member_.default)}) default value " f"must be of type {member_.type!r}"
            )
    return member_


def _is_fixed_collection_instance(obj: Any) -> bool:
    """Return True if obj is an instance of a fixed collection."""
    return hasattr(type(obj), _MEMBERS)


def is_fixed_collection(obj: Any) -> bool:
    """Return True if obj is a class or instance of a fixed collection."""
    cls = obj if isinstance(obj, type) and not isinstance(obj, GenericAlias) else type(obj)
    return hasattr(cls, _MEMBERS)
