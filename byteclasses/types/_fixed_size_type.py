"""Abstract fixed size type."""

from abc import ABC
from collections.abc import ByteString
from typing import SupportsBytes

from .._enums import ByteOrder

__all__: list[str] = []


class _FixedSizeType(ABC, SupportsBytes):
    """Base class for fixed size types."""

    _type_char: bytes = NotImplemented

    _length: int = NotImplemented

    def __init__(self, *, byte_order: bytes | ByteOrder, data: ByteString | None = None) -> None:
        """Initialize the instance."""
        if self._type_char is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__} does not implement '_type_char'")
        if self._length is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__} does not implement '_length'")
        self._byte_order = ByteOrder(byte_order)
        if data is None:
            self._data: bytearray | memoryview = bytearray(len(self))
        else:
            if isinstance(data, bytes):
                self._data = bytearray(data)
            else:
                self._data = data

    def __getitem__(self, sliced):
        return self._data[sliced]

    def __bytes__(self) -> bytes:
        """Return the byte representation of the instance."""
        return bytes(self._data)

    def __len__(self) -> int:
        """Return the byte length of the instance."""
        if self._length is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__}._length")
        return self._length if self._length >= 0 else 0

    def __str__(self) -> str:
        """Return the byte representation of the instance."""
        return f"0x{self.__bytes__().hex()}"

    @property
    def byte_order(self) -> ByteOrder:
        """Return the byte order of the instance."""
        return self._byte_order

    @byte_order.setter
    def byte_order(self, value: bytes | ByteOrder) -> None:
        """Set new byte order."""
        self._byte_order = ByteOrder(value)

    @property
    def endianness(self) -> str:
        """Return the string name of the byte order for the instance."""
        return self._byte_order.name

    @property
    def fmt(self) -> bytes:
        """Return the format string for the instance."""
        return self.byte_order.value + self.type_char

    @property
    def data(self) -> ByteString:
        """Return the byte representation of the instance."""
        return bytes(self._data[: self._length])

    @data.setter
    def data(self, new_value: bytes | bytearray | None = None) -> None:
        """Set the byte representation of the instance."""
        if new_value is None:
            # Setting data to None zeroes all data
            self._data[:] = bytes(len(self))
        else:
            if len(new_value) < len(self):
                end = len(new_value)
            elif len(new_value) == len(self):
                end = len(self)
            else:
                raise ValueError(f"{self.__class__.__name__} value must be <={len(self)} bytes long")
            self._data[:end] = new_value

    @property
    def type_char(self) -> bytes:
        """Return the type character of the class."""
        if self._type_char is NotImplemented:
            raise NotImplementedError(f"Type character not implemented for {self}")
        return self._type_char

    def attach(self, mv: memoryview, retain_value: bool = True) -> None:
        """Replace internal data and attach provided memoryview.

        Memoryview length must match byte length of fixed length type.
        """
        if not isinstance(mv, memoryview):
            raise TypeError("Only memoryviews can be attached to fixed length types.")
        mv_len = len(mv)
        self_len = len(self)
        if mv_len != len(self):
            raise ValueError(f"Memoryview length ({mv_len} bytes) must be {self_len} bytes.")
        temp = self._data
        self._data = mv
        if retain_value:
            self._data[:] = temp
