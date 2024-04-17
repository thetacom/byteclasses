"""Fixed Size Character Primitives."""

from struct import calcsize

from ..._enums import ByteOrder, TypeChar
from ...types.primitives.integers import Int8, UInt8

__all__ = ["SChar", "UChar", "Char"]


class SChar(Int8):
    """8-bit Signed Character."""

    _type_char: bytes = TypeChar.INT8.value
    _length: int = calcsize(_type_char)
    _signed: bool = True


class UChar(UInt8):
    """8-bit Unsigned Character."""

    _type_char: bytes = TypeChar.UINT8.value
    _length: int = calcsize(_type_char)
    _signed: bool = False

    def __init__(
        self,
        char: str = "\x00",
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE.value,
    ) -> None:
        """Initialize UChar instance."""
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Character value must a single character string.")
        super().__init__(char, byte_order=byte_order)

    def __str__(self) -> str:
        """Return the numeric representation of the instance."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return the string representation of the instance."""
        return f"{self.__class__.__name__}({self.value!r})"

    @property
    def value(self):
        """Return the value of the instance."""
        return chr(self._get_value())

    @value.setter
    def value(self, new_value: str) -> None:
        """Set the value of the instance."""
        if len(new_value) != 1:
            raise ValueError("Value can only be a single character.")
        self._set_value(ord(new_value), int)


Char = UChar
