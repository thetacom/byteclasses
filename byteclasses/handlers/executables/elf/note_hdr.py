"""Elf Note Header Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from enum import IntEnum

from ....types.collections import member, structure
from ....types.primitives.byte_enum import ByteEnum
from ....types.primitives.integers import UInt32, UInt64

__all__ = [
    "NoteHdr32",
    "NoteHdr64",
    "NoteType",
]


@structure
class NoteHdr32:
    """32-bit Elf Note Header."""

    n_namesz: UInt32
    n_descsz: UInt32
    n_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(NoteType, UInt32, byte_order=byte_order))


@structure
class NoteHdr64:
    """64-bit Elf Note Header."""

    n_namesz: UInt64
    n_descsz: UInt64
    n_type: ByteEnum = member(factory=lambda byte_order: ByteEnum(NoteType, UInt64, byte_order=byte_order))


class NoteType(IntEnum):
    """Elf Note Types."""

    PRSTATUS = 1
    PRFPREG = 2
    PRPSINFO = 3
    TASKSTRUCT = 4
    AUXV = 6
    SIGINFO = 0x53494749
    FILE = 0x46494C45
    PRXFPREG = 0x46E62B7F  #  copied from gdb5.1/include/elf/common.h
    PPC_VMX = 0x100  #  PowerPC Altivec/VMX registers
    PPC_SPE = 0x101  #  PowerPC SPE/EVR registers
    PPC_VSX = 0x102  #  PowerPC VSX registers
    PPC_TAR = 0x103  #  Target Address Register
    PPC_PPR = 0x104  #  Program Priority Register
    PPC_DSCR = 0x105  #  Data Stream Control Register
    PPC_EBB = 0x106  #  Event Based Branch Registers
    PPC_PMU = 0x107  #  Performance Monitor Registers
    PPC_TM_CGPR = 0x108  #  TM checkpointed GPR Registers
    PPC_TM_CFPR = 0x109  #  TM checkpointed FPR Registers
    PPC_TM_CVMX = 0x10A  #  TM checkpointed VMX Registers
    PPC_TM_CVSX = 0x10B  #  TM checkpointed VSX Registers
    PPC_TM_SPR = 0x10C  #  TM Special Purpose Registers
    PPC_TM_CTAR = 0x10D  #  TM checkpointed Target Address Register
    PPC_TM_CPPR = 0x10E  #  TM checkpointed Program Priority Register
    PPC_TM_CDSCR = 0x10F  #  TM checkpointed Data Stream Control Register
    PPC_PKEY = 0x110  #  Memory Protection Keys registers
    PPC_DEXCR = 0x111  #  PowerPC DEXCR registers
    PPC_HASHKEYR = 0x112  #  PowerPC HASHKEYR register
    I386_TLS = 0x200  #  i386 TLS slots (struct user_desc)
    I386_IOPERM = 0x201  #  x86 io permission bitmap (1=deny)
    X86_XSTATE = 0x202  #  x86 extended state using xsave
    X86_SHSTK = 0x204  #  x86 SHSTK state
    S390_HIGH_GPRS = 0x300  #  s390 upper register halves
    S390_TIMER = 0x301  #  s390 timer register
    S390_TODCMP = 0x302  #  s390 TOD clock comparator register
    S390_TODPREG = 0x303  #  s390 TOD programmable register
    S390_CTRS = 0x304  #  s390 control registers
    S390_PREFIX = 0x305  #  s390 prefix register
    S390_LAST_BREAK = 0x306  #  s390 breaking event address
    S390_SYSTEM_CALL = 0x307  #  s390 system call restart data
    S390_TDB = 0x308  #  s390 transaction diagnostic block
    S390_VXRS_LOW = 0x309  #  s390 vector registers 0-15 upper half
    S390_VXRS_HIGH = 0x30A  #  s390 vector registers 16-31
    S390_GS_CB = 0x30B  #  s390 guarded storage registers
    S390_GS_BC = 0x30C  #  s390 guarded storage broadcast control block
    S390_RI_CB = 0x30D  #  s390 runtime instrumentation
    S390_PV_CPU_DATA = 0x30E  #  s390 protvirt cpu dump data
    ARM_VFP = 0x400  #  ARM VFP/NEON registers
    ARM_TLS = 0x401  #  ARM TLS register
    ARM_HW_BREAK = 0x402  #  ARM hardware breakpoint registers
    ARM_HW_WATCH = 0x403  #  ARM hardware watchpoint registers
    ARM_SYSTEM_CALL = 0x404  #  ARM system call number
    ARM_SVE = 0x405  #  ARM Scalable Vector Extension registers
    ARM_PAC_MASK = 0x406  #  ARM pointer authentication code masks
    ARM_PACA_KEYS = 0x407  #  ARM pointer authentication address keys
    ARM_PACG_KEYS = 0x408  #  ARM pointer authentication generic key
    ARM_TAGGED_ADDR_CTRL = 0x409  #  arm64 tagged address control (prctl())
    ARM_PAC_ENABLED_KEYS = 0x40A  #  arm64 ptr auth enabled keys (prctl())
    ARM_SSVE = 0x40B  #  ARM Streaming SVE registers
    ARM_ZA = 0x40C  #  ARM SME ZA registers
    ARM_ZT = 0x40D  #  ARM SME ZT registers
    ARM_FPMR = 0x40E  #  ARM floating point mode register
    ARC_V2 = 0x600  #  ARCv2 accumulator/extra registers
    VMCOREDD = 0x700  #  Vmcore Device Dump Note
    MIPS_DSP = 0x800  #  MIPS DSP ASE registers
    MIPS_FP_MODE = 0x801  #  MIPS floating-point mode
    MIPS_MSA = 0x802  #  MIPS SIMD registers
    RISCV_CSR = 0x900  #  RISC-V Control and Status Registers
    RISCV_VECTOR = 0x901  #  RISC-V vector registers
    LOONGARCH_CPUCFG = 0xA00  #  LoongArch CPU config registers
    LOONGARCH_CSR = 0xA01  #  LoongArch control and status registers
    LOONGARCH_LSX = 0xA02  #  LoongArch Loongson SIMD Extension registers
    LOONGARCH_LASX = 0xA03  #  LoongArch Loongson Advanced SIMD Extension registers
    LOONGARCH_LBT = 0xA04  #  LoongArch Loongson Binary Translation registers
    LOONGARCH_HW_BREAK = 0xA05  #  LoongArch hardware breakpoint registers
    LOONGARCH_HW_WATCH = 0xA06  #  LoongArch hardware watchpoint registers
    GNU_PROPERTY_TYPE_0 = 5
