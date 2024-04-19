"""Elf Dynamic Entry Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from ....types.collections import structure, union
from ....types.primitives.integers import Int32, Int64, UInt32, UInt64

__all__ = [
    "DynEntry32",
    "DynEntry64",
]


@union
class DUn32:
    """32-bit Elf Dynamic Entry Union."""

    d_val: UInt32
    d_ptr: UInt32


@structure
class DynEntry32:
    """32-bit Elf Dynamic Entry."""

    d_tag: Int32
    d_un: DUn32


@union
class DUn64:
    """64-bit Elf Dynamic Entry Union."""

    d_val: UInt64
    d_ptr: UInt64


@structure
class DynEntry64:
    """64-bit Elf Dynamic Entry."""

    d_tag: Int64
    d_un: DUn64
