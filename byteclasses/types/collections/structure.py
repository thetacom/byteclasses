"""Fixed length structure type."""

from collections.abc import Callable
from typing import Any, overload

from ..._enums import ByteOrder
from ._collection import create_collection
from ._collection_class_spec import _CollectionClassSpec
from ._methods import _build_init_method
from .fixed_size_collection_protocol import FixedSizeCollection
from .member import _init_members

__all__ = ["structure"]


@overload
def structure(
    cls: type | None, /, *, byte_order: bytes | ByteOrder, packed: bool
) -> Callable[[type], FixedSizeCollection]: ...


@overload
def structure(cls: type) -> FixedSizeCollection: ...


def structure(  # type: ignore
    cls: type | None = None,
    /,
    *,
    byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
    packed: bool = False,
) -> FixedSizeCollection | Callable[[type], FixedSizeCollection]:
    """Return the same class as was passed in.

    Fixed length structure methods are added to the class.

    Implemented similar to the dataclasses.dataclass decorator.
    """
    methods: dict[str, Callable] = {
        "__init__": _build_structure_init_method,
    }
    structure_cls = create_collection(cls, "structure", byte_order, packed, methods)
    return structure_cls


def _build_structure_init_method(
    spec: _CollectionClassSpec,
    globals_: dict[str, Any],
) -> Callable:
    """Create structure init function."""
    body: list[str] = []
    body.extend(_init_members(spec, globals_))
    # Collect structure member lengths
    lengths_str = "[" + ",".join(f"len(self.{member_.name})" for member_ in spec.members) + "]"

    # Calculate structure member offsets
    body.extend(
        [
            f"member_lengths = {lengths_str}",
            "member_offsets = []",
            "collection_length = 0",
            "for l in member_lengths:",
        ]
    )
    if not spec.packed:  # Insert padding to keep members aligned if not packed
        body.extend(
            [
                "  if collection_length % l != 0:",
                "    padding = l - (collection_length % l)",
                "    collection_length += padding",
            ]
        )
    body.extend(
        [
            "  member_offsets.append(collection_length)",
            "  collection_length += l",
            f"{spec.self_name}._collection_init(collection_length, member_offsets)",
        ]
    )

    return _build_init_method(spec, body, globals_)
