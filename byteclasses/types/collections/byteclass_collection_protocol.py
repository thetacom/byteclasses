""""Fixed Size Collection Protocol."""

from collections.abc import ByteString
from typing import Protocol, runtime_checkable

from ._params import _Params
from .member import Member

__all__ = [
    "ByteclassCollectionError",
    "ByteclassCollection",
]


class ByteclassCollectionError(AttributeError):
    """Raised when an invalid operation is performed on a fixed size collection."""


@runtime_checkable
class ByteclassCollection(Protocol):
    """Protocol class for fixed size collection types."""

    __collection_members__: list[Member]
    __collection_params__: _Params
    data: bytearray

    def __call__(self): ...
    def __bytes__(self) -> bytes: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: int | slice) -> int | ByteString: ...
    def __setitem__(self, key: int | slice, value: int | ByteString) -> None: ...
    def attach(self, mv: memoryview) -> None:
        """Attach memoryview to underlying data attribute."""
