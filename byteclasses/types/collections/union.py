"""Fixed length Union type."""

from collections.abc import Callable
from typing import Any, overload

from ..._enums import ByteOrder
from ._collection import create_collection
from ._collection_class_spec import _CollectionClassSpec
from ._methods import _build_init_method
from .byteclass_collection_protocol import ByteclassCollection
from .member import _init_members, _member_assign

__all__ = ["union"]


@overload
def union(
    cls: None = None, /, *, byte_order: bytes | ByteOrder = ByteOrder.NATIVE
) -> Callable[[type], ByteclassCollection]: ...


@overload
def union(cls: type, /, *, byte_order: bytes | ByteOrder = ByteOrder.NATIVE) -> ByteclassCollection: ...


def union(  # type: ignore
    cls: type | None = None,
    /,
    *,
    byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
) -> ByteclassCollection | Callable[[type], ByteclassCollection]:
    """Return the same class as was passed in.

    Fixed length union methods are added to the class.

    Implemented similar to the dataclasses.dataclass decorator.
    """
    methods: dict[str, Callable] = {
        "__init__": _build_union_init_method,
    }
    union_cls = create_collection(cls, "union", byte_order, True, methods)
    return union_cls


def _build_union_init_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Create union init function."""

    body = []
    body.extend(_init_members(spec, globals_))

    # Initialize union member offsets to 0
    for member_ in spec.members:
        body.append(f"{spec.self_name}.{member_.name}.offset = 0")

    # Collect union member lengths
    lengths_str = "[" + ",".join(f"len(self.{member_.name})" for member_ in spec.members) + "]"
    body.extend(
        [
            f"member_lengths = {lengths_str}",
            "collection_length = max(member_lengths)",
            _member_assign("_length", "collection_length", spec.self_name),
        ]
    )

    return _build_init_method(spec, body, globals_)
