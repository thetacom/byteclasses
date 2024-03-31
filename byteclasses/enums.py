"""Byteclasses Enums module."""

from enum import Enum

__all__ = ["ByteOrder", "TypeChar"]


class ByteOrder(Enum):
    """Byte order for binary data.

    Base on the endianness values supported by the Python struct module.
    https://docs.python.org/3/library/struct.html
    """

    # Endianness | Size | Alignment
    NATIVE = b"@"  # native | native | native
    NATIVE_STD = b"="  # native | standard | none
    LE = b"<"  # little | standard | none
    BE = b">"  # big | standard | none
    NET = b"!"  # big | standard | none


class TypeChar(Enum):
    """Fixed size types for binary data.

    Base on the types supported by the Python struct module.
    https://docs.python.org/3/library/struct.html
    """

    # Single byte types
    PAD = b"x"  # Pad byte; size 1 byte
    BOOL = b"?"  # bool; size 1 byte
    CHAR = b"c"  # char; size 1 byte
    INT8 = b"b"  # int8_t; size 1 byte
    UINT8 = b"B"  # uint8_t; size 1 byte

    # Two byte types
    INT16 = b"h"  # int16_t; size 2 bytes
    UINT16 = b"H"  # uint16_t; size 2 bytes
    FLOAT16 = b"e"  # float16_t; size 2 bytes

    # Four byte types
    INT32 = b"i"  # int32_t; size 4 bytes
    UINT32 = b"I"  # uint32_t; size 4 bytes
    FLOAT32 = b"f"  # float; size 4 bytes

    # Eight byte types
    INT64 = b"q"  # int64_t; size 8 bytes
    UINT64 = b"Q"  # uint64_t; size 8 bytes
    FLOAT64 = b"d"  # double; size 8 bytes

    # Platform dependent types
    SSIZE = b"n"  # ssize_t; size native
    SIZE = b"N"  # size_t; size native
    LONG = b"l"  # long int; size native
    ULONG = b"L"  # unsigned long int; size native

    # Variable length types
    STR = b"s"  # string; size variable
    PASCAL = b"p"  # Pascal string; size variable

    # Alias types
    BIT = BOOL  # Bit; size 1 byte
    SCHAR = INT8  # signed char; size 1 byte
    UCHAR = UINT8  # unsigned char; size 1 byte
    BYTE = UCHAR  # unsigned char; size 1 byte

    SHORT = INT16  # short; size 2 bytes
    USHORT = UINT16  # unsigned short; size 2 bytes
    WORD = UINT16  # Single word; size 2 bytes
    HALF = FLOAT16  # half; size 2 bytes

    INT = INT32  # int; size 4 bytes
    UINT = UINT32  # unsigned int; size 4 bytes
    DWORD = UINT32  # Double word; size 4 bytes
    FLOAT = FLOAT32  # float; size 4 bytes

    LONG_LONG = INT64  # long long; size 8 bytes
    ULONG_LONG = UINT64  # unsigned long long; size 8 bytes
    QWORD = UINT64  # Quad word; size 8 bytes
    DOUBLE = FLOAT64  # double; size 8 bytes

    BYTES = STR  # byte array; size variable
    ARRAY = STR  # array; size variable
