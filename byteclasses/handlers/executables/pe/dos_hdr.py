"""Legacy DOS Header Class."""

from ....types.collections import ByteArray, member, structure
from ....types.primitives.generics import Word
from ....types.primitives.integers import Ptr32, UInt16

__all__ = [
    "DOSHdr",
]


@structure(packed=True)
class DOSHdr:
    """DOS Executable Header Class.

    typedef struct _IMAGE_DOS_HEADER {
        WORD   e_magic;
        WORD   e_cblp;
        WORD   e_cp;
        WORD   e_crlc;
        WORD   e_cparhdr;
        WORD   e_minalloc;
        WORD   e_maxalloc;
        WORD   e_ss;
        WORD   e_sp;
        WORD   e_csum;
        WORD   e_ip;
        WORD   e_cs;
        WORD   e_lfarlc;
        WORD   e_ovno;
        WORD   e_res[4];
        WORD   e_oemid;
        WORD   e_oeminfo;
        WORD   e_res2[10];
        LONG   e_lfanew;
    } IMAGE_DOS_HEADER
    """

    e_magic: Word  # Magic number
    e_cblp: UInt16  # Bytes on last page of file
    e_cp: UInt16  # Pages in file
    e_crlc: UInt16  # Relocations
    e_cparhdr: UInt16  # Size of header in paragraphs
    e_minalloc: UInt16  # Minimum extra paragraphs needed
    e_maxalloc: UInt16  # Maximum extra paragraphs needed
    e_ss: UInt16  # Initial (relative) SS value
    e_sp: UInt16  # Initial SP value
    e_csum: UInt16  # Checksum
    e_ip: UInt16  # Initial IP value
    e_cs: UInt16  # Initial (relative) CS value
    e_lfarlc: UInt16  # File address of relocation table
    e_ovno: UInt16  # Overlay number
    e_res: ByteArray = member(factory=lambda byte_order: ByteArray(4, UInt16))  # type: ignore
    e_oemid: UInt16  # OEM identifier (for e_oeminfo)
    e_oeminfo: UInt16  # OEM information; e_oemid specific
    e_res2: ByteArray = member(factory=lambda byte_order: ByteArray(10, UInt16))  # type: ignore
    e_lfanew: Ptr32  # File address of new exe header
