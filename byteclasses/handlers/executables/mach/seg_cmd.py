"""Mach-O Segment Command Module."""

from ....types import BitField32, Int32, Ptr32, Ptr64, String, UInt32, UInt64, member, structure

__all__ = [
    "SegCmd32",
    "SegCmd64",
]


class SegFlags32(BitField32):
    """Mach-O Segment Flags 32-bit BitField."""


@structure
class SegCmd32:
    """Mach-O 32-bit Segment Command."""

    cmd: UInt32
    cmdsize: UInt32
    segname: String = member(factory=lambda byte_order: String(16))  # type: ignore
    vmaddr: Ptr32
    vmsize: UInt32
    fileoff: Ptr32
    filesize: UInt32
    maxprot: Int32
    initprot: Int32
    nsects: UInt32
    flags: SegFlags32


@structure
class SegCmd64:
    """Mach-O 64-bit Segment Command."""

    cmd: UInt32
    cmdsize: UInt32
    segname: String = member(factory=lambda byte_order: String(16))  # type: ignore
    vmaddr: Ptr64
    vmsize: UInt64
    fileoff: Ptr64
    filesize: UInt64
    maxprot: Int32
    initprot: Int32
    nsects: UInt32
    flags: SegFlags32
