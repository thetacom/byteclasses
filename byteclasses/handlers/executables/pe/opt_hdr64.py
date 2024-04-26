"""PE Optional Header Class."""

# pylint: disable=R0801
from ....types.collections import ByteArray, member, structure
from ....types.primitives.bitfield import BitField16, BitField32
from ....types.primitives.generics import Word
from ....types.primitives.integers import Ptr32, Ptr64, UInt8, UInt16, UInt32, UInt64
from .data_dir import DataDir

__all__ = ["OptHdr64"]

NUM_DIR_ENT = 16


@structure(packed=True)
class OptHdr64:
    """PE 64-bit Optional Header Class.

    typedef struct _IMAGE_OPTIONAL_HEADER64 {
        WORD        Magic;
        BYTE        MajorLinkerVersion;
        BYTE        MinorLinkerVersion;
        DWORD       SizeOfCode;
        DWORD       SizeOfInitializedData;
        DWORD       SizeOfUninitializedData;
        DWORD       AddressOfEntryPoint;
        DWORD       BaseOfCode;
        ULONGLONG   ImageBase;
        DWORD       SectionAlignment;
        DWORD       FileAlignment;
        WORD        MajorOperatingSystemVersion;
        WORD        MinorOperatingSystemVersion;
        WORD        MajorImageVersion;
        WORD        MinorImageVersion;
        WORD        MajorSubsystemVersion;
        WORD        MinorSubsystemVersion;
        DWORD       Win32VersionValue;
        DWORD       SizeOfImage;
        DWORD       SizeOfHeaders;
        DWORD       CheckSum;
        WORD        Subsystem;
        WORD        DllCharacteristics;
        ULONGLONG   SizeOfStackReserve;
        ULONGLONG   SizeOfStackCommit;
        ULONGLONG   SizeOfHeapReserve;
        ULONGLONG   SizeOfHeapCommit;
        DWORD       LoaderFlags;
        DWORD       NumberOfRvaAndSizes;
        IMAGE_DATA_DIRECTORY DataDirectory[DIRECTORY_ENTRIES_NUM];
    } IMAGE_OPTIONAL_HEADER64;
    """

    magic: Word
    major_linker_ver: UInt8
    minor_linker_ver: UInt8
    size_of_code: UInt32
    size_of_init_data: UInt32
    size_of_uninit_data: UInt32
    addr_of_entrypoint: Ptr32
    base_of_code: Ptr32
    # NT Additional Fields
    image_base: Ptr64
    section_alignment: UInt32
    file_alignment: UInt32
    major_os_ver: UInt16
    minor_os_ver: UInt16
    major_img_ver: UInt16
    minor_img_ver: UInt16
    major_subsys_ver: UInt16
    minor_subsys_ver: UInt16
    win32_ver_val: UInt32
    size_of_img: UInt32
    size_of_hdrs: UInt32
    checksum: UInt32
    subsystem: UInt16
    dll_characteristics: BitField16
    size_of_stack_reserve: UInt64
    size_of_stack_commit: UInt64
    size_of_heap_reserve: UInt64
    size_of_heap_commit: UInt64
    loader_flags: BitField32
    num_of_rva_and_sizes: UInt32
    data_directory: ByteArray = member(factory=lambda byte_order: ByteArray(NUM_DIR_ENT, DataDir))  # type: ignore
