"""Fixed Size Integer Types."""

from enum import IntEnum
from struct import calcsize

from ..._enums import TypeChar
from ...types._fixed_size_type import _FixedSizeType

__all__ = [
    "Bit",
    "Byte",
    "DWord",
    "QWord",
    "Word",
]


class Bit(IntEnum):
    """A boolean equivalent bit class."""

    FALSE = 0
    TRUE = 1


class Byte(_FixedSizeType):
    """Generic 8-bit Byte Class."""

    _type_char: bytes = TypeChar.BYTE.value
    _length: int = calcsize(_type_char)


class Word(_FixedSizeType):
    """Generic 2-byte Word Class."""

    _type_char: bytes = TypeChar.WORD.value
    _length: int = calcsize(_type_char)


class DWord(_FixedSizeType):
    """Generic 4-byte Word Class."""

    _type_char: bytes = TypeChar.DWORD.value
    _length: int = calcsize(_type_char)


class QWord(_FixedSizeType):
    """Generic 8-byte Word Class."""

    _type_char: bytes = TypeChar.QWORD.value
    _length: int = calcsize(_type_char)
