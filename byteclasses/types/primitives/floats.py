"""Fixed length floating point types."""

from collections.abc import ByteString
from struct import calcsize
from typing import Any, cast

from ..._enums import ByteOrder, TypeChar
from ...types.primitives._primitive_number import _PrimitiveNumber

__all__ = [
    "Float16",
    "Half",
    "Float32",
    "Float",
    "Float64",
    "Double",
]


class _FixedFloat(_PrimitiveNumber):
    """Generic Fixed Size Float."""

    def __init__(
        self,
        value: float | None = None,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE.value,
        data: ByteString | None = None,
    ) -> None:
        """Initialize Fixed Float instance."""
        super().__init__(value, byte_order=byte_order, data=data)

    def _bound_value(self, value: float) -> float:
        """Bound the value of the instance."""
        return value

    @property
    def value(self) -> float:
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
