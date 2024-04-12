"""Collection decorator internal functions."""

from collections.abc import Callable
from typing import cast

from ..._enums import ByteOrder
from ...types.collections._fixed_collection_type import _process_class
from ._collection_class_spec import _CollectionClassSpec
from .fixed_size_collection_protocol import FixedSizeCollection


def create_collection(
    cls: type | None,
    collection_type: str,
    byte_order: bytes | ByteOrder,
    packed: bool,
    methods: dict[str, Callable],
    allowed_types: tuple[type, ...] | None = None,
) -> FixedSizeCollection | Callable[[type], FixedSizeCollection]:
    """Create custom collection class."""
    if isinstance(byte_order, str):
        byte_order = ByteOrder(bytes(byte_order, encoding="utf8"))

    def outer_wrapper(cls: type) -> FixedSizeCollection:
        spec = _CollectionClassSpec(
            base_cls=cls,
            collection_type=collection_type,
            byte_order=ByteOrder(byte_order),
            packed=packed,
            methods=methods,
        )
        if allowed_types:
            spec.allowed_types = allowed_types
        new_cls: FixedSizeCollection = _process_class(spec)
        return cast(FixedSizeCollection, new_cls)

    # See if we're being called as @structure or @structure().
    if cls is None:
        return outer_wrapper  # We're called with parens.
    return outer_wrapper(cls)  # We're called as @structure without parens.
