"""Fixed length structure type."""

from collections.abc import Callable
from typing import Any, overload

from ..._enums import ByteOrder
from ._collection import create_collection
from ._collection_class_spec import _CollectionClassSpec
from ._methods import _build_init_method
from .byteclass_collection_protocol import ByteclassCollection
from .member import _init_members, _member_assign

__all__ = ["structure"]


@overload
def structure(
    cls: None = None, /, *, byte_order: bytes | ByteOrder = ByteOrder.NATIVE, packed: bool = False
) -> Callable[[type], ByteclassCollection]: ...


@overload
def structure(
    cls: type, /, *, byte_order: bytes | ByteOrder = ByteOrder.NATIVE, packed: bool = False
) -> ByteclassCollection: ...


def structure(  # type: ignore
    cls: type | None = None,
    /,
    *,
    byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
    packed: bool = False,
) -> ByteclassCollection | Callable[[type], ByteclassCollection]:
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

    # Calculate structure member offsets
    body.append("collection_length = 0")
    for member_ in spec.members:
        body.append(f"mbr_len = len({spec.self_name}.{member_.name})")
        if not spec.packed:  # Insert padding to keep members aligned if not packed
            body.extend(
                [
                    "if collection_length % mbr_len != 0:",
                    "  padding = mbr_len - (collection_length % mbr_len)",
                    "  collection_length += padding",
                ]
            )
        body.extend(
            [
                f"{spec.self_name}.{member_.name}.offset = collection_length",
                "collection_length += mbr_len",
                _member_assign("_length", "collection_length", spec.self_name),
            ]
        )

    return _build_init_method(spec, body, globals_)
