"""Bit Position Member class."""

from .bitfield import BitField

MIN_WIDTH = 1


class BitPos:
    """A member class representing a pit position for use in a BitField class."""

    def __init__(self, idx: int, *, bit_width: int = MIN_WIDTH) -> None:
        """Initialize BitPos."""
        super().__init__()
        self._idx = idx
        if bit_width < MIN_WIDTH:
            raise ValueError(f"Bit position must have a bit_width greater than one ({MIN_WIDTH}).")
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
        if self._bit_width == 1:
            instance[self.idx] = value
        else:
            remaining_bits = value
            for i in range(self.idx, self.idx + self.bit_width):
                bit = remaining_bits & 1
                instance[i] = bit
                remaining_bits = remaining_bits >> 1

    @property
    def bit_width(self) -> int:
        """Return BitPos bit width."""
        return self._bit_width

    @property
    def idx(self) -> int:
        """Return read-only index value."""
        return self._idx


def bitpos2mask(bit_pos: BitPos) -> int:
    """Return an integer mask from a BitPos instance."""
    val = 0
    for _ in range(bit_pos.bit_width):
        val = (val << 1) | 1
    return val << bit_pos.idx


def mask2bitpos(mask: int) -> BitPos:
    """Return a BitPos instance from an integer mask."""
    pos = 0
    bit_width = 0
    for i in range(len(bin(mask)[2:])):
        bit = 1 & mask
        if bit == 1:
            bit_width += 1
        else:
            if bit_width > 0:
                raise ValueError(f"Invalid mask, non-contiguous bits set ({bin(mask)}).")
        if bit_width == 1:
            pos = i
        mask = mask >> 1
    if bit_width == 0:
        raise ValueError("Invalid mask, no bits set.")
    return BitPos(pos, bit_width=bit_width)
