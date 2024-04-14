"""Fixed length byte array types for binary data."""

from collections.abc import ByteString
from copy import deepcopy
from numbers import Number

from ..._enums import ByteOrder
from ...types._fixed_numeric_type import _FixedNumericType
from ...types._fixed_size_type import _FixedSizeType
from .member import _MEMBERS


class FixedArray:
    """An fixed length array of a fixed length item."""

    def __init__(
        self,
        item: _FixedSizeType | type[_FixedSizeType],
        /,
        item_count: int,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
    ) -> None:
        """Initialize a fixed length array.

        Args:
            item_type: The type of the items in the array.
            item_count: The number of items in array.
        """
        self._byte_order: ByteOrder = ByteOrder(byte_order)
        if item_count < 2:
            raise ValueError(f"Invalid item_count: {item_count}; must be >= 2")
        if isinstance(item, _FixedSizeType):
            self._items: list[_FixedSizeType] = []
            for _ in range(item_count):
                new_item = deepcopy(item)
                new_item.byte_order = self._byte_order
                self._items.append(new_item)
            item_instance = item
        elif isinstance(item, type):
            if issubclass(item, _FixedSizeType):
                self._items = [item(byte_order=self._byte_order) for _ in range(item_count)]
            item_instance = self._items[0]
        else:
            raise TypeError(
                f"Invalid item type ({item.__class__.__name__}): Must be a FixedSizeType class or instance."
            )
        self._type_char: bytes = item_instance.type_char * item_count
        item_length = len(item_instance)
        byte_length = item_length * item_count
        self._length = byte_length
        self._data = memoryview(bytearray(byte_length))
        self._attach_members()

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

    def attach(self, mv: memoryview) -> None:
        """Attach memoryview to underlying data attribute."""
        if not isinstance(mv, memoryview):
            raise AttributeError("Only memoryviews can be attached to collection.")
        if len(mv) != len(self):
            raise AttributeError(f"Memoryview length ({len(mv)}) must match collection length ({len(self)}).")
        self._data = mv
        self._attach_members()

    def _attach_members(self) -> None:
        """Attach member items to internal data attribute."""
        item_length = len(self._items[0])
        for i, idx in enumerate(range(0, self._length, item_length)):
            self._items[i].attach(self._data[idx : idx + item_length])


setattr(FixedArray, _MEMBERS, [])
