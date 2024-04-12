"""BitField Fixed Length Class."""

from collections.abc import ByteString, Iterable, Sequence
from functools import cached_property
from struct import calcsize
from typing import SupportsIndex, overload

from ..._enums import ByteOrder, TypeChar
from .._fixed_size_type import _FixedSizeType


class BitField(_FixedSizeType):
    """BitField Fixed Size Class."""

    byte_length: int = 1
    _signed: bool = False

    def __init__(
        self,
        *,
        byte_order: Iterable[SupportsIndex] = ByteOrder.NATIVE.value,
        data: ByteString | None = None,
    ) -> None:
        """Initialize the instance."""
        if self.byte_length < 1:
            raise ValueError("byte_length must be at least 1 byte")
        self._type_char = TypeChar.BYTE.value * self.byte_length
        self._length: int = calcsize(self._type_char)
        super().__init__(byte_order)
        if data:
            self.data = data

    def __str__(self) -> str:
        """Return bitfield string representation."""
        return "".join(bin(i)[2:].rjust(8, "0")[::-1] for i in self._data)

    def __repr__(self) -> str:
        """Return bitfield class representation."""
        return f"{self.__class__.__qualname__}(byte_length={self._length}, data={self._data})"

    def __getitem__(self, key: int | slice) -> bool | list[bool]:
        """Get bit values based on index or slice."""
        if isinstance(key, int):
            if key < 0:
                key %= self.bit_length
            if key >= self.bit_length:
                raise IndexError(f"index {key} out of range")
            return self.get_bit(key)
        if isinstance(key, slice):
            return [self.get_bit(idx) for idx in range(key.start, key.stop, key.step)]
        raise NotImplementedError

    @overload
    def __setitem__(self, key: int, value: int | bool) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: int | bool | Sequence[int | bool]) -> None: ...
    def __setitem__(self, key: int | slice, value: int | bool | Sequence[int | bool]) -> None:
        """Set bit values based on index or slice."""
        if isinstance(key, int):
            if key < 0:
                key %= self.bit_length
            if key >= self.bit_length:
                raise IndexError(f"index {key} out of range")
            if not isinstance(value, (int, bool)) or int(value) not in (0, 1):
                raise TypeError("Can only set bit to 0, 1, True, or False")
            self.set_bit(key, value)
        elif isinstance(key, slice):
            if isinstance(value, (int, bool)):
                for idx in range(key.start, key.stop, key.step):
                    self.set_bit(idx, value)
            elif isinstance(value, Sequence):
                for idx in range(key.start, key.stop, key.step):
                    self.set_bit(idx, value[idx])
        else:
            raise NotImplementedError

    @cached_property
    def bit_length(self) -> int:
        """Calculate instance bit length."""
        return self._length * 8

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
        binary_value = int(value)
        if binary_value not in (0, 1):
            raise ValueError("Invalid bit value")
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
