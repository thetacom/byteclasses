"""Fixed length byte array types for binary data."""

from collections.abc import ByteString, Iterable, Iterator
from numbers import Number
from typing import overload

from ..._enums import ByteOrder
from ...constants import _BYTECLASS, _MEMBERS
from ...types._fixed_numeric_type import _FixedNumericType
from ...types._fixed_size_type import _FixedSizeType
from ...util import is_byteclass, is_byteclass_collection
from ..primitives.integers import UInt8


class FixedArray:
    """An fixed length array of a fixed length item."""

    def __init__(
        self,
        item_count: int,
        item_type: type = UInt8,
        /,
        *,
        byte_order: bytes | ByteOrder = ByteOrder.NATIVE,
    ) -> None:
        """Initialize a fixed length array.

        Args:
            item_count: The number of items in array.
            item_type: The type of the items in the array. Default: UInt8
        """
        self._byte_order: ByteOrder = ByteOrder(byte_order)
        if item_count < 2:
            raise ValueError(f"Invalid item_count: {item_count}; must be >= 2")
        if not isinstance(item_type, type):
            raise TypeError("Invalid item_type must be a Byteclass not an instance.")
        if not is_byteclass(item_type):
            raise TypeError(
                f"Invalid item type {item_type.__name__}({item_type.__class__.__name__}): Must be a Byteclass type."
            )
        if is_byteclass_collection(item_type):
            self._items: tuple[_FixedSizeType] = tuple(item_type() for _ in range(item_count))
        else:
            self._items = tuple(item_type(byte_order=self._byte_order) for _ in range(item_count))
        item_instance = self._items[0]
        item_length = len(item_instance)
        offset = 0
        for item in self._items:
            item.offset = offset
            offset += item_length
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

    def __iter__(self) -> Iterator:
        """Return an item iterator."""
        return iter(self._items)

    @overload
    def __getitem__(self, key: int) -> _FixedSizeType: ...

    @overload
    def __getitem__(self, key: slice) -> tuple[_FixedSizeType]: ...

    def __getitem__(self, key: int | slice) -> _FixedSizeType | tuple[_FixedSizeType]:
        """Implement getitem descriptor."""
        if isinstance(key, (int, slice)):
            return self._items[key]
        return NotImplemented

    def __setitem__(self, key: int | slice, value: ByteString | int | _FixedSizeType) -> None:  # pylint: disable=R0912
        """Implement setitem descriptor."""
        if isinstance(key, int):
            item = self._items[key]
            if isinstance(value, Number) and isinstance(item, _FixedNumericType):
                self._items[key].value = value
            elif isinstance(value, _FixedSizeType) and type(self._items[key] == type(value)):
                self._items[key].data = value.data
            elif isinstance(value, (bytes, bytearray)):
                self._items[key].data = value
            else:
                raise NotImplementedError
        elif isinstance(key, slice):
            step = 1 if key.step is None else key.step
            if key.start is None:
                start = 0 if step > 0 else self._length - 1
            else:
                start = key.start
            if key.stop is None:
                stop = self._length if step > 0 else -1
            else:
                stop = key.stop
            for i in range(start, stop, step):
                item = self._items[i]
                if isinstance(value, Number) and isinstance(item, _FixedNumericType):
                    item.value = value
                elif isinstance(item, _FixedNumericType) and isinstance(value, Iterable):
                    item.value = value[i]
                elif isinstance(value, _FixedSizeType) and type(self._items[i] == type(value)):
                    item.data = value.data
                elif isinstance(value, (bytes, bytearray)):
                    item.data = value
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

    @property
    def item_count(self) -> int:
        """Return array item count."""
        return len(self._items)

    @property
    def items(self) -> tuple:
        """Return array item count."""
        return self._items

    def attach(self, mv: memoryview, retain_value: bool = False) -> None:
        """Attach memoryview to underlying data attribute."""
        if not isinstance(mv, memoryview):
            raise AttributeError("Only memoryviews can be attached to collection.")
        if len(mv) != len(self):
            raise AttributeError(f"Memoryview length ({len(mv)}) must match collection length ({len(self)}).")
        self._data = mv
        self._attach_members(retain_value)

    def _attach_members(self, retain_value: bool = True) -> None:
        """Attach member items to internal data attribute."""
        item_length = len(self._items[0])
        for i, idx in enumerate(range(0, self._length, item_length)):
            self._items[i].attach(self._data[idx : idx + item_length], retain_value)


setattr(FixedArray, _BYTECLASS, True)
setattr(FixedArray, _MEMBERS, [])
