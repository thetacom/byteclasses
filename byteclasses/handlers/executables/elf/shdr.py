"""Elf Section Header Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from enum import IntEnum

from ....types.collections import member, structure
from ....types.primitives.byte_enum import ByteEnum
from ....types.primitives.generics import BitField32, BitPos
from ....types.primitives.integers import Ptr32, Ptr64, UInt32, UInt64

__all__ = [
    "SHdr32",
    "SHdr64",
    "SHdrType",
    "SBitField32",
    "SBitField64",
]


class SBitField32(BitField32):
    """Section BitField32."""

    WRITE = BitPos(0)  # 0x1
    ALLOC = BitPos(1)  # 0x2
    EXECINSTR = BitPos(2)  # 0x4
    RELA_LIVEPATCH = BitPos(20)  # 0x00100000
    RO_AFTER_INIT = BitPos(21)  # 0x00200000
    MASKPROC = BitPos(28, bit_width=4)  # 0xF0000000


class SBitField64(SBitField32):
    """Section BitField64."""

    byte_length = 8


@structure
class SHdr32:
    """32-bit Elf Section Header."""

    sh_name: UInt32
    sh_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(SHdrType, UInt32, byte_order=byte_order))
    sh_flags: SBitField32
    sh_addr: Ptr32
    sh_offset: UInt32
    sh_size: UInt32
    sh_link: UInt32
    sh_info: UInt32
    sh_addralign: UInt32
    sh_entsize: UInt32


@structure
class SHdr64:
    """64-bit Elf Section Header."""

    sh_name: UInt32
    sh_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(SHdrType, UInt32, byte_order=byte_order))
    sh_flags: SBitField64
    sh_addr: Ptr64
    sh_offset: UInt64
    sh_size: UInt64
    sh_link: UInt32
    sh_info: UInt32
    sh_addralign: UInt64
    sh_entsize: UInt64


class SHdrType(IntEnum):
    """Elf Section Header Types."""

    NULL = 0
    PROGBITS = 1
    SYMTAB = 2
    STRTAB = 3
    RELA = 4
    HASH = 5
    DYNAMIC = 6
    NOTE = 7
    NOBITS = 8
    REL = 9
    SHLIB = 10
    DYNSYM = 11
    NUM = 12
    LOPROC = 0x70000000
    HIPROC = 0x7FFFFFFF
    LOUSER = 0x80000000
    HIUSER = 0xFFFFFFFF
