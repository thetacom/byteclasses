"""A dataclass used to collect specification details for constructing a class."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..._enums import ByteOrder
from ...types.collections.member import Member


@dataclass
class _CollectionClassSpec:  # pylint: disable=R0902
    """Collection Class Specification."""

    base_cls: type
    collection_type: str
    byte_order: ByteOrder
    packed: bool
    methods: dict[
        str,
        Callable[
            ["_CollectionClassSpec", dict[str, Any]],
            Any,
        ],
    ]
    members: list[Member] = field(default_factory=list)
    allowed_types: tuple[type, ...] = field(default_factory=tuple)
    attributes: list[str] = field(default_factory=list)
    self_name: str = "self"
    length: int = 0
