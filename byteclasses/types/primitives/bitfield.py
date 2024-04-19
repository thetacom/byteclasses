"""BitField Fixed Length Class."""

from collections.abc import ByteString, Sequence
from struct import calcsize
from typing import overload

from ..._enums import ByteOrder, TypeChar
from .._fixed_size_type import _FixedSizeType


class BitField(_FixedSizeType):
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
        super().__init__(byte_order=byte_order, data=data)

    def __str__(self) -> str:
        """Return bitfield string representation."""
        return "".join(bin(i)[2:].rjust(8, "0")[::-1] for i in self._data)

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
