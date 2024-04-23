"""Elf Note Header Classes.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from enum import IntEnum

from ....types.collections import structure
from ....types.primitives.integers import UInt32, UInt64

__all__ = [
    "NoteHdr32",
    "NoteHdr64",
    "ElfNoteType",
]


@structure
class NoteHdr32:
    """32-bit Elf Note Header."""

    n_namesz: UInt32
    n_descsz: UInt32
    n_type: UInt32


@structure
class NoteHdr64:
    """64-bit Elf Note Header."""

    n_namesz: UInt64
    n_descsz: UInt64
    n_type: UInt64


class ElfNoteType(IntEnum):
    """Elf Note Types."""

    NT_PRSTATUS = 1
    NT_PRFPREG = 2
    NT_PRPSINFO = 3
    NT_TASKSTRUCT = 4
    NT_AUXV = 6
    NT_SIGINFO = 0x53494749
    NT_FILE = 0x46494C45
    NT_PRXFPREG = 0x46E62B7F  #  copied from gdb5.1/include/elf/common.h
    NT_PPC_VMX = 0x100  #  PowerPC Altivec/VMX registers
    NT_PPC_SPE = 0x101  #  PowerPC SPE/EVR registers
    NT_PPC_VSX = 0x102  #  PowerPC VSX registers
    NT_PPC_TAR = 0x103  #  Target Address Register
    NT_PPC_PPR = 0x104  #  Program Priority Register
    NT_PPC_DSCR = 0x105  #  Data Stream Control Register
    NT_PPC_EBB = 0x106  #  Event Based Branch Registers
    NT_PPC_PMU = 0x107  #  Performance Monitor Registers
    NT_PPC_TM_CGPR = 0x108  #  TM checkpointed GPR Registers
    NT_PPC_TM_CFPR = 0x109  #  TM checkpointed FPR Registers
    NT_PPC_TM_CVMX = 0x10A  #  TM checkpointed VMX Registers
    NT_PPC_TM_CVSX = 0x10B  #  TM checkpointed VSX Registers
    NT_PPC_TM_SPR = 0x10C  #  TM Special Purpose Registers
    NT_PPC_TM_CTAR = 0x10D  #  TM checkpointed Target Address Register
    NT_PPC_TM_CPPR = 0x10E  #  TM checkpointed Program Priority Register
    NT_PPC_TM_CDSCR = 0x10F  #  TM checkpointed Data Stream Control Register
    NT_PPC_PKEY = 0x110  #  Memory Protection Keys registers
    NT_PPC_DEXCR = 0x111  #  PowerPC DEXCR registers
    NT_PPC_HASHKEYR = 0x112  #  PowerPC HASHKEYR register
    NT_386_TLS = 0x200  #  i386 TLS slots (struct user_desc)
    NT_386_IOPERM = 0x201  #  x86 io permission bitmap (1=deny)
    NT_X86_XSTATE = 0x202  #  x86 extended state using xsave
    NT_X86_SHSTK = 0x204  #  x86 SHSTK state
    NT_S390_HIGH_GPRS = 0x300  #  s390 upper register halves
    NT_S390_TIMER = 0x301  #  s390 timer register
    NT_S390_TODCMP = 0x302  #  s390 TOD clock comparator register
    NT_S390_TODPREG = 0x303  #  s390 TOD programmable register
    NT_S390_CTRS = 0x304  #  s390 control registers
    NT_S390_PREFIX = 0x305  #  s390 prefix register
    NT_S390_LAST_BREAK = 0x306  #  s390 breaking event address
    NT_S390_SYSTEM_CALL = 0x307  #  s390 system call restart data
    NT_S390_TDB = 0x308  #  s390 transaction diagnostic block
    NT_S390_VXRS_LOW = 0x309  #  s390 vector registers 0-15 upper half
    NT_S390_VXRS_HIGH = 0x30A  #  s390 vector registers 16-31
    NT_S390_GS_CB = 0x30B  #  s390 guarded storage registers
    NT_S390_GS_BC = 0x30C  #  s390 guarded storage broadcast control block
    NT_S390_RI_CB = 0x30D  #  s390 runtime instrumentation
    NT_S390_PV_CPU_DATA = 0x30E  #  s390 protvirt cpu dump data
    NT_ARM_VFP = 0x400  #  ARM VFP/NEON registers
    NT_ARM_TLS = 0x401  #  ARM TLS register
    NT_ARM_HW_BREAK = 0x402  #  ARM hardware breakpoint registers
    NT_ARM_HW_WATCH = 0x403  #  ARM hardware watchpoint registers
    NT_ARM_SYSTEM_CALL = 0x404  #  ARM system call number
    NT_ARM_SVE = 0x405  #  ARM Scalable Vector Extension registers
    NT_ARM_PAC_MASK = 0x406  #  ARM pointer authentication code masks
    NT_ARM_PACA_KEYS = 0x407  #  ARM pointer authentication address keys
    NT_ARM_PACG_KEYS = 0x408  #  ARM pointer authentication generic key
    NT_ARM_TAGGED_ADDR_CTRL = 0x409  #  arm64 tagged address control (prctl())
    NT_ARM_PAC_ENABLED_KEYS = 0x40A  #  arm64 ptr auth enabled keys (prctl())
    NT_ARM_SSVE = 0x40B  #  ARM Streaming SVE registers
    NT_ARM_ZA = 0x40C  #  ARM SME ZA registers
    NT_ARM_ZT = 0x40D  #  ARM SME ZT registers
    NT_ARM_FPMR = 0x40E  #  ARM floating point mode register
    NT_ARC_V2 = 0x600  #  ARCv2 accumulator/extra registers
    NT_VMCOREDD = 0x700  #  Vmcore Device Dump Note
    NT_MIPS_DSP = 0x800  #  MIPS DSP ASE registers
    NT_MIPS_FP_MODE = 0x801  #  MIPS floating-point mode
    NT_MIPS_MSA = 0x802  #  MIPS SIMD registers
    NT_RISCV_CSR = 0x900  #  RISC-V Control and Status Registers
    NT_RISCV_VECTOR = 0x901  #  RISC-V vector registers
    NT_LOONGARCH_CPUCFG = 0xA00  #  LoongArch CPU config registers
    NT_LOONGARCH_CSR = 0xA01  #  LoongArch control and status registers
    NT_LOONGARCH_LSX = 0xA02  #  LoongArch Loongson SIMD Extension registers
    NT_LOONGARCH_LASX = 0xA03  #  LoongArch Loongson Advanced SIMD Extension registers
    NT_LOONGARCH_LBT = 0xA04  #  LoongArch Loongson Binary Translation registers
    NT_LOONGARCH_HW_BREAK = 0xA05  #  LoongArch hardware breakpoint registers
    NT_LOONGARCH_HW_WATCH = 0xA06  #  LoongArch hardware watchpoint registers
    NT_GNU_PROPERTY_TYPE_0 = 5
