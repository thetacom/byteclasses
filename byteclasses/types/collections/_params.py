"""Collection Parameter class."""

from ._collection_class_spec import _CollectionClassSpec


class _Params:
    """Contains the collection parameters for a fixed size collection."""

    __slots__ = ("type",)

    def __init__(self, spec: _CollectionClassSpec) -> None:
        """Initialize the collection parameters."""
        self.type = spec.collection_type

    def __repr__(self) -> str:
        """Return a repr string for this collection parameters."""
        return f"_Params(type={self.type=!r})"
