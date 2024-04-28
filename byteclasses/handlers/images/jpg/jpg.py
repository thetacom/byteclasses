"""Pre-defined JPG Image Handler Module."""

from collections.abc import ByteString
from reprlib import recursive_repr

from ..._data_handler import _DataHandler
from .seg import Seg


class JPG(_DataHandler):
    """JPG Image Handler Class."""

    def __init__(self, data: ByteString) -> None:
        """Initialize instance."""
        super().__init__(data)
        segments = []
        offset = 0
        while offset < len(data):
            seg = Seg(data[offset:])
            segments.append(seg)
            offset += len(seg)
        self._segments = tuple(segments)

    def __repr__(self) -> str:
        """Return instance raw representation."""
        return f"{self.__class__.__name__}(data={self.data!r})"

    @recursive_repr()
    def __str__(self) -> str:
        """Return instance string representation."""
        return f"<{self.__class__.__name__}:" + "|".join(map(repr, self.segments)) + ">"

    @property
    def segments(self) -> tuple[Seg, ...]:
        """Return image segments."""
        return self._segments
