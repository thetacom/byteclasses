"""Elf Symbol Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from ....types.collections import structure
from ....types.primitives.characters import UChar
from ....types.primitives.integers import UInt16, UInt32, UInt64

__all__ = [
    "SymEntry32",
    "SymEntry64",
]


@structure
class SymEntry32:
    """32-bit Elf Symbol Entry."""

    st_name: UInt32
    st_value: UInt32
    st_size: UInt32
    st_info: UChar
    st_other: UChar
    st_shndx: UInt16


@structure
class SymEntry64:
    """64-bit Elf Symbol."""

    st_name: UInt32
    st_info: UChar
    st_other: UChar
    st_shndx: UInt16
    st_value: UInt64
    st_size: UInt64
