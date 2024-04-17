"""Generic Data Handler Class."""

from abc import ABC


class _DataHandler(ABC):
    """A generic data handler class."""

    def __init__(self, data: bytes | bytearray) -> None:
        """Initialize data handler instance."""
        self._data: memoryview = memoryview(bytearray(data))

    def __bytes__(self) -> bytes:
        """Return data handler bytes."""
        return bytes(self._data)

    def __len__(self) -> int:
        """Return data handler length."""
        return len(self._data)

    def __repr__(self) -> str:
        """Return data handler representation."""
        return f"{self.__class__.__name__}(data={self._data!r})"

    def __str__(self) -> str:
        """Return data handler string."""
        return str(self._data)

    @property
    def data(self) -> memoryview:
        """Return data handler data."""
        return self._data
