"""Fixed Size Integer Types."""

from functools import cached_property
from numbers import Integral
from struct import calcsize
from typing import Any, cast

from ..._enums import ByteOrder, TypeChar
from ...types._fixed_numeric_type import _FixedNumericType

__all__ = [
    "Int",
    "Int8",
    "SChar",
    "UInt8",
    "UChar",
    "Int16",
    "Short",
    "UInt16",
    "UShort",
    "Int32",
    "UInt32",
    "UInt",
    "Long",
    "ULong",
    "Int64",
    "UInt64",
    "LongLong",
    "ULongLong",
]


class UnderflowError(OverflowError):
    """Exception raised when an integer underflow occurs."""


class FixedIntegerDivisionError(OverflowError):
    """Exception raised when an integer divison results in a non integer value."""


class _FixedInt(_FixedNumericType):
    """Generic Fixed Size Integer."""

    _signed: bool = NotImplemented

    def __init__(
        self,
        value=0,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE.value,
    ) -> None:
        """Initialize Fixed Int instance."""
        if self._signed is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__} does not implement '_signed'")
        super().__init__(value, byte_order=byte_order)

    @cached_property
    def max(self) -> int:
        """Return the maximum value."""
        return (1 << (self._length * 8 - 1)) - 1 if self._signed else (1 << (self._length * 8)) - 1

    @cached_property
    def min(self) -> int:
        """Return the minimum value."""
        return -(1 << (self._length * 8 - 1)) if self._signed else 0

    @property
    def signed(self) -> bool:
        """Return whether the signedness."""
        return self._signed

    @property
    def value(self):
        """Return the value of the instance."""
        return cast(int, self._get_value())

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the value of the instance."""
        self._set_value(new_value, int)

    def __and__(self, other: Any):
        """Return the bitwise AND of the instance and other."""
        if isinstance(other, _FixedInt):
            return self.value & other.value
        if isinstance(other, int):
            return self.value & other
        return NotImplemented

    def __rand__(self, other: Any):
        """Return the bitwise AND of the instance and other.

        Satisfies the Integral interface.
        """
        return self.__and__(other)

    def __index__(self):
        """Return the index of the instance."""
        return int(self.value)

    def __int__(self):
        """Return the integer value of the instance.

        Satisfies the Integral interface.
        """
        return int(self.value)

    def __invert__(self):
        """Return the bitwise inverse of the instance."""
        return ~self.value & self.max

    def __lshift__(self, other: Any):
        """Return the left shift of the instance and other.

        Satisfies the Integral interface.
        """
        if isinstance(other, _FixedInt):
            return self.value << other.value
        if isinstance(other, Integral):
            return self.value << other
        return NotImplemented

    def __rlshift__(self, other: Any):
        """Return the left shift of the instance and other.

        Satisfies the Integral interface.
        """
        if isinstance(other, Integral):
            return other << self.value
        return NotImplemented

    def __or__(self, other: Any):
        """Return the bitwise OR of the instance and other.

        Satisfies the Integral interface.
        """
        if isinstance(other, _FixedInt):
            return self.value | other.value
        if isinstance(other, Integral):
            return self.value | other
        return NotImplemented

    def __ror__(self, other: Any):
        """Return the bitwise OR of the instance and other.

        Satisfies the Integral interface.
        """
        return self.__or__(other)

    def __rshift__(self, other: Any):
        """Return the right shift of the instance and other.

        Satisfies the Integral interface.
        """
        if isinstance(other, _FixedInt):
            return self.value >> other.value
        if isinstance(other, Integral):
            return self.value >> other
        return NotImplemented

    def __rrshift__(self, other: Any):
        """Return the right shift of the instance and other.

        Satisfies the Integral interface.
        """
        if isinstance(other, Integral):
            return other >> self.value
        return NotImplemented

    def __trunc__(self):
        """Return the truncated value of the instance."""
        return self.value

    def __xor__(self, other: Any):
        """Return the bitwise XOR of the instance and other."""
        if isinstance(other, _FixedInt):
            return self.value ^ other.value
        if isinstance(other, Integral):
            return self.value ^ other
        return NotImplemented

    def __rxor__(self, other: Any):
        """Return the bitwise XOR of the instance and other."""
        return self.__xor__(other)

    def _validate_value(self, value: Any) -> None:
        if value < self.min:
            raise UnderflowError(f"UnderfowError: value ({value}) below {self.__class__.__name__} min ({self.min})")
        if value > self.max:
            raise OverflowError(f"OverfowError: value ({value}) exceeded {self.__class__.__name__} max ({self.max})")


class Int8(_FixedInt):
    """8-bit signed integer."""

    _type_char: bytes = TypeChar.INT8.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


SChar = Int8


class UInt8(_FixedInt):
    """8-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT8.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


UChar = UInt8


class Int16(_FixedInt):
    """16-bit signed integer."""

    _type_char: bytes = TypeChar.INT16.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


Short = Int16


class UInt16(_FixedInt):
    """16-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT16.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


UShort = UInt16


class Int32(_FixedInt):
    """32-bit signed integer."""

    _type_char: bytes = TypeChar.INT32.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


Int = Int32


class UInt32(_FixedInt):
    """32-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT32.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


UInt = UInt32


class Long(_FixedInt):
    """32-bit signed long integer."""

    _type_char: bytes = TypeChar.LONG.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


class ULong(_FixedInt):
    """32-bit unsigned long integer."""

    _type_char: bytes = TypeChar.ULONG.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


class Int64(_FixedInt):
    """64-bit signed integer."""

    _type_char: bytes = TypeChar.INT64.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


LongLong = Int64


class UInt64(_FixedInt):
    """64-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT64.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


ULongLong = UInt64
