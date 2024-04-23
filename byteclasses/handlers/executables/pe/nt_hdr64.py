"""Windows NT 64-bit executable header class.."""

from ....types.collections import structure
from ....types.primitives.generics import DWord
from .file_hdr import FileHdr
from .opt_hdr64 import OptHdr64

__all__ = ["NTHdr64"]


@structure(packed=True)
class NTHdr64:
    """64-bit Windows Executable Header Class.

    typedef struct _IMAGE_NT_HEADERS64 {
        DWORD Signature;
        IMAGE_FILE_HEADER FileHeader;
        IMAGE_OPTIONAL_HEADER64 OptionalHeader;
    } IMAGE_NT_HEADERS64;
    """

    signature: DWord
    file_hdr: FileHdr
    opt_hdr: OptHdr64
