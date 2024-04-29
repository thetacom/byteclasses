"""Elf Handler Class."""

from functools import cached_property

from ..._data_handler import _DataHandler
from .elf_hdr import ElfHdr32, ElfHdr64
from .pentry import PEntry32, PEntry64
from .sentry import SEntry32, SEntry64

__all__ = [
    "Elf32",
    "Elf64",
]


class Elf(_DataHandler):
    """Elf Executable Handler.

    Handles 32-bit and 64-bit ELFs.
    """

    def __init__(self, hdr_cls: type[ElfHdr32 | ElfHdr64], data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize Elf Handler instance."""
        super().__init__(data)
        self._hdr = hdr_cls()
        try:
            self._hdr.attach(memoryview(self._data))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return Elf Executable string."""
        return f"{self.__class__.__name__}(type={self.type}, machine={self.machine}, version={self.version})"

    @property
    def hdr(self) -> ElfHdr32 | ElfHdr64:
        """Return Elf header."""
        return self._hdr

    @property
    def type(self) -> str:
        """Return Elf Type property."""
        return self.hdr.e_type.name

    @property
    def machine(self) -> str:
        """Return Elf Machine property."""
        return self.hdr.e_machine.name

    @property
    def version(self) -> str:
        """Return Elf Version property."""
        return self.hdr.e_version.name

    @property
    def flags(self) -> dict[str, bool | int]:
        """Return Elf Flags property."""
        return self.hdr.e_flags.flags

    @property
    def entry(self):
        """Return Elf Entry property."""
        return self.hdr.e_entry

    @property
    def prog_hdr_offset(self):
        """Return Elf Program Hdr Offset property."""
        return self.hdr.e_phoff

    @property
    def section_hdr_offset(self):
        """Return Elf Section Hdr Offset property."""
        return self.hdr.e_shoff


class Elf32(Elf):
    """32-bit Elf Executable Handler."""

    def __init__(self, elf_data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 32-bit Elf Handler instance."""
        super().__init__(ElfHdr32, elf_data)

    @cached_property
    def pogram_table(self) -> list[PEntry32]:
        """Returns Elf32 Program Table."""
        table: list[PEntry32] = []
        start = self.hdr.e_phoff.value
        entry_size = self.hdr.e_phentsize.value
        for _ in range(self.hdr.e_phnum):
            p_entry = PEntry32(self.data[start : start + entry_size])
            table.append(p_entry)
            start += entry_size
        return table

    @cached_property
    def section_table(self) -> list[SEntry32]:
        """Returns Elf32 Section Table."""
        table: list[SEntry32] = []
        start = self.hdr.e_shoff.value
        entry_size = self.hdr.e_shentsize.value
        for _ in range(self.hdr.e_shnum):
            s_hdr = SEntry32(self.data[start : start + entry_size])
            table.append(s_hdr)
            start += entry_size
        return table


class Elf64(Elf):
    """64-bit Elf Executable Handler."""

    def __init__(self, elf_data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 64-bit Elf Handler instance."""
        super().__init__(ElfHdr64, elf_data)

    @cached_property
    def program_table(self) -> list[PEntry64]:
        """Returns Elf64 Program Table."""
        table: list[PEntry64] = []
        start = self.hdr.e_phoff.value
        entry_size = self.hdr.e_phentsize.value
        for _ in range(self.hdr.e_phnum):
            p_entry = PEntry64(self.data[start : start + entry_size])
            table.append(p_entry)
            start += entry_size
        return table

    @cached_property
    def section_table(self) -> list[SEntry64]:
        """Returns Elf64 Section Table."""
        table: list[SEntry64] = []
        start = self.hdr.e_shoff.value
        entry_size = self.hdr.e_shentsize.value
        for _ in range(self.hdr.e_shnum):
            s_hdr = SEntry64(self.data[start : start + entry_size])
            table.append(s_hdr)
            start += entry_size
        return table
