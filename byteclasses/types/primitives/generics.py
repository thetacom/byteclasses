"""Fixed Size Integer Types."""

from enum import IntEnum
from struct import calcsize

from ..._enums import TypeChar
from ...types.primitives._primitive import _Primitive
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


class Byte(_Primitive):
    """Generic 8-bit Byte Class."""

    _type_char: bytes = TypeChar.BYTE.value
    _length: int = calcsize(_type_char)


class Word(_Primitive):
    """Generic 2-byte Word Class."""

    _type_char: bytes = TypeChar.WORD.value
    _length: int = calcsize(_type_char)


class DWord(_Primitive):
    """Generic 4-byte Word Class."""

    _type_char: bytes = TypeChar.DWORD.value
    _length: int = calcsize(_type_char)


class QWord(_Primitive):
    """Generic 8-byte Word Class."""

    _type_char: bytes = TypeChar.QWORD.value
    _length: int = calcsize(_type_char)
