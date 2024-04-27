"""Elf Dynamic Entry Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from enum import IntEnum

from ....types.collections import member, structure, union
from ....types.primitives.byte_enum import ByteEnum
from ....types.primitives.integers import Int32, Int64, UInt32, UInt64

__all__ = [
    "DynEntry32",
    "DynEntry64",
]


class DynTag(IntEnum):
    """Elf Dynamic Entry Tags."""

    NULL = 0
    NEEDED = 1
    PLTRELSZ = 2
    PLTGOT = 3
    HASH = 4
    STRTAB = 5
    SYMTAB = 6
    RELA = 7
    RELASZ = 8
    RELAENT = 9
    STRSZ = 10
    SYMENT = 11
    INIT = 12
    FINI = 13
    SONAME = 14
    RPATH = 15
    SYMBOLIC = 16
    REL = 17
    RELSZ = 18
    RELENT = 19
    PLTREL = 20
    DEBUG = 21
    TEXTREL = 22
    JMPREL = 23
    ENCODING = 32


@union
class DUn32:
    """32-bit Elf Dynamic Entry Union."""

    d_val: UInt32
    d_ptr: UInt32


@structure
class DynEntry32:
    """32-bit Elf Dynamic Entry."""

    d_tag: ByteEnum = member(factory=lambda byte_order: ByteEnum(DynTag, Int32, byte_order=byte_order))
    d_un: DUn32


@union
class DUn64:
    """64-bit Elf Dynamic Entry Union."""

    d_val: UInt64
    d_ptr: UInt64


@structure
class DynEntry64:
    """64-bit Elf Dynamic Entry."""

    d_tag: ByteEnum = member(factory=lambda byte_order: ByteEnum(DynTag, Int64, byte_order=byte_order))
    d_un: DUn64
