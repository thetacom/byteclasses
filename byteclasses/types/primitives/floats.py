"""Fixed length floating point types."""

from numbers import Number
from struct import calcsize
from typing import Any, cast

from ..._enums import TypeChar
from ...types._fixed_numeric_type import _FixedNumericType

__all__ = [
    "Float16",
    "Half",
    "Float32",
    "Float",
    "Float64",
    "Double",
]


class _FixedFloat(_FixedNumericType):
    """Generic Fixed Size Float."""

    def _validate_value(self, value: Number) -> None:
        """Validate the value of the instance."""

    @property
    def value(self):
        """Return the value of the instance."""
        return cast(float, self._get_value())

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the value of the instance."""
        self._set_value(new_value, float)


class Float16(_FixedFloat):
    """16-bit float."""

    _type_char: bytes = TypeChar.FLOAT16.value
    _length: int = calcsize(_type_char)


Half = Float16


class Float32(_FixedFloat):
    """32-bit float."""

    _type_char: bytes = TypeChar.FLOAT32.value
    _length: int = calcsize(_type_char)


Float = Float32


class Float64(_FixedFloat):
    """64-bit float."""

    _type_char: bytes = TypeChar.FLOAT64.value
    _length: int = calcsize(_type_char)


Double = Float64
