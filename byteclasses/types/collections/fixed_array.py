"""Fixed length byte array types for binary data."""

from collections.abc import ByteString
from copy import deepcopy
from numbers import Number

from ...types._fixed_numeric_type import _FixedNumericType
from ...types._fixed_size_type import _FixedSizeType


class FixedArray:
    """An fixed length array of a fixed length item."""

    def __init__(
        self,
        item: _FixedSizeType,
        /,
        item_count: int,
    ) -> None:
        """Initialize a fixed length array.

        Args:
            item_type: The type of the items in the array.
            item_count: The number of items in array.
        """
        if not isinstance(item, _FixedSizeType):
            raise TypeError(f"Invalid item type: {item.__class__.__name__}")
        if item_count < 2:
            raise ValueError(f"Invalid item_count: {item_count}; must be >= 2")
        self._byte_order: bytes = item.byte_order
        self._type_char: bytes = item.type_char * item_count
        self._items = [deepcopy(item) for _ in range(item_count)]
        item_length = len(item)
        byte_length = item_length * item_count
        self._length = byte_length
        self._data = bytearray(byte_length)
        data_mv = memoryview(self._data)
        for i, idx in enumerate(range(0, self._length, item_length)):
            self._items[i].attach(data_mv[idx : idx + item_length])

    def __repr__(self) -> str:
        """Return string representation of fixed array."""
        return str(self._items)

    def __len__(self) -> int:
        """Return byte length of array."""
        return self._length

    def __bytes__(self) -> bytes:
        """Return array bytes."""
        return bytes(self._data)

    def __getitem__(self, key: int | slice) -> _FixedSizeType | list[_FixedSizeType]:
        """Implement getitem descriptor."""
        if isinstance(key, (int, slice)):
            return self._items[key]
        return NotImplemented

    def __setitem__(self, key: int | slice, value: ByteString | int | _FixedSizeType) -> None:
        """Implement setitem descriptor."""
        if isinstance(key, int):
            item = self._items[key]
            if isinstance(value, Number) and isinstance(item, _FixedNumericType):
                item.value = value
                self._items[key] = item
            elif isinstance(value, _FixedSizeType) and type(self._items[key] == type(value)):
                self._items[key].data = value.data
            elif isinstance(value, (bytes, bytearray)):
                self._items[key].data = value
            else:
                raise NotImplementedError
        elif isinstance(key, slice):
            for i in range(key.start, key.stop, key.step):
                item = self._items[i]
                if isinstance(value, Number) and isinstance(item, _FixedNumericType):
                    item.value = value
                    self._items[i] = item
                elif isinstance(value, _FixedSizeType) and type(self._items[i] == type(value)):
                    self._items[i].data = value.data
                elif isinstance(value, (bytes, bytearray)):
                    self._items[i].data = value
                else:
                    raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def data(self) -> bytes:
        """Return array data."""
        return bytes(self._data)

    @data.setter
    def data(self, new_data: ByteString) -> None:
        """Set array data."""
        if len(new_data) != self._length:
            raise ValueError(f"Invalid data length, expected {self._length}, receieved {len(new_data)}")
        self._data[:] = new_data
