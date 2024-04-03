"""Abstract fixed size numeric type.

The parent class for all fixed size numeric primitive types.

Implements interfaces that attempt to adhere to the following specifications:
[A Type Hierarchy for Numbers](https://peps.python.org/pep-3141/)
[Introducing Abstract Base Classes](https://peps.python.org/pep-3119/)

"""

import math
from abc import abstractmethod
from collections.abc import Iterable
from numbers import Integral, Real
from struct import pack, unpack
from typing import Any, SupportsIndex

from ..enums import ByteOrder
from ..types._fixed_size_type import _FixedSizeType

__all__: list[str] = []


class _FixedNumericType(_FixedSizeType):
    """Base class for fixed size numeric types."""

    def __init__(
        self,
        value: int | float = 0,
        *,
        byte_order: Iterable[SupportsIndex] = ByteOrder.NATIVE.value,
    ) -> None:
        """Initialize the instance."""
        super().__init__(byte_order)
        if isinstance(value, _FixedNumericType):
            self.value = value.value
        elif isinstance(value, Real):
            self.value = value
        else:
            raise TypeError(f"Invalid value: {value}")

    def __str__(self) -> str:
        """Return the numeric representation of the instance."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return the string representation of the instance."""
        return f"{self.__class__.__name__}({self.value})"

    def __abs__(self):
        """Return the absolute value of the instance.

        Satisfies Complex interface.
        """
        return abs(self.value)

    def __add__(self, other: Any):
        """Return the sum of the instance and the other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value + other.value
        if isinstance(other, Real):
            return self.value + other
        return NotImplemented

    def __radd__(self, other: Any):
        """Return the sum of the instance and the other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value + other.value
        if isinstance(other, Real):
            return self.value + other
        return NotImplemented

    def __bool__(self) -> bool:
        """Return the boolean value of the instance.

        Satisfies Complex interface.
        """
        return bool(self.value)

    def __ceil__(self):
        """Return the ceiling of the instance.

        Satisfies Real interface.
        """
        return math.ceil(self.value)

    def __complex__(self):
        """Return the complex value of the instance.

        Satisfies Complex interface.
        """
        return complex(self.value)

    def __eq__(self, other: Any):
        """Return True if the instance is equal to other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value == other.value
        if isinstance(other, Real):
            return self.value == other
        return NotImplemented

    def __divmod__(self, other: Any):
        """Return the quotient and remainder of the instance and other.

        Satisfies Real interface.
        """
        if isinstance(other, _FixedNumericType):
            return divmod(self.value, other.value)
        if isinstance(other, Real):
            return divmod(self.value, other)
        return NotImplemented

    def __rdivmod__(self, other: Any):
        """Return the quotient and remainder of the instance and other.

        Satisfies Real interface.
        """
        if isinstance(other, _FixedNumericType):
            return divmod(other.value, self.value)
        if isinstance(other, Real):
            return divmod(other, self.value)
        return NotImplemented

    def __float__(self) -> float:
        """Return the floating point value of the instance.

        Satisfies Real interface.
        """
        return float(self.value)

    def __floor__(self):
        """Return the floor of the instance.

        Satisfies Real interface.
        """
        return math.floor(self.value)

    def __floordiv__(self, other: Any):
        """Return the floor division of the instance and other."""
        if isinstance(other, _FixedNumericType):
            return self.value // other.value
        if isinstance(other, Integral):
            return self.value // other
        return NotImplemented

    def __rfloordiv__(self, other: Any):
        """Return the floor division of the instance and other."""
        if isinstance(other, _FixedNumericType):
            return other.value // self.value
        if isinstance(other, Real):
            return other // self.value
        return NotImplemented

    def __ge__(self, other: Any):
        """Return True if the instance is greater than or equal to other."""
        if isinstance(other, _FixedNumericType):
            return self.value >= other.value
        if isinstance(other, Real):
            return self.value >= other
        return NotImplemented

    def __gt__(self, other: Any):
        """Return True if the instance is greater than other."""
        if isinstance(other, _FixedNumericType):
            return self.value > other.value
        if isinstance(other, Real):
            return self.value > other
        return NotImplemented

    def __hash__(self) -> int:
        """Return the hash value of the instance.

        Satisfies Number interface.
        """
        return hash(self.value)

    def __le__(self, other: Any):
        """Return True if the instance is less than or equal to other.

        Satisfies Real interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value <= other.value
        if isinstance(other, Real):
            return self.value <= other
        return NotImplemented

    def __lt__(self, other: Any):
        """Return True if the instance is less than other.

        Satisfies Real interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value < other.value
        if isinstance(other, Real):
            return self.value < other
        return NotImplemented

    def __mod__(self, other: Any):
        """Return the modulus of the instance and other.

        Satisfies Real interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value % other.value
        if isinstance(other, Real):
            return self.value % other
        return NotImplemented

    def __rmod__(self, other: Any):
        """Return the modulus of the instance and other.

        Satisfies Real interface.
        """
        if isinstance(other, _FixedNumericType):
            return other.value % self.value
        if isinstance(other, Real):
            return other % self.value
        return NotImplemented

    def __mul__(self, other: Any):
        """Return the product of the instance and other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value * other.value
        if isinstance(other, Real):
            return self.value * other
        return NotImplemented

    def __rmul__(self, other: Any):
        """Return the product of the instance and other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value * other.value
        if isinstance(other, Real):
            return self.value * other
        return NotImplemented

    def __neg__(self):
        """Return the negation of the instance.

        Satisfies Real interface.
        """
        return -self.value

    def __pos__(self):
        """Return a positive value instance.

        Satisfies Real interface.
        """
        return +self.value

    def __pow__(self, exponent: Any, modulus=None):
        """Return the power of the instance and other.

        Satisfies Complex interface.
        """
        if isinstance(exponent, _FixedNumericType):
            return self.value**exponent.value
        if isinstance(exponent, int):
            return self.value**exponent
        return NotImplemented

    def __rpow__(self, base: Any):
        """Return the power of the instance and other.

        Satisfies Complex interface.
        """
        if isinstance(base, _FixedNumericType):
            return base.value**self.value
        if isinstance(base, int):
            return base**self.value
        return NotImplemented

    def __round__(self, ndigits=None):
        """Return the rounded value of the instance.

        Satisfies Real interface.
        """
        return round(self.value, ndigits)

    def __sub__(self, other: Any):
        """Return the difference of the instance and other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return self.value - other.value
        if isinstance(other, Real):
            return self.value - other
        return NotImplemented

    def __rsub__(self, other: Any):
        """Return the difference of the other and instance.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return other.value - self.value
        if isinstance(other, Real):
            return other - self.value
        return NotImplemented

    def __truediv__(self, other: Any, allow_cast: bool = False):
        """Return the true division of the instance and other.

        Satisfies Complex interface.

        self / other: Should promote to float when necessary.
        """
        if isinstance(other, _FixedNumericType):
            return self.value / other.value
        if isinstance(other, Real):
            return self.value / other
        return NotImplemented

    def __rtruediv__(self, other: Any):
        """Return the quotient of the instance and other.

        Satisfies Complex interface.
        """
        if isinstance(other, _FixedNumericType):
            return other.value / self.value
        if isinstance(other, Real):
            return other / self.value
        return NotImplemented

    def __trunc__(self) -> int:
        """Truncate the instance to an integer.

        Satisfies Real interface.
        """
        raise NotImplementedError

    def _validate_value(self, new_value: Any | None = None) -> None:
        """Validate the value."""
        raise NotImplementedError("_validate_value method not implemented")

    @property
    def _value(self):
        """Return the value of the instance."""
        if self._data is None:
            raise ValueError("value is None")
        if not isinstance(self._data, (bytearray, memoryview)):
            raise ValueError("Invalid type for internal data property")
        if len(self._data) < len(self):
            raise ValueError("Internal data property too short")
        return unpack(self.fmt, self._data[: len(self)])[0]

    @_value.setter
    def _value(self, new_value: Any) -> None:
        """Set the value of the instance."""
        if isinstance(new_value, _FixedNumericType):
            value_ = new_value.value
        elif isinstance(new_value, Real):
            value_ = new_value
        else:
            raise TypeError(f"Value cannot be {type(new_value)}")
        self._validate_value(value_)
        self.data = pack(self.fmt, value_)

    @property
    @abstractmethod
    def value(self) -> Any:
        """Return the value of the instance."""

    @value.setter
    @abstractmethod
    def value(self, new_value: Any) -> None:
        """Set the value of the instance."""
