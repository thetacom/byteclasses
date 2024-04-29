"""Elf Executable Header Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from enum import IntEnum

from ....types.collections import String, member, structure
from ....types.primitives.byte_enum import ByteEnum
from ....types.primitives.generics import BitField
from ....types.primitives.integers import Ptr32, Ptr64, UInt16, UInt32

__all__ = [
    "ElfHdr32",
    "ElfHdr64",
    "ElfType",
    "ElfMachine",
    "ElfVersion",
]


class BitField32(BitField):
    """32-bit BitField."""

    byte_length = 4


@structure
class ElfHdr32:
    """32-bit Elf Header Class."""

    e_ident: String = member(factory=lambda byte_order: String(16))  # type: ignore
    e_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(ElfType, UInt16, byte_order=byte_order))
    e_machine: ByteEnum = member(factory=lambda byte_order: ByteEnum(ElfMachine, UInt16, byte_order=byte_order))
    e_version: ByteEnum = member(factory=lambda byte_order: ByteEnum(ElfVersion, UInt32, byte_order=byte_order))
    e_entry: Ptr32
    e_phoff: Ptr32
    e_shoff: Ptr32
    e_flags: BitField32
    e_ehsize: UInt16
    e_phentsize: UInt16
    e_phnum: UInt16
    e_shentsize: UInt16
    e_shnum: UInt16
    e_shstrndx: UInt16


@structure
class ElfHdr64:
    """64-bit Elf Header Class."""

    e_ident: String = member(factory=lambda byte_order: String(16))  # type: ignore
    e_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(ElfType, UInt16, byte_order=byte_order))
    e_machine: ByteEnum = member(factory=lambda byte_order: ByteEnum(ElfMachine, UInt16, byte_order=byte_order))
    e_version: ByteEnum = member(factory=lambda byte_order: ByteEnum(ElfVersion, UInt32, byte_order=byte_order))
    e_entry: Ptr64
    e_phoff: Ptr64
    e_shoff: Ptr64
    e_flags: BitField32
    e_ehsize: UInt16
    e_phentsize: UInt16
    e_phnum: UInt16
    e_shentsize: UInt16
    e_shnum: UInt16
    e_shstrndx: UInt16


class ElfType(IntEnum):
    """Elf Types."""

    NONE = 0
    REL = 1
    EXEC = 2
    DYN = 3
    CORE = 4
    LOPROC = 0xFF00
    HIPROC = 0xFFFF


class ElfMachine(IntEnum):
    """Elf Machine Types."""

    NONE = 0
    M32 = 1
    SPARC = 2
    I386 = 3
    M68K = 4
    M88K = 5
    I486 = 6  # Perhaps disused
    I860 = 7
    MIPS = 8  # MIPS R3000 (officially, big-endian only)
    MIPS_RS3_LE = 10  # MIPS R3000 little-endian
    MIPS_RS4_BE = 10  # MIPS R4000 big-endian
    PARISC = 15  # HPPA
    SPARC32PLUS = 18  # Sun's "v8plus"
    PPC = 20  # PowerPC
    PPC64 = 21  # PowerPC64
    SPU = 23  # Cell BE SPU
    ARM = 40  # ARM 32 bit
    SH = 42  # SuperH
    SPARCV9 = 43  # SPARC v9 64-bit
    H8_300 = 46  # Renesas H8/300
    IA_64 = 50  # HP/Intel IA-64
    X86_64 = 62  # AMD x86-64
    S390 = 22  # IBM S/390
    CRIS = 76  # Axis Communications 32-bit embedded processor
    M32R = 88  # Renesas M32R
    MN10300 = 89  # Panasonic/MEI MN10300, AM33
    OPENRISC = 92  # OpenRISC 32-bit embedded processor
    ARCOMPACT = 93  # ARCompact processor
    XTENSA = 94  # Tensilica Xtensa Architecture
    BLACKFIN = 106  # ADI Blackfin Processor
    UNICORE = 110  # UniCore-32
    ALTERA_NIOS2 = 113  # Altera Nios II soft-core processor
    TI_C6000 = 140  # TI C6X DSPs
    HEXAGON = 164  # QUALCOMM Hexagon
    NDS32 = 167  # Andes Technology compact code size
    AARCH64 = 183  # ARM 64 bit
    TILEPRO = 188  # Tilera TILEPro
    MICROBLAZE = 189  # Xilinx MicroBlaze
    TILEGX = 191  # Tilera TILE-Gx
    ARCV2 = 195  # ARCv2 Cores
    RISCV = 243  # RISC-V
    BPF = 247  # Linux BPF - in-kernel virtual machine
    CSKY = 252  # C-SKY
    LOONGARCH = 258  # LoongArch
    FRV = 0x5441  # Fujitsu FR-V
    ALPHA = 0x9026
    CYGNUS_M32R = 0x9041
    S390_OLD = 0xA390
    CYGNUS_MN10300 = 0xBEEF


class ElfVersion(IntEnum):
    """Elf Versions."""

    NONE = 0  # e_version, EI_VERSION
    CURRENT = 1
    NUM = 2
