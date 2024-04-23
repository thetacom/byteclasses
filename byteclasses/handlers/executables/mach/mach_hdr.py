"""Pre-defined MacOS Executable Header Class.

[OS X ABI Mach-O File Format Reference](https://github.com/aidansteele/osx-abi-macho-file-format-reference)
[llvm::MachO Namespace Reference](https://llvm.org/doxygen/namespacellvm_1_1MachO.html)
"""

from enum import IntEnum

from ....types.collections import structure
from ....types.primitives.bitfield import BitField32, mask2bitpos
from ....types.primitives.generics import DWord
from ....types.primitives.integers import Int32, UInt32

__all__ = [
    "MachFlags32",
    "MachHdr32",
    "MachHdr64",
    "MH_MAGIC32",
    "MH_MAGIC64",
]

MH_MAGIC32 = b"\xce\xfa\xed\xfe"  # 0xFEEDFACE
MH_MAGIC64 = b"\xcf\xfa\xed\xfe"  # 0xFEEDFACF


class CPUArchMask(IntEnum):
    """Mach-O CPU Archtecture Masks."""

    ARCH_MASK = 0xFF000000
    ARCH_ABI64 = 0x01000000
    ARCH_ABI64_32 = 0x02000000


class CPUType(IntEnum):
    """Mach-O CPU Types."""

    ANY = -1
    X86 = 7
    I386 = X86
    X86_64 = X86 | CPUArchMask.ARCH_ABI64
    MC98000 = 10
    ARM = 12
    ARM64 = ARM | CPUArchMask.ARCH_ABI64
    ARM64_32 = ARM | CPUArchMask.ARCH_ABI64_32
    SPARC = 14
    POWERPC = 18
    POWERPC64 = POWERPC | CPUArchMask.ARCH_ABI64


class CPUSubtypeMask(IntEnum):
    """Mach-O CPU Subtype Masks."""

    MASK = 0xFF000000
    LIB64 = 0x80000000
    MULTIPLE = ~0


class X86Subtype(IntEnum):
    """Mach-O CPU X86 Subtypes."""

    I386_ALL = 3
    I386 = 3
    I486 = 4
    I486SX = 0x84
    I586 = 5
    PENT = I586
    PENTPRO = 0x16
    PENTII_M3 = 0x36
    PENTII_M5 = 0x56
    CELERON = 0x67
    CELERON_MOBILE = 0x77
    PENTIUM_3 = 0x08
    PENTIUM_3_M = 0x18
    PENTIUM_3_XEON = 0x28
    PENTIUM_M = 0x09
    PENTIUM_4 = 0x0A
    PENTIUM_4_M = 0x1A
    ITANIUM = 0x0B
    ITANIUM_2 = 0x1B
    XEON = 0x0C
    XEON_MP = 0x1C
    X86_ALL = 3
    X86_64_ALL = 3
    X86_ARCH1 = 4
    X86_64_H = 8


class ArmSubtype(IntEnum):
    """Mach-O CPU Arm Subtypes."""

    ARM_ALL = 0
    ARM_V4T = 5
    ARM_V6 = 6
    ARM_V5 = 7
    ARM_V5TEJ = 7
    ARM_XSCALE = 8
    ARM_V7 = 9
    ARM_V7S = 11
    ARM_V7K = 12
    ARM_V6M = 14
    ARM_V7M = 15
    ARM_V7EM = 16


class Arm64Subtype(IntEnum):
    """Mach-O CPU Arm64 Subtypes."""

    ARM64_ALL = 0
    ARM64_V8 = 1
    ARM64E = 2


CPU_MAP = {
    CPUType.X86: X86Subtype,
    CPUType.ARM: ArmSubtype,
    CPUType.ARM64: Arm64Subtype,
}


class MachFlags32(BitField32):
    """Mach-O Flags 32-bit BitField."""

    NOUNDEFS = mask2bitpos(0x00000001)
    INCRLINK = mask2bitpos(0x00000002)
    DYLDLINK = mask2bitpos(0x00000004)
    BINDATLOAD = mask2bitpos(0x00000008)
    PREBOUND = mask2bitpos(0x00000010)
    SPLIT_SEGS = mask2bitpos(0x00000020)
    LAZY_INIT = mask2bitpos(0x00000040)
    TWOLEVEL = mask2bitpos(0x00000080)
    FORCE_FLAT = mask2bitpos(0x00000100)
    NOMULTIDEFS = mask2bitpos(0x00000200)
    NOFIXPREBINDING = mask2bitpos(0x00000400)
    PREBINDABLE = mask2bitpos(0x00000800)
    ALLMODSBOUND = mask2bitpos(0x00001000)
    SUBSECTIONS_VIA_SYMBOLS = mask2bitpos(0x00002000)
    CANONICAL = mask2bitpos(0x00004000)
    WEAK_DEFINES = mask2bitpos(0x00008000)
    BINDS_TO_WEAK = mask2bitpos(0x00010000)
    ALLOW_STACK_EXECUTION = mask2bitpos(0x00020000)
    ROOT_SAFE = mask2bitpos(0x00040000)
    SETUID_SAFE = mask2bitpos(0x00080000)
    NO_REEXPORTED_DYLIBS = mask2bitpos(0x00100000)
    PIE = mask2bitpos(0x00200000)
    DEAD_STRIPPABLE_DYLIB = mask2bitpos(0x00400000)
    HAS_TLV_DESCRIPTORS = mask2bitpos(0x00800000)
    NO_HEAP_EXECUTION = mask2bitpos(0x01000000)
    APP_EXTENSION_SAFE = mask2bitpos(0x02000000)
    NLIST_OUTOFSYNC_WITH_DYLDINFO = mask2bitpos(0x04000000)
    SIM_SUPPORT = mask2bitpos(0x08000000)
    DYLIB_IN_CACHE = mask2bitpos(0x80000000)


@structure
class MachHdr32:
    """32-bit MacOS Executable."""

    magic: DWord
    cputype: Int32
    cpusubtype: Int32
    filetype: UInt32
    ncmds: UInt32
    sizeofcmds: UInt32
    flags: MachFlags32


@structure
class MachHdr64:
    """64-bit MacOS Executable."""

    magic: DWord
    cputype: Int32
    cpusubtype: Int32
    filetype: UInt32
    ncmds: UInt32
    sizeofcmds: UInt32
    flags: MachFlags32
    reserved: UInt32
