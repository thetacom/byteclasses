"""Pre-defined Unix/Linux Executable Handler Class."""

from enum import IntEnum
from functools import cached_property

from .._data_handler import _DataHandler
from .elf_hdr import Elf32Hdr, Elf32PHdr, Elf32SHdr, Elf64Hdr, Elf64PHdr, Elf64SHdr

__all__ = [
    "Elf32",
    "Elf64",
    "ElfType",
    "ElfDynType",
    "ElfSHType",
    "ElfSHFlag",
    "ElfNoteType",
]


class ElfType(IntEnum):
    """Elf Types."""

    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4
    ET_LOPROC = 0xFF00
    ET_HIPROC = 0xFFFF


class ElfMachine(IntEnum):
    """Elf Machine Types."""

    EM_NONE = 0
    EM_M32 = 1
    EM_SPARC = 2
    EM_386 = 3
    EM_68K = 4
    EM_88K = 5
    EM_486 = 6  # Perhaps disused
    EM_860 = 7
    EM_MIPS = 8  # MIPS R3000 (officially, big-endian only)
    EM_MIPS_RS3_LE = 10  # MIPS R3000 little-endian
    EM_MIPS_RS4_BE = 10  # MIPS R4000 big-endian
    EM_PARISC = 15  # HPPA
    EM_SPARC32PLUS = 18  # Sun's "v8plus"
    EM_PPC = 20  # PowerPC
    EM_PPC64 = 21  # PowerPC64
    EM_SPU = 23  # Cell BE SPU
    EM_ARM = 40  # ARM 32 bit
    EM_SH = 42  # SuperH
    EM_SPARCV9 = 43  # SPARC v9 64-bit
    EM_H8_300 = 46  # Renesas H8/300
    EM_IA_64 = 50  # HP/Intel IA-64
    EM_X86_64 = 62  # AMD x86-64
    EM_S390 = 22  # IBM S/390
    EM_CRIS = 76  # Axis Communications 32-bit embedded processor
    EM_M32R = 88  # Renesas M32R
    EM_MN10300 = 89  # Panasonic/MEI MN10300, AM33
    EM_OPENRISC = 92  # OpenRISC 32-bit embedded processor
    EM_ARCOMPACT = 93  # ARCompact processor
    EM_XTENSA = 94  # Tensilica Xtensa Architecture
    EM_BLACKFIN = 106  # ADI Blackfin Processor
    EM_UNICORE = 110  # UniCore-32
    EM_ALTERA_NIOS2 = 113  # Altera Nios II soft-core processor
    EM_TI_C6000 = 140  # TI C6X DSPs
    EM_HEXAGON = 164  # QUALCOMM Hexagon
    EM_NDS32 = 167  # Andes Technology compact code size
    EM_AARCH64 = 183  # ARM 64 bit
    EM_TILEPRO = 188  # Tilera TILEPro
    EM_MICROBLAZE = 189  # Xilinx MicroBlaze
    EM_TILEGX = 191  # Tilera TILE-Gx
    EM_ARCV2 = 195  # ARCv2 Cores
    EM_RISCV = 243  # RISC-V
    EM_BPF = 247  # Linux BPF - in-kernel virtual machine
    EM_CSKY = 252  # C-SKY
    EM_LOONGARCH = 258  # LoongArch
    EM_FRV = 0x5441  # Fujitsu FR-V
    EM_ALPHA = 0x9026
    EM_CYGNUS_M32R = 0x9041
    EM_S390_OLD = 0xA390
    EM_CYGNUS_MN10300 = 0xBEEF


class ElfVersion(IntEnum):
    """Elf Versions."""

    EV_NONE = 0  # e_version, EI_VERSION
    EV_CURRENT = 1
    EV_NUM = 2


class ElfDynType(IntEnum):
    """Elf Dynamic Section Types."""

    DT_NULL = 0
    DT_NEEDED = 1
    DT_PLTRELSZ = 2
    DT_PLTGOT = 3
    DT_HASH = 4
    DT_STRTAB = 5
    DT_SYMTAB = 6
    DT_RELA = 7
    DT_RELASZ = 8
    DT_RELAENT = 9
    DT_STRSZ = 10
    DT_SYMENT = 11
    DT_INIT = 12
    DT_FINI = 13
    DT_SONAME = 14
    DT_RPATH = 15
    DT_SYMBOLIC = 16
    DT_REL = 17
    DT_RELSZ = 18
    DT_RELENT = 19
    DT_PLTREL = 20
    DT_DEBUG = 21
    DT_TEXTREL = 22
    DT_JMPREL = 23
    DT_ENCODING = 32


class ElfSHType(IntEnum):
    """Elf Section Header Types."""

    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    SHT_SHLIB = 10
    SHT_DYNSYM = 11
    SHT_NUM = 12
    SHT_LOPROC = 0x70000000
    SHT_HIPROC = 0x7FFFFFFF
    SHT_LOUSER = 0x80000000
    SHT_HIUSER = 0xFFFFFFFF


