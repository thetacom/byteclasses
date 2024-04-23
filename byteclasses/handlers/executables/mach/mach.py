"""Pre-defined MacOS Executable Handler Class."""

from ..._data_handler import _DataHandler
from .mach_hdr import CPU_MAP, CPUType, MachHdr32, MachHdr64

__all__ = [
    "Mach32",
    "Mach64",
]


class Mach(_DataHandler):
    """Mach-O Executable Handler.

    Handles 32-bit and 64-bit Mach-Os.
    """

    def __init__(self, hdr_cls: type[MachHdr32 | MachHdr64], data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize Mach-O Handler instance."""
        super().__init__(data)
        self._hdr = hdr_cls()
        try:
            self._hdr.attach(memoryview(self._data))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return Mach-O Executable string."""
        return f"{self.__class__.__name__}(magic={self.magic})"

    @property
    def hdr(self) -> MachHdr32 | MachHdr64:
        """Return Mach-O header."""
        return self._hdr

    @property
    def magic(self) -> str:
        """Return Mach-O Magic property."""
        return str(self.hdr.magic.data)

    @property
    def cpu_type(self) -> str:
        """Return Mach-O CPU Type property."""
        try:
            return CPUType(self.hdr.cputype.value).name
        except ValueError:
            return hex(self.hdr.cputype)

    @property
    def cpu_subtype(self) -> str:
        """Return Mach-O CPU Subtype property."""
        try:
            subtype_enum = CPU_MAP[CPUType(self.hdr.cputype.value)]
            return subtype_enum(self.hdr.cpusubtype.value).name
        except (KeyError, ValueError):
            return hex(self.hdr.cpusubtype)

    @property
    def filetype(self):
        """Return Mach-O Filetype property."""
        return self.hdr.filetype

    @property
    def num_cmds(self):
        """Return Mach-O num_cmds property."""
        return self.hdr.ncmds

    @property
    def cmd_size(self):
        """Return Mach-O cmd_size property."""
        return self.hdr.sizeofcmds

    @property
    def flags(self):
        """Return Mach-O flags property."""
        return self.hdr.flags.flags


class Mach32(Mach):
    """32-bit Mach-O Executable Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 32-bit Mach-O Handler instance."""
        super().__init__(MachHdr32, data)


class Mach64(Mach):
    """64-bit Elf Executable Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 64-bit Mach-O Handler instance."""
        super().__init__(MachHdr64, data)
