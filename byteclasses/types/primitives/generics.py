"""Fixed Size Integer Types."""

from collections.abc import ByteString
from enum import IntEnum
from struct import calcsize
from typing import Any

from ..._enums import ByteOrder, TypeChar
from ...types._fixed_size_type import _FixedSizeType
from .bitfield import BitField, BitField16, BitField32, BitField64, BitPos

__all__ = [
    "Bit",
    "Byte",
    "DWord",
    "QWord",
    "Word",
    "BitField",
    "BitField16",
    "BitField32",
    "BitField64",
    "BitPos",
]


class Bit(IntEnum):
    """A boolean equivalent bit class."""

    FALSE = 0
    TRUE = 1


class _FixedSizeGeneric(_FixedSizeType):
    """A generic fixed size type."""

    def __init__(
        self,
        value: ByteString | None = None,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE.value,
        data: ByteString | None = None,
    ) -> None:
        """Initialize Fixed Size Generic instance."""
        if value is not None and data is not None:
            raise ValueError("Cannot specify both value and data arguments.")
        super().__init__(byte_order=byte_order, data=data)
        if value is not None:
            if isinstance(value, (bytes, bytearray, memoryview)):
                self.value = value
            else:
                raise TypeError(f"Invalid value type ({type(value)}): expected bytes")

    @property
    def value(self) -> Any:
        """Return the value of the instance."""
        return self.data

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the value of the instance."""
        self.data = new_value


class Byte(_FixedSizeGeneric):
    """Generic 8-bit Byte Class."""

    _type_char: bytes = TypeChar.BYTE.value
    _length: int = calcsize(_type_char)


class Word(_FixedSizeGeneric):
    """Generic 2-byte Word Class."""

    _type_char: bytes = TypeChar.WORD.value
    _length: int = calcsize(_type_char)


class DWord(_FixedSizeGeneric):
    """Generic 4-byte Word Class."""

    _type_char: bytes = TypeChar.DWORD.value
    _length: int = calcsize(_type_char)


class QWord(_FixedSizeGeneric):
    """Generic 8-byte Word Class."""

    _type_char: bytes = TypeChar.QWORD.value
    _length: int = calcsize(_type_char)
