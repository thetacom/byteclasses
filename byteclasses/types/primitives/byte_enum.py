"""A fixed size enum class."""

from collections.abc import ByteString
from enum import IntEnum

from ..._enums import ByteOrder
from ...constants import _BYTECLASS
from .integers import _PrimitiveInt


class ByteEnum:
    """A fixed size enum class."""

    def __init__(
        self,
        enum_cls: type[IntEnum],
        int_cls: type[_PrimitiveInt],
        value: int | None = None,
        /,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
        data: ByteString | None = None,
    ):
        if not issubclass(enum_cls, IntEnum):
            raise ValueError("enum_cls must be a subclass of the IntEnum class.")
        if not issubclass(int_cls, _PrimitiveInt):
            raise ValueError("int_cls must be a byteclass integer primitive class.")
        self._enum_cls = enum_cls
        self._int: _PrimitiveInt = int_cls(value, byte_order=byte_order)
        if data is not None:
            self._int.data = data

    def __str__(self) -> str:
        """Return the string representation of the instance."""
        return self.name

    def __repr__(self) -> str:
        """Return the raw representation of the instance."""
        return f"<{self._enum_cls.__name__}.{self.name}: {hex(self.value)}>"

    def __bytes__(self) -> bytes:
        """Return the byte representation of the instance."""
        return bytes(self._int)

    def __len__(self) -> int:
        """Return instance byte length."""
        return len(self._int)

    def __int__(self) -> int:
        """Return instance integer value."""
        return self.value

    @property
    def byte_order(self) -> ByteOrder:
        """Return the byte order of the instance."""
        return self._int.byte_order

    @byte_order.setter
    def byte_order(self, new_byte_order: bytes | ByteOrder) -> None:
        """Set the byte_order of the instance."""
        self._int.byte_order = ByteOrder(new_byte_order)

    @property
    def data(self) -> ByteString:
        """Return the byte representation of the instance."""
        return self._int.data

    @data.setter
    def data(self, new_data: bytes | bytearray | None = None) -> None:
        """Set the byte representation of the instance."""
        self._int.data = new_data

    @property
    def name(self) -> str:
        """Return the name of the instance."""
        try:
            return self._enum_cls(self.value).name
        except ValueError:
            return "UNKNOWN"

    @property
    def value(self) -> int:
        """Return the value of the instance."""
        return self._int.value

    @value.setter
    def value(self, new_value: int) -> None:
        """Set the value of the instance."""
        self._int.value = new_value

    def attach(self, new_data: ByteString, retain_value: bool = True) -> None:
        """Replace _int data and attach provided memoryview.

        Memoryview length must match byte length of fixed length type.
        """
        self._int.attach(new_data, retain_value)


setattr(ByteEnum, _BYTECLASS, True)
