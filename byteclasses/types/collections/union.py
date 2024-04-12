"""Fixed length Union type."""

from collections.abc import Callable
from typing import Any, overload

from ..._enums import ByteOrder
from ._collection import create_collection
from ._collection_class_spec import _CollectionClassSpec
from ._methods import _build_init_method
from .fixed_size_collection_protocol import FixedSizeCollection
from .member import _init_members

__all__ = ["union"]


@overload
def union(*, byte_order: bytes | ByteOrder) -> Callable[[type], FixedSizeCollection]: ...


@overload
def union(cls: type, /, *, byte_order: bytes | ByteOrder = ByteOrder.NATIVE) -> FixedSizeCollection: ...


def union(
    cls: type | None = None,
    /,
    *,
    byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
) -> FixedSizeCollection | Callable[[type], FixedSizeCollection]:
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
    # Collect union member lengths
    lengths_str = "[" + ",".join(f"len(self.{member_.name})" for member_ in spec.members) + "]"

    # Initialize union member offsets to 0
    body.extend(
        [
            f"member_lengths = {lengths_str}",
            "member_offsets = [0 for _ in member_lengths]",
            "collection_length = max(member_lengths)",
            f"{spec.self_name}._collection_init(collection_length, member_offsets)",
        ]
    )

    return _build_init_method(spec, body, globals_)
