"""BitField Fixed Length Class."""

from collections.abc import ByteString, Iterable, Sequence
from struct import calcsize
from typing import overload

from ..._enums import ByteOrder, TypeChar
from ._primitive import _Primitive

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
        if instance is None and issubclass(owner, BitField):
            return self
        if not isinstance(instance, BitField):
            raise TypeError(f"BitPos only intended for use on BitField classes ({instance=})({owner=}).")
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


class BitField(_Primitive):
    """BitField Fixed Size Class."""

    byte_length: int = 1
    _signed: bool = False

    def __init__(
        self,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE.value,
        data: ByteString | None = None,
    ) -> None:
        """Initialize the instance."""
        if self.byte_length < 1:
            raise ValueError("byte_length must be at least 1 byte")
        self._type_char = TypeChar.BYTE.value * self.byte_length
        self._length: int = calcsize(self._type_char)
        if data is not None and len(data) != self._length:
            raise ValueError(f"Data length must be {self._length} bytes")
        super().__init__(byte_order=byte_order, data=data)

    def __str__(self) -> str:
        """Return bitfield string representation."""
        return (
            f"{self.__class__.__name__}("
            f"{''.join(bin(i)[2:].rjust(8, '0')[::-1] for i in self._data)}, flags={self.flags})"
        )

    def __repr__(self) -> str:
        """Return bitfield class representation."""
        return f"{self.__class__.__qualname__}(data={bytes(self._data)!r})"

    def __getitem__(self, key: int | slice) -> bool | list[bool]:
        """Get bit values based on index or slice."""
        if isinstance(key, int):
            if key < 0:
                key %= self.bit_length
            if key >= self.bit_length:
                raise IndexError(f"index {key} out of range")
            return self.get_bit(key)
        if isinstance(key, slice):
            step = 1 if key.step is None else key.step
            if key.start is None:
                start = 0 if step > 0 else self.bit_length - 1
            else:
                start = key.start
            if key.stop is None:
                stop = self.bit_length if step > 0 else -1
            else:
                stop = key.stop
            return [self.get_bit(idx) for idx in range(start, stop, step)]
        raise NotImplementedError

    @overload
    def __setitem__(self, key: int, value: int | bool) -> None: ...

    @overload
    def __setitem__(self, key: slice, value: int | bool | Sequence[int | bool]) -> None: ...

    def __setitem__(self, key: int | slice, value: int | bool | Sequence[int | bool]) -> None:
        """Set bit values based on index or slice."""
        if isinstance(key, int):
            if not isinstance(value, (int, bool)):
                raise TypeError("Assignment by index only accepts boolean or integer values.")
            self._set_bit_by_idx(key, value)
        elif isinstance(key, slice):
            self._set_bits_by_slice(key, value)
        else:
            raise NotImplementedError

    @property
    def flags(self) -> dict[str, bool | int]:
        """Return a dictionary of all named bit positions."""
        return {
            name: getattr(self, name) for name in type(self).__dict__ if isinstance(getattr(type(self), name), BitPos)
        }

    @property
    def value(self) -> tuple[bool | list[bool], ...]:
        """Return a boolean value list for all bits within BitField."""
        return tuple(self[idx] for idx in range(self.bit_length))

    @value.setter
    def value(self, new_values: bool | Iterable[bool] | dict[int, bool]):
        """Set BitField values."""
        if isinstance(new_values, bool):
            for idx in range(self.bit_length):
                self[idx] = new_values
        elif isinstance(new_values, dict):
            for idx, val in new_values.items():
                self[int(idx)] = val
        elif isinstance(new_values, (list, tuple)):
            for idx, val in enumerate(new_values):
                self[idx] = val
        else:
            raise NotImplementedError()

    def _set_bit_by_idx(self, idx: int, value: int | bool) -> None:
        """Set bit from index."""
        if idx < 0:
            idx %= self.bit_length
        if idx >= self.bit_length:
            raise IndexError(f"index ({idx}) out of range")
        self.set_bit(idx, bool(value))

    def _set_bits_by_slice(self, slc: slice, value: int | bool | Sequence[int | bool]) -> None:
        """Set multiple bits with slice."""
        if slc.step is None:
            step = 1
        else:
            step = slc.step
        if slc.start is None:
            if step > 0:
                start = 0
            else:
                start = self.bit_length - 1
        else:
            start = slc.start
        if slc.stop is None:
            if step > 0:
                stop = self.bit_length
            else:
                stop = -1
        else:
            stop = slc.stop
        if isinstance(value, (int, bool)):
            for idx in range(start, stop, step):
                self.set_bit(idx, value)
        elif isinstance(value, Sequence):
            for idx in range(start, stop, step):
                self.set_bit(idx, value[idx])

    def clear_bit(self, idx: int):
        """Clear bit in bitfield instance."""
        self.set_bit(idx, 0)

    def get_bit(self, idx: int) -> bool:
        """Get bit in bitfield instance."""
        if idx >= self.bit_length or idx < 0:
            raise IndexError("Invalid bit index")
        byte_idx = idx // 8
        offset = idx % 8
        byte_value = self._data[byte_idx]
        mask = 1 << offset
        bit_value = byte_value & mask
        return bool(bit_value)

    def set_bit(self, idx: int, value: int | bool = 1):
        """Set bit in bitfield instance."""
        if idx >= self.bit_length or idx < 0:
            raise IndexError("Invalid bit index")
        value = int(bool(value))
        byte_idx = idx // 8
        offset = idx % 8
        byte_value = self._data[byte_idx]
        if value:
            mask = 1 << offset
            byte_value |= mask
        else:
            mask = ~(1 << offset)
            byte_value &= mask
        self._data[byte_idx] = byte_value


class BitField16(BitField):
    """16-bit BitField."""

    byte_length = 2


class BitField32(BitField):
    """32-bit BitField."""

    byte_length = 4


class BitField64(BitField):
    """64-bit BitField."""

    byte_length = 8


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
