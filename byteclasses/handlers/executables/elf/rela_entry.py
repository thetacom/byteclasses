"""Elf Relocation Addend Entry Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from ....types.collections import structure
from ....types.primitives.integers import UInt32, UInt64

__all__ = [
    "RelAEntry32",
    "RelAEntry64",
]


@structure
class RelAEntry32:
    """32-bit Elf Relocation Addend Entry."""

    r_offset: UInt32
    r_info: UInt32
    r_addend: UInt32


@structure
class RelAEntry64:
    """64-bit Elf Relocation Addend Entry."""

    r_offset: UInt64
    r_info: UInt64
    r_addend: UInt32