class ElfSHFlag(IntEnum):
    """Elf Section Header Flags."""

    SHF_WRITE = 0x1
    SHF_ALLOC = 0x2
    SHF_EXECINSTR = 0x4
    SHF_RELA_LIVEPATCH = 0x00100000
    SHF_RO_AFTER_INIT = 0x00200000
    SHF_MASKPROC = 0xF0000000


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


class Elf(_DataHandler):
    """Elf Executable Handler.

    Handles 32-bit and 64-bit ELFs.
    """

    def __init__(self, hdr_cls: type[Elf32Hdr | Elf64Hdr], data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize Elf Handler instance."""
        super().__init__(data)
        self._hdr = hdr_cls()
        try:
            self._hdr.attach(memoryview(self._data))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return Elf Executable string."""
        return f"{self.__class__.__name__}(type={self.type})"

    @property
    def hdr(self) -> Elf32Hdr | Elf64Hdr:
        """Return Elf header."""
        return self._hdr

    @property
    def type(self) -> str:
        """Return Elf Type property."""
        try:
            return ElfType(self.hdr.e_type.value).name
        except ValueError:
            return hex(self.hdr.e_type)

    @property
    def machine(self) -> str:
        """Return Elf Machine property."""
        try:
            return ElfMachine(self.hdr.e_machine.value).name
        except ValueError:
            return hex(self.hdr.e_machine)

    @property
    def version(self) -> str:
        """Return Elf Version property."""
        try:
            return ElfVersion(self.hdr.e_version.value).name
        except ValueError:
            return hex(self.hdr.e_version)

    @property
    def flags(self) -> str:
        """Return Elf Flags property."""
        return str(self.hdr.e_flags)


class Elf32(Elf):
    """32-bit Elf Executable Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 32-bit Elf Handler instance."""
        super().__init__(Elf32Hdr, data)

    @property
    def entry(self) -> str:
        """Return Elf Entry property."""
        return f"0x{self.hdr.e_entry.value:08x}"

    @property
    def prog_hdr_offset(self) -> str:
        """Return Elf Program Hdr Offset property."""
        return f"0x{self.hdr.e_phoff.value:08x}"

    @property
    def section_hdr_offset(self) -> str:
        """Return Elf Section Hdr Offset property."""
        return f"0x{self.hdr.e_shoff.value:08x}"

    @cached_property
    def prog_hdr_table(self) -> list[Elf32PHdr]:
        """Returns a list of Elf32 Program Headers."""
        table: list[Elf32PHdr] = []
        start = self.hdr.e_phoff.value
        entry_size = self.hdr.e_phentsize.value
        for _ in range(self.hdr.e_phnum):
            p_hdr = Elf32PHdr()
            p_hdr.attach(self.data[start : start + entry_size])  # type: ignore
            table.append(p_hdr)
            start += entry_size
        return table

    @cached_property
    def section_hdr_table(self) -> list[Elf32SHdr]:
        """Returns a list of Elf32 Section Headers."""
        table: list[Elf32SHdr] = []
        start = self.hdr.e_shoff.value
        entry_size = self.hdr.e_shentsize.value
        for _ in range(self.hdr.e_shnum):
            s_hdr = Elf32SHdr()
            s_hdr.attach(self.data[start : start + entry_size])  # type: ignore
            table.append(s_hdr)
            start += entry_size
        return table


class Elf64(Elf):
    """64-bit Elf Executable Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 64-bit Elf Handler instance."""
        super().__init__(Elf64Hdr, data)

    @property
    def entry(self) -> str:
        """Return Elf Entry property."""
        return f"0x{self.hdr.e_entry.value:016x}"

    @property
    def prog_hdr_offset(self) -> str:
        """Return Elf Program Hdr Offset property."""
        return f"0x{self.hdr.e_phoff.value:016x}"

    @property
    def section_hdr_offset(self) -> str:
        """Return Elf Section Hdr Offset property."""
        return f"0x{self.hdr.e_shoff.value:016x}"

    @cached_property
    def prog_hdr_table(self) -> list[Elf64PHdr]:
        """Returns a list of Elf64 Program Headers."""
        table: list[Elf64PHdr] = []
        start = self.hdr.e_phoff.value
        entry_size = self.hdr.e_phentsize.value
        for _ in range(self.hdr.e_phnum):
            p_hdr = Elf64PHdr()
            p_hdr.attach(self.data[start : start + entry_size])  # type: ignore
            table.append(p_hdr)
            start += entry_size
        return table

    @cached_property
    def section_hdr_table(self) -> list[Elf64SHdr]:
        """Returns a list of Elf64 Section Headers."""
        table: list[Elf64SHdr] = []
        start = self.hdr.e_shoff.value
        entry_size = self.hdr.e_shentsize.value
        for _ in range(self.hdr.e_shnum):
            s_hdr = Elf64SHdr()
            s_hdr.attach(self.data[start : start + entry_size])  # type: ignore
            table.append(s_hdr)
            start += entry_size
        return table
