"""PE File Header Class.

length: 20 bytes

typedef struct _IMAGE_FILE_HEADER {
    WORD    Machine;
    WORD    NumberOfSections;
    DWORD   TimeDateStamp;
    DWORD   PointerToSymbolTable;
    DWORD   NumberOfSymbols;
    WORD    SizeOfOptionalHeader;
    WORD    Characteristics;
} IMAGE_FILE_HEADER, *PIMAGE_FILE_HEADER;
"""

from ....types.collections import structure
from ....types.primitives.integers import Ptr32, UInt16, UInt32

__all__ = [
    "FileHdr",
]


@structure(packed=True)
class FileHdr:
    """PE File Header Class."""

    machine: UInt16
    number_of_sections: UInt16
    time_datestamp: UInt32
    ptr_to_sym_tbl: Ptr32
    num_of_sym: UInt32
    size_of_opt_hdr: UInt16
    characteristics: UInt16
