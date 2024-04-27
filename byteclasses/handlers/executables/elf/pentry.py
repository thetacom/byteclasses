"""Elf Program Table Entry."""

from ..._data_handler import _DataHandler
from .phdr import PHdr32, PHdr64

__all__ = [
    "PEntry32",
    "PEntry64",
]


class PEntry(_DataHandler):
    """Elf Program Table Entry Handler."""

    def __init__(self, hdr_cls: type[PHdr32 | PHdr64], data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize PEntry Handler instance."""
        super().__init__(data)
        self._hdr = hdr_cls()
        try:
            self._hdr.attach(memoryview(self._data))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return PEntry string."""
        return repr(self)

    def __repr__(self) -> str:
        """Return PEntry raw representation."""
        return (
            f"{self.__class__.__name__}(type={self.type}, offset={self.offset}, vaddr={self.vaddr}, "
            f"paddr={self.paddr}, file_size={self.file_size}, flags={self.flags})"
        )

    @property
    def hdr(self) -> PHdr32 | PHdr64:
        """Return Program Table Entry header."""
        return self._hdr

    @property
    def type(self) -> str:
        """Return PEntry Type property."""
        return self.hdr.p_type.name

    @property
    def offset(self) -> str:
        """Return PEntry Offset property."""
        return str(self.hdr.p_offset)

    @property
    def vaddr(self) -> str:
        """Return PEntry VAddr property."""
        return str(self.hdr.p_vaddr)

    @property
    def paddr(self) -> str:
        """Return PEntry PAddr property."""
        return str(self.hdr.p_paddr)

    @property
    def file_size(self) -> str:
        """Return PEntry file size property."""
        return str(self.hdr.p_filesz)

    @property
    def flags(self):
        """Return PEntry flags property."""
        return self.hdr.p_flags.flags


class PEntry32(PEntry):
    """32-bit PEntry Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 32-bit PEntry Handler instance."""
        super().__init__(PHdr32, data)


class PEntry64(PEntry):
    """64-bit PEntry Handler."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 64-bit PEntry Handler instance."""
        super().__init__(PHdr64, data)
