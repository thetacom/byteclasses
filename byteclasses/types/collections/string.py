"""Fixed Size String Byteclass."""

from collections.abc import ByteString

from ..primitives.characters import UChar
from .byte_array import ByteArray


class String(ByteArray):
    """A fixed size string collection based on ByteArray.

    Collection members are UChar primitives and are interpreted with a `utf-8` encoding.
    """

    def __init__(
        self, length: int, *, value: str | None = None, data: bytes | None = None, null_terminated: bool = True
    ) -> None:
        """Initialize String instance."""
        self._null_terminated: bool = null_terminated
        super().__init__(length, UChar)
        if data is not None and value is not None:
            raise ValueError("Cannot specify both value and data.")
        if data is not None:
            self.data = data
        if value is not None:
            self.value = value

    def __str__(self) -> str:
        """Return string representation."""
        return self.value

    def __repr__(self) -> str:
        """Return raw representation."""
        return f"{self.__class__.__name__}({len(self._items)}, value={self.value!r})"

    @property
    def data(self) -> bytes:
        """Return array data."""
        return bytes(self._data)

    @data.setter
    def data(self, new_data: ByteString) -> None:
        """Set array data."""
        if len(new_data) != self._length:
            raise ValueError(f"Invalid data length, expected {self._length}, receieved {len(new_data)}")
        self._data[:] = new_data
        if self._null_terminated:
            self._null_terminate()

    @property
    def value(self) -> str:
        """Return String value."""
        return "".join([item.value for item in self._items]).rstrip("\x00")

    @value.setter
    def value(self, new_value: str) -> None:
        """Set String value."""
        max_length = self._length - 1 if self.null_terminated else self._length
        value_bytes = new_value.encode("utf8").ljust(max_length, b"\x00")[:max_length]
        if self.null_terminated:
            value_bytes += b"\x00"
        self.data = value_bytes

    @property
    def null_terminated(self) -> bool:
        """Return String null terminated status."""
        return self._null_terminated

    def _null_terminate(self) -> None:
        """Null terminate string."""
        self[-1] = b"\x00"
