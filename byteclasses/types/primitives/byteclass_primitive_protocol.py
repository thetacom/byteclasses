"""Byteclass Primitive Protocol Classes."""

from typing import Protocol, runtime_checkable

__all__ = ["ByteclassPrimitive"]


@runtime_checkable
class ByteclassPrimitive(Protocol):
    """Protocol class for primitive types."""

    def __call__(self): ...
    def __len__(self) -> int: ...
    def __bytes__(self) -> bytes: ...
    def attach(self, mv: memoryview):
        """Attaches memoryview to underlying data attribute."""
