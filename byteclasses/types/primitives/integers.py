"""Fixed Size Integer Types."""

from collections.abc import ByteString
from functools import cached_property
from numbers import Integral
from struct import calcsize
from typing import Any, cast

from ..._enums import ByteOrder, TypeChar
from ...types.primitives._primitive_number import _PrimitiveNumber

__all__ = [
    "Int",
    "Int8",
    "SChar",
    "UInt8",
    "UChar",
    "Int16",
    "Short",
    "UInt16",
    "Ptr16",
    "UShort",
    "Int32",
    "UInt32",
    "UInt",
    "Ptr32",
    "Long",
    "ULong",
    "Int64",
    "UInt64",
    "Ptr64",
    "LongLong",
    "ULongLong",
]


class UnderflowError(OverflowError):
    """Exception raised when an integer underflow occurs."""


class FixedIntegerDivisionError(OverflowError):
    """Exception raised when an integer divison results in a non integer value."""


class _PrimitiveInt(_PrimitiveNumber):
    """Generic Fixed Size Integer."""

    _signed: bool = NotImplemented

    def __init__(
        self,
        value: Any | None = None,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE.value,
        data: ByteString | None = None,
        allow_overflow: bool = False,
    ) -> None:
        """Initialize Fixed Int instance."""
        self._allow_overflow = allow_overflow
        if self._signed is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__} does not implement '_signed'")
        super().__init__(value, byte_order=byte_order, data=data)

    @property
    def allow_overflow(self) -> bool:
        """Return allow overflow status."""
        return self._allow_overflow

    @cached_property
    def max(self) -> int:
        """Return the maximum value."""
        return (1 << (self.bit_length - 1)) - 1 if self._signed else (1 << self.bit_length) - 1

    @cached_property
    def min(self) -> int:
        """Return the minimum value."""
        return -(1 << (self.bit_length - 1)) if self._signed else 0

    @property
    def signed(self) -> bool:
        """Return whether the signedness."""
        return self._signed

    @property
    def value(self) -> int:
        """Return the value of the instance."""
        return cast(int, self._get_value())

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the value of the instance."""
        self._set_value(new_value, int)

    def __and__(self, other: Any):
        """Return the bitwise AND of the instance and other."""
        if isinstance(other, _PrimitiveInt):
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
        if isinstance(other, _PrimitiveInt):
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
        if isinstance(other, _PrimitiveInt):
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
        if isinstance(other, _PrimitiveInt):
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
        if isinstance(other, _PrimitiveInt):
            return self.value ^ other.value
        if isinstance(other, Integral):
            return self.value ^ other
        return NotImplemented

    def __rxor__(self, other: Any):
        """Return the bitwise XOR of the instance and other."""
        return self.__xor__(other)

    def _bound_value(self, value: int) -> int:
        if value < self.min or value > self.max:
            if self._allow_overflow:
                mod_value = 1 << self.bit_length
                if self._signed:
                    offset = 1 << (self.bit_length - 1)
                    return ((value + offset) % mod_value) - offset
                return value % mod_value
            if value < self.min:
                raise UnderflowError(f"UnderfowError: value ({value}) below {self.__class__.__name__} min ({self.min})")
            if value > self.max:
                raise OverflowError(
                    f"OverfowError: value ({value}) exceeded {self.__class__.__name__} max ({self.max})"
                )
        return value


class Int8(_PrimitiveInt):
    """8-bit signed integer."""

    _type_char: bytes = TypeChar.INT8.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


SChar = Int8


class UInt8(_PrimitiveInt):
    """8-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT8.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


UChar = UInt8


class Int16(_PrimitiveInt):
    """16-bit signed integer."""

    _type_char: bytes = TypeChar.INT16.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


Short = Int16


class UInt16(_PrimitiveInt):
    """16-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT16.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


UShort = UInt16


class Ptr16(UInt16):
    """16-bit Pointer (UInt16).

    String representation displays in hexadecimal.
    """

    def __str__(self) -> str:
        """Return Ptr16 string representation."""
        return f"0x{self.value:04x}"

    def __repr__(self) -> str:
        """Return the raw representation."""
        return f"{self.__class__.__name__}({hex(self.value)})"


class Int32(_PrimitiveInt):
    """32-bit signed integer."""

    _type_char: bytes = TypeChar.INT32.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


Int = Int32


class UInt32(_PrimitiveInt):
    """32-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT32.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


UInt = UInt32


class Ptr32(UInt32):
    """32-bit Pointer (UInt32).

    String representation displays in hexadecimal.
    """

    def __str__(self) -> str:
        """Return Ptr32 string representation."""
        return f"0x{self.value:08x}"

    def __repr__(self) -> str:
        """Return the raw representation."""
        return f"{self.__class__.__name__}({hex(self.value)})"


class Long(_PrimitiveInt):
    """32-bit signed long integer."""

    _type_char: bytes = TypeChar.LONG.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


class ULong(_PrimitiveInt):
    """32-bit unsigned long integer."""

    _type_char: bytes = TypeChar.ULONG.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


class Int64(_PrimitiveInt):
    """64-bit signed integer."""

    _type_char: bytes = TypeChar.INT64.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


LongLong = Int64


class UInt64(_PrimitiveInt):
    """64-bit unsigned integer."""

    _type_char: bytes = TypeChar.UINT64.value
    _length: int = calcsize(_type_char)
    _signed: bool = False


ULongLong = UInt64


class Ptr64(UInt64):
    """64-bit Pointer (UInt64).

    String representation displays in hexadecimal.
    """

    def __str__(self) -> str:
        """Return Ptr64 string representation."""
        return f"0x{self.value:016x}"

    def __repr__(self) -> str:
        """Return the raw representation."""
        return f"{self.__class__.__name__}({hex(self.value)})"
