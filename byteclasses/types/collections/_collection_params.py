"""Collection Parameter class."""

from ._collection_class_spec import _CollectionClassSpec


class _CollectionParams:
    """Contains the collection parameters for a fixed size collection."""

    __slots__ = (
        "type",
        "byte_order",
    )

    def __init__(self, spec: _CollectionClassSpec) -> None:
        """Initialize the collection parameters."""
        self.type = spec.collection_type
        self.byte_order = spec.byte_order

    def __repr__(self) -> str:
        """Return a repr string for this collection parameters."""
        return f"_CollectionParams({self.byte_order=!r})"
