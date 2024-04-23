"""Pre-defined Windows Executable Handler Class."""

from ..._data_handler import _DataHandler
from .dos_hdr import DOSHdr
from .nt_hdr32 import NTHdr32
from .nt_hdr64 import NTHdr64

__all__ = [
    "PE32",
    "PE64",
]


class PE(_DataHandler):
    """Windows Executable Handler.

    Handles 32-bit and 64-bit PEs.
    """

    def __init__(self, hdr_cls: type[NTHdr32 | NTHdr64], data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize PE Handler instance."""
        super().__init__(data)
        self._dos_hdr = DOSHdr()
        self._hdr = hdr_cls()
        try:
            self._dos_hdr.attach(memoryview(self._data))  # type: ignore
            self._hdr.attach(memoryview(self._data[self._dos_hdr.e_lfanew.value :]))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return PE Executable string."""
        return f"{self.__class__.__name__}(magic={self.magic})"

    @property
    def dos_hdr(self) -> DOSHdr:
        """Return PE DOS header."""
        return self._dos_hdr

    @property
    def hdr(self) -> NTHdr32 | NTHdr64:
        """Return PE NT header."""
        return self._hdr

    @property
    def magic(self) -> str:
        """Return PE Magic property."""
        return str(self.dos_hdr.e_magic)


class PE32(PE):
    """Windows 32-bit Executable Data Handler."""

    def __init__(self, pe_data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 32-bit PE Handler instance."""
        super().__init__(NTHdr32, pe_data)


class PE64(PE):
    """Windows 64-bit Executable Data Handler."""

    def __init__(self, pe_data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize 64-bit PE Handler instance."""
        super().__init__(NTHdr64, pe_data)
