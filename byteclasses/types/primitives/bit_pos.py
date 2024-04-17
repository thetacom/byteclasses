"""Bit Position Member class."""

from .bitfield import BitField


class BitPos:
    """A member class representing a pit position for use in a BitField class."""

    def __init__(self, idx: int, *, bit_width: int = 1) -> None:
        """Initialize BitPos."""
        super().__init__()
        self._idx = idx
        self._bit_width = bit_width

    def __get__(self, instance, owner=None):
        """Implement get descriptor."""
        if not isinstance(instance, BitField):
            raise TypeError("BitPos only intended for use on BitField classes.")
        if self._bit_width == 1:
            return instance[self.idx]
        val = 0
        for i in instance[self.idx : self.idx + self.bit_width][::-1]:
            val = val << 1 | int(i)
        return val

    def __set__(self, instance, value) -> None:
        """Implement set descriptor."""
        if not isinstance(instance, BitField):
            raise TypeError("BitPos only intended for use on BitField classes.")
        instance[self.idx] = value

    @property
    def bit_width(self) -> int:
        """Return BitPos bit width."""
        return self._bit_width

    @property
    def idx(self) -> int:
        """Return read-only index value."""
        return self._idx
