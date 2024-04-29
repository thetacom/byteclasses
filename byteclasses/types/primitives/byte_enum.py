"""A fixed size enum class."""

from collections.abc import ByteString
from enum import Enum, IntEnum
from typing import Any

from ..._enums import ByteOrder
from ...constants import _BYTECLASS
from ...util import is_byteclass_primitive
from ._primitive import _Primitive
from ._primitive_number import _PrimitiveNumber


class ByteEnum:
    """A fixed size enum class."""

    def __init__(
        self,
        enum_cls: type[Enum],
        var_cls: type[_Primitive],
        value: Any | None = None,
        /,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
        data: ByteString | None = None,
    ):
        if not issubclass(enum_cls, Enum):
            raise ValueError("enum_cls must be a subclass of the Enum class.")
        self._enum_cls = enum_cls
        if not is_byteclass_primitive(var_cls):
            raise ValueError("var_cls must be a byteclass primitive class.")
        self._var: _Primitive = var_cls(value, byte_order=byte_order)
        if data is not None:
            self._var.data = data

    def __str__(self) -> str:
        """Return the string representation of the instance."""
        return self.name

    def __repr__(self) -> str:
        """Return the raw representation of the instance."""
        if issubclass(self._enum_cls, IntEnum):
            return f"<{self._enum_cls.__name__}.{self.name}: {hex(self.value)}>"
        return f"<{self._enum_cls.__name__}.{self.name}: {self.value}>"

    def __bytes__(self) -> bytes:
        """Return the byte representation of the instance."""
        return bytes(self._var)

    def __len__(self) -> int:
        """Return instance byte length."""
        return len(self._var)

    def __int__(self) -> int:
        """Return instance integer value.

        Only supported for numeric variable types (ie. byteclass integers and floats).
        """
        if not isinstance(self._var, _PrimitiveNumber):
            raise TypeError(f"ByteEnum variable type ({self._var.__class__.__name__}) is not numeric.")
        return int(self.value)

    @property
    def byte_order(self) -> ByteOrder:
        """Return the byte order of the instance."""
        return self._var.byte_order

    @byte_order.setter
    def byte_order(self, new_byte_order: bytes | ByteOrder) -> None:
        """Set the byte_order of the instance."""
        self._var.byte_order = ByteOrder(new_byte_order)

    @property
    def data(self) -> ByteString:
        """Return the byte representation of the instance."""
        return self._var.data

    @data.setter
    def data(self, new_data: bytes | bytearray | None = None) -> None:
        """Set the byte representation of the instance."""
        self._var.data = new_data

    @property
    def name(self) -> str:
        """Return the name of the instance."""
        try:
            return self._enum_cls(self.value).name
        except ValueError:
            return "UNKNOWN"

    @property
    def value(self) -> Any:
        """Return the value of the instance."""
        return self._var.value

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the value of the instance."""
        self._var.value = new_value

    def attach(self, new_data: ByteString, retain_value: bool = True) -> None:
        """Replace _var data and attach provided memoryview.

        Memoryview length must match byte length of fixed length type.
        """
        self._var.attach(new_data, retain_value)


setattr(ByteEnum, _BYTECLASS, True)
