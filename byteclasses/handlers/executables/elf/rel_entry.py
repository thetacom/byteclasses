"""Elf Relocation Entry Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from ....types.collections import structure
from ....types.primitives.integers import UInt32, UInt64

__all__ = [
    "RelEntry32",
    "RelEntry64",
]


@structure
class RelEntry32:
    """32-bit Elf Relocation Entry."""

    r_offset: UInt32
    r_info: UInt32


@structure
class RelEntry64:
    """64-bit Elf Relocation Entry."""

    r_offset: UInt64
    r_info: UInt64
