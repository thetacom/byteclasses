"""Fixed Size Type Protocol Classes."""

from typing import Protocol, runtime_checkable

__all__ = ["FixedSizeType"]


@runtime_checkable
class FixedSizeType(Protocol):
    """Protocol class for fixed size types."""

    def __call__(self): ...
    def __len__(self) -> int: ...
    def __bytes__(self) -> bytes: ...
    def attach(self, mv: memoryview):
        """Attaches memoryview to underlying data attribute."""
