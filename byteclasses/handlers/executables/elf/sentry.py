"""Elf Section Table Entry."""

from ..._data_handler import _DataHandler
from .shdr import SHdr32, SHdr64

__all__ = [
    "SEntry32",
    "SEntry64",
]


class SEntry(_DataHandler):
    """Elf Section Table Entry Handler."""

    def __init__(self, hdr_cls: type[SHdr32 | SHdr64], data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize SEntry Handler instance."""
        super().__init__(data)
        self._hdr = hdr_cls()
        try:
            self._hdr.attach(memoryview(self._data))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return SEntry string."""
        return repr(self)

    def __repr__(self) -> str:
        """Return SEntry raw representation."""
        return (
            f"{self.__class__.__name__}(name={self.name}, type={self.type}, flags={self.flags}, "
            f"addr={self.addr}, offset={self.offset}, size={self.size}, link={self.link}, "
            f"info={self.info}, addr_align={self.addr_align}, entry_size={self.entry_size})"
        )

    @property
    def hdr(self) -> SHdr32 | SHdr64:
        """Return Section Table Entry header."""
        return self._hdr

    @property
    def name(self) -> str:
        """Return SEntry Name property."""
        return str(self.hdr.sh_name)

    @property
    def type(self) -> str:
        """Return SEntry Type property."""
        return self.hdr.sh_type.name

    @property
    def flags(self):
        """Return SEntry flags property."""
        return self.hdr.sh_flags

    @property
    def addr(self) -> str:
        """Return SEntry Addr property."""
        return str(self.hdr.sh_addr)

    @property
    def offset(self) -> str:
        """Return SEntry Offset property."""
        return str(self.hdr.sh_offset)

    @property
    def size(self) -> str:
        """Return SEntry Size property."""
        return str(self.hdr.sh_size)

    @property
    def link(self) -> str:
        """Return SEntry Link property."""
        return str(self.hdr.sh_link)

    @property
    def info(self) -> str:
        """Return SEntry Info property."""
        return str(self.hdr.sh_info)

    @property
    def addr_align(self) -> str:
        """Return SEntry addr_align property."""
        return str(self.hdr.sh_addralign)

    @property
    def entry_size(self) -> str:
        """Return SEntry entry_size property."""
        return str(self.hdr.sh_entsize)


class SEntry32(SEntry):
    """32-bit SEntry Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 32-bit SEntry Handler instance."""
        super().__init__(SHdr32, data)


class SEntry64(SEntry):
    """64-bit SEntry Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 64-bit SEntry Handler instance."""
        super().__init__(SHdr64, data)
