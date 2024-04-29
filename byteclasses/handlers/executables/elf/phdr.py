"""Elf Program Header Class.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from enum import IntEnum

from ....types.collections import member, structure
from ....types.primitives.byte_enum import ByteEnum
from ....types.primitives.generics import BitField32, BitPos
from ....types.primitives.integers import Ptr32, Ptr64, UInt32, UInt64

__all__ = [
    "PHdr32",
    "PHdr64",
]


class PBitField32(BitField32):
    """Elf PHdr BitField."""

    execute = BitPos(0)  # 0x1
    write = BitPos(1)  # 0x2
    read = BitPos(2)  # 0x4


@structure
class PHdr32:
    """32-bit Elf Program Header."""

    p_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(PHdrType, UInt32, byte_order=byte_order))
    p_offset: Ptr32
    p_vaddr: Ptr32
    p_paddr: Ptr32
    p_filesz: UInt32
    p_memsz: UInt32
    p_flags: PBitField32
    p_align: UInt32


@structure
class PHdr64:
    """64-bit Elf Program Header."""

    p_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(PHdrType, UInt32, byte_order=byte_order))
    p_flags: PBitField32
    p_offset: Ptr64
    p_vaddr: Ptr64
    p_paddr: Ptr64
    p_filesz: UInt64
    p_memsz: UInt64
    p_align: UInt64


class PHdrType(IntEnum):
    """Elf Program Hdr Types."""

    NULL = 0
    LOAD = 1
    DYNAMIC = 2
    INTERP = 3
    NOTE = 4
    SHLIB = 5
    PHDR = 6
    TLS = 7  # Thread local storage segment
    LOOS = 0x60000000  # OS-specific
    HIOS = 0x6FFFFFFF  # OS-specific
    LOPROC = 0x70000000
    HIPROC = 0x7FFFFFFF
    GNU_EH_FRAME = LOOS + 0x474E550
    GNU_STACK = LOOS + 0x474E551
    GNU_RELRO = LOOS + 0x474E552
    GNU_PROPERTY = LOOS + 0x474E553
