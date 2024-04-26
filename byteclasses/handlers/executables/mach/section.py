"""Mach-O Section Module.

[llvm::MachO Namespace Reference](https://llvm.org/doxygen/namespacellvm_1_1MachO.html)
"""

from ....types.collections import String, member, structure
from ....types.primitives.generics import BitField32
from ....types.primitives.integers import Ptr32, Ptr64, UInt32, UInt64

__all__ = [
    "Section32",
    "Section64",
]


class SecFlags32(BitField32):
    """Mach-O Section Flags 32-bit BitField."""


@structure
class Section32:
    """Mach-O 32-bit Section.

    [section](https://developer.apple.com/documentation/kernel/section/)
    """

    sectname: String = member(factory=lambda byte_order: String(16))  # type: ignore
    segname: String = member(factory=lambda byte_order: String(16))  # type: ignore
    addr: Ptr32
    size: UInt32
    offset: Ptr32
    align: UInt32
    reloff: UInt32
    nreloc: UInt32
    flags: SecFlags32
    reserved1: UInt32
    reserved2: UInt32


@structure
class Section64:
    """Mach-O 64-bit Section.

    [section_64](https://developer.apple.com/documentation/kernel/section_64/)
    """

    sectname: String = member(factory=lambda byte_order: String(16))  # type: ignore
    segname: String = member(factory=lambda byte_order: String(16))  # type: ignore
    addr: Ptr64
    size: UInt64
    offset: Ptr32
    align: UInt32
    reloff: UInt32
    nreloc: UInt32
    flags: SecFlags32
    reserved1: UInt32
    reserved2: UInt32
    reserved3: UInt32
