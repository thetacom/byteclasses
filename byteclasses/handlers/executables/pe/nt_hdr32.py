"""Windows NT 32-bit executable header class.."""

from ....types.collections import structure
from ....types.primitives.generics import DWord
from .file_hdr import FileHdr
from .opt_hdr32 import OptHdr32

__all__ = ["NTHdr32"]


@structure(packed=True)
class NTHdr32:
    """32-bit Windows Executable Header Class.

    typedef struct _IMAGE_NT_HEADERS {
        DWORD Signature;
        IMAGE_FILE_HEADER FileHeader;
        IMAGE_OPTIONAL_HEADER32 OptionalHeader;
    } IMAGE_NT_HEADERS32;
    """

    signature: DWord
    file_hdr: FileHdr
    opt_hdr: OptHdr32
