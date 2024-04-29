"""Constructors for common collection class methods."""

import builtins
from collections.abc import ByteString, Callable, Iterable
from functools import cached_property, singledispatchmethod
from reprlib import recursive_repr
from typing import Any, cast

from ..._enums import ByteOrder
from ._collection_class_spec import _CollectionClassSpec
from ._util import _tuple_str
from .byteclass_collection_protocol import ByteclassCollectionError
from .member import MISSING, _member_assign


def _create_method(
    name: str,
    args: Iterable[str],
    body: Iterable[str],
    decorators: Iterable[str] | None = None,
    *,
    globals_: dict[str, Any] | None = None,
    locals_: dict[str, Any] | None = None,
    return_type: Any = MISSING,
) -> Callable:
    if locals_ is None:
        locals_ = {}
    if "BUILTINS" not in locals_:
        locals_["BUILTINS"] = builtins
    return_annotation = ""
    if return_type is not MISSING:
        locals_["_return_type"] = return_type
        return_annotation = "->_return_type"
    args = ",".join(args)
    body = "\n".join(f"    {line}" for line in body)
    decorator_lines = "\n  ".join(f"@{decorator}" for decorator in decorators or [])
    # Compute the text of the entire function.
    txt = f"  {decorator_lines}\n  def {name}({args}){return_annotation}:\n{body}"

    local_vars = ", ".join(locals_.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n  return {name}"
    # print(txt)
    namespace: dict[str, Any] = {}
    exec(txt, globals_, namespace)  # nosec pylint: disable=exec-used
    return cast(Callable[..., Any], namespace["__create_fn__"](**locals_))


def _build_init_method(
    spec: _CollectionClassSpec,
    body: list[str],
    globals_: dict[str, Any],
) -> Callable:
    """Create structure init function."""
    locals_: dict[str, Any] = {f"_type_{member_.name}": member_.type for member_ in spec.members}
    locals_.update({"MISSING": MISSING, "ByteString": ByteString, "ByteOrder": ByteOrder})
    init_body = [
        _member_assign("byte_order", "byte_order", spec.self_name),
        _member_assign("offset", "0", spec.self_name),
    ]
    init_body.extend(body)
    init_body.extend(
        [
            # Initialize _data
            _member_assign("_data", f"memoryview(bytearray({spec.self_name}._length))", spec.self_name),
            # Attach members to slices of _data memoryview
            f"{spec.self_name}._attach_members(retain_value=True)",
            "if data is not None:",
            f"  {spec.self_name}.data = data",
        ]
    )
    return _create_method(
        "__init__",
        [spec.self_name, "data: ByteString | None = None", f"byte_order: bytes = {spec.byte_order.value!r}"],
        init_body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )


def _build_len_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a __len__ method for the class."""
    locals_ = {
        "cls": spec.base_cls,
        "byte_order": spec.byte_order,
        "packed": spec.packed,
        "cached_property": cached_property,
        "singledispatchmethod": singledispatchmethod,
    }

    body = [f"return {spec.self_name}._length"]
    return _create_method(
        "__len__",
        (spec.self_name,),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=int,
    )


def _build_repr_method(spec: _CollectionClassSpec, globals_: dict[str, Any] | None) -> Callable:
    """Create the __repr__ function for a fixed collection class."""
    locals_ = {"recursive_repr": recursive_repr}
    func = _create_method(
        "__repr__",
        (spec.self_name,),
        [
            "return "
            + spec.self_name
            + '.__class__.__qualname__ + f"(byte_order={ '
            + spec.self_name
            + ".byte_order},"
            + "data={"
            + spec.self_name
            + '.data!r})"',
        ],
        # decorators=["recursive_repr"],
        globals_=globals_,
        locals_=locals_,
    )
    return func


def _build_str_method(spec: _CollectionClassSpec, globals_: dict[str, Any] | None) -> Callable:
    """Create the __str__ function for a fixed collection class."""
    locals_ = {"recursive_repr": recursive_repr}
    func = _create_method(
        "__str__",
        (spec.self_name,),
        [
            "return "
            + spec.self_name
            + '.__class__.__qualname__ + f"('
            + ", ".join([f"{member_.name}={{self.{member_.name}!r}}" for member_ in spec.members])
            + ')"'
        ],
        # decorators=["recursive_repr"],
        globals_=globals_,
        locals_=locals_,
    )
    return func


def _build_del_attr(spec: _CollectionClassSpec, globals_: dict[str, Any]) -> Callable:
    """Create the __delattr__ function for a fixed collection class."""
    locals_ = {"cls": spec.base_cls, "ByteclassCollectionError": ByteclassCollectionError}
    members_str = "(" + ",".join(repr(member_.name) for member_ in spec.members) + ",)"
    return _create_method(
        "__delattr__",
        (spec.self_name, "name"),
        (
            f"if type({spec.self_name}) is cls or name in {members_str}:",
            ' raise ByteclassCollectionError(f"cannot delete member {name!r}")',
            f"super(cls, {spec.self_name}).__delattr__(name)",
        ),
        locals_=locals_,
        globals_=globals_,
    )


def _build_cmp_method(
    spec: _CollectionClassSpec,
    name: str,
    operation: str,
    self_tuple_str: str,
    other_tuple_str: str,
    globals_: dict[str, Any],
) -> Callable:
    """Create a comparison function for a fixed collection class.

    If the members in the object are named 'x' and 'y', then self_tuple is the string
    '(self.x,self.y)' and other_tuple is the string '(other.x,other.y)'.
    """
    return _create_method(
        name,
        (spec.self_name, "other"),
        [
            f"if other.__class__ is {spec.self_name}.__class__:",
            f" return {self_tuple_str}{operation}{other_tuple_str}",
            "return NotImplemented",
        ],
        globals_=globals_,
    )


def _build_hash_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Create a hash function for a fixed collection class."""
    self_tuple = _tuple_str(spec.self_name, spec.members)
    return _create_method("__hash__", (spec.self_name,), [f"return hash({self_tuple})"], globals_=globals_)


# Decide if/how we're going to create a hash function.  Key is
# (unsafe_hash, eq, frozen, does-hash-exist).  Value is the action to
# take.  The common case is to do nothing, so instead of providing a
# function that is a no-op, use None to signify that.


def _raise_hash_exception(spec: _CollectionClassSpec, __) -> None:
    """Raise an exception to signify that hash function already exists."""
    raise TypeError(f"Cannot overwrite attribute __hash__ " f"in class {spec.base_cls.__name__}")


def _build_attach_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a public attach method for the class.

    Attaches provided memoryview to internal _data attribute after validation.
    """
    locals_ = {
        "cls": spec.base_cls,
        "memoryview": memoryview,
        "bytearray": bytearray,
        "bytes": bytes,
        "ByteString": ByteString,
    }
    body = (
        "data_len = len(new_data)",
        f"self_len = len({spec.self_name})",
        "if data_len < self_len:",
        "  raise AttributeError(f'Data length ({data_len}) must greater than or equal to {self_len} bytes.')",
        "if isinstance(new_data, memoryview):",
        "  mv: memoryview = new_data",
        "elif isinstance(new_data, bytearray):",
        "  mv = memoryview(new_data)",
        "elif isinstance(new_data, bytes):",
        "  mv = memoryview(bytearray(new_data))",
        "else:",
        "  raise TypeError(f'Unsupported data type ({type(new_data)})')",
        f"{spec.self_name}._data = mv[:self_len]",
        f"{spec.self_name}._attach_members(retain_value)",
    )
    return _create_method(
        "attach",
        (spec.self_name, "new_data: ByteString", "retain_value: bool = False"),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )


def _build_attach_members_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a private _attach_members method for the class.

    Attaches members to internal _data attribute.
    """
    locals_ = {
        "cls": spec.base_cls,
    }
    lengths_str = "[" + ",".join(f"len(self.{member_.name})" for member_ in spec.members) + "]"
    body: list[str] = [f"member_lengths = {lengths_str}"]
    for member_ in spec.members:
        body.append(
            f"{spec.self_name}.{member_.name}.attach("
            f"{spec.self_name}._data[{spec.self_name}.{member_.name}.offset:"
            f"{spec.self_name}.{member_.name}.offset + len({spec.self_name}.{member_.name})], retain_value)"
        )

    return _create_method(
        "attach",
        (spec.self_name, "retain_value: bool = False"),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )


def _build_bytes_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a __bytes__ method for the class."""
    locals_ = {
        "cls": spec.base_cls,
    }
    body = [
        f"return bytes({spec.self_name}._data)",
    ]
    return _create_method(
        "__bytes__",
        (spec.self_name,),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type="bytes",
    )


def _build_data_property(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> property:
    getter = _build_data_getter_method(spec, globals_)
    setter = _build_data_setter_method(spec, globals_)
    return property(getter, setter)


def _build_data_getter_method(spec: _CollectionClassSpec, globals_: dict[str, Any]) -> Callable:
    """Generate a data getter method for the class."""
    locals_: dict[str, Any] = {}
    body = [f"return bytearray({spec.self_name}._data)"]

    return _create_method(
        "_get_data",
        (spec.self_name,),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=bytearray,
    )


def _build_data_setter_method(spec: _CollectionClassSpec, globals_: dict[str, Any]) -> Callable:
    """Generate a data setter method for the class."""
    locals_ = {
        "cls": spec.base_cls,
        "ByteString": ByteString,
    }
    body: list[str] = [
        f"if len(value) < len({spec.self_name}):",
        "  raise ValueError(f'{value} is too short for {" + spec.self_name + ".__class__.__name__}')",
        f"{spec.self_name}._data[:] = value",
    ]
    return _create_method(
        "_set_data",
        (spec.self_name, "value: ByteString"),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )


def _build_getitem_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a __getitem__ method for the class."""

    body = [
        "if isinstance(key, int):",
        "  if key < 0:",
        f"    key += len({spec.self_name})",
        f"  if key >= len({spec.self_name}):",
        "    raise IndexError(f'index {key} out of range')",
        f"  return {spec.self_name}._data[key]",
        "if isinstance(key, slice):",
        f"  return bytes({spec.self_name}._data[key])",
        f"return {spec.self_name}.__getattr__(key)",
    ]
    return _create_method(
        "__getitem__",
        (spec.self_name, "key: int | slice"),
        body,
        globals_=globals_,
        return_type="int | ByteString | _Primitive",
    )


def _build_setitem_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a __setitem__ method for the class."""
    locals_ = {
        "cls": spec.base_cls,
        "ByteString": ByteString,
    }

    body = [
        "if isinstance(key, int) and isinstance(value, int):",
        "  if key < 0:",
        f"    key += len({spec.self_name})",
        f"  if key < 0 or key >= len({spec.self_name}):",
        "    raise IndexError(f'index {key} out of range')",
        "  if value < 0 or value > 255:",
        "    raise ValueError(f'value {value} out of range')",
        f"  {spec.self_name}._data[key] = value",
        "elif isinstance(key, slice):",
        "  if key.start is None:",
        "    start = 0",
        "  else:",
        "    start = key.start",
        "  if key.stop is None:",
        f"    stop = len({spec.self_name})",
        "  else:",
        "    stop = key.stop",
        "  if key.step is None:",
        "    step = 1",
        "  else:",
        "    step = key.step",
        "  data = self.data",
        f"  if type(value) == type({spec.self_name}):",
        "    data[key] = value.data[key]",
        "  elif getattr(value, '_COLLECTION_PARAMS', None) is not None and "
        f"len({spec.self_name}) == len(value):"
        "    data[key] = value.data[key]",
        "  elif isinstance(value, ByteString) and len(value) == 1:",
        "    for i in range(start, stop, step):",
        "      data[i] = value[0]",
        "  elif isinstance(value, int):",
        "    for i in range(start, stop, step):",
        "      data[i] = value",
        "  else:",
        "    raise TypeError(f'Invalid slice asignment for {" + spec.self_name + ".__class__.__name__}')",
        f"  {spec.self_name}._data[:] = data",
        "else:",
        f"  super(cls, {spec.self_name}).__setitem__(key, value)",
    ]
    return _create_method(
        "__setitem__",
        (spec.self_name, "key: int | slice", "value: int | ByteString"),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )


def _build_delattr_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a proxy delattr for the class.

    Prevents the member attributes from being deleted.
    """
    locals_ = {
        "cls": spec.base_cls,
    }
    attributes_str = "(" + ",".join(repr(attr_) for attr_ in spec.attributes) + ",)"
    members_str = "(" + ",".join(repr(member_.name) for member_ in spec.members) + ",)"
    setter_body = (
        f"if attr in {attributes_str}:",
        "  raise AttributeError('Cannot delete required attribute from collection.')",
        f"if attr in {members_str}:",
        "  raise AttributeError('Cannot delete member from collection.')",
        "super().__delattr__(attr)",
    )
    return _create_method(
        "__delattr__",
        (spec.self_name, "attr"),
        setter_body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )


def _build_setattr_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Generate a custom setattr for the class."""
    locals_ = {
        "cls": spec.base_cls,
    }

    members_str = "(" + ",".join(repr(member_.name) for member_ in spec.members) + ",)"
    body = (
        f"if name in {members_str}:",
        f"  item = {spec.self_name}.__getattribute__(name)",
        "  if getattr(item, '_COLLECTION_PARAMS', None) is not None:",
        "    item.data = value",
        "  else:",
        "    item.value = value",
        f"elif name == 'data' or name in {spec.self_name}.__slots__:",
        f"  BUILTINS.object.__setattr__({spec.self_name}, name, value)",
        "else:",
        "  raise AttributeError(f'{name} is not a member or property of {cls.__name__}')",
    )
    return _create_method(
        "__setattr__",
        (spec.self_name, "name", "value"),
        body,
        locals_=locals_,
        globals_=globals_,
        return_type=None,
    )
