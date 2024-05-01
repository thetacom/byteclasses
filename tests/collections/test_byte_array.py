"""Test suite for ByteArray Byteclass."""

from collections.abc import Iterator

import pytest

from byteclasses.types import ByteArray, UInt8, UInt16, UInt32, Word, structure

NULL_BYTE = b"\x00"


def test_byte_array_creation():
    """Test ByteArray creation and properties."""
    expected_count = 8
    expected_length = expected_count * len(UInt8())
    fa = ByteArray(expected_count)
    assert len(fa) == expected_count
    assert fa.data == NULL_BYTE * expected_length


def test_byte_array_creation_with_primitive_type():
    """Test ByteArray creation with primitive type."""
    expected_count = 8
    item_type = UInt32
    expected_length = expected_count * len(item_type())
    fa = ByteArray(expected_count, item_type)
    assert len(fa) == expected_length
    assert fa.data == NULL_BYTE * expected_length


def test_byte_array_creation_with_collection_type():
    """Test ByteArray creation with collection type."""

    @structure
    class TestStruct:
        """Test Structure."""

        item1: UInt8

    expected_count = 8
    item_type = TestStruct
    expected_length = expected_count * len(item_type())
    fa = ByteArray(expected_count, item_type)
    assert len(fa) == expected_length
    assert fa.data == NULL_BYTE * expected_length


def test_byte_array_creation_with_invalid_count():
    """Test ByteArray creation with invalid count."""
    with pytest.raises(ValueError):
        _ = ByteArray(1, UInt8)


def test_byte_array_creation_with_invalid_type():
    """Test ByteArray creation with invalid type."""
    with pytest.raises(TypeError):
        _ = ByteArray(2, int)


def test_byte_array_creation_with_primitive_instance():
    """Test ByteArray creation with primitive instance."""
    with pytest.raises(TypeError):
        _ = ByteArray(2, UInt8())


def test_byte_array_repr_dunder():
    """Test ByteArray __repr__ method."""
    var = ByteArray(2, UInt8)
    assert repr(var) == "ByteArray(2, UInt8)"


def test_byte_array_str_dunder():
    """Test ByteArray __str__ method."""
    var = ByteArray(2, UInt8)
    assert str(var) == "(UInt8(0), UInt8(0))"


def test_byte_array_bytes_dunder():
    """Test ByteArray __bytes__ method."""
    var = ByteArray(2, UInt8)
    assert bytes(var) == b"\x00\x00"


def test_byte_array_iter_dunder():
    """Test ByteArray __iter__ method."""
    var = ByteArray(2, UInt8)
    iterator = iter(var)
    assert isinstance(iterator, Iterator)


def test_byte_array_getitem_with_int():
    """Test ByteArray __getitem__ method with int key."""
    var = ByteArray(2, UInt8)
    item = var[1]
    assert isinstance(item, UInt8)


def test_byte_array_getitem_with_slice():
    """Test ByteArray __getitem__ method with slice key."""
    var = ByteArray(2, UInt8)
    items = var[0:1]
    assert isinstance(items, tuple)
    assert len(items) == 1


def test_byte_array_getitem_with_unsupported():
    """Test ByteArray __getitem__ method with unsupported key."""
    var = ByteArray(2, UInt8)
    with pytest.raises(NotImplementedError):
        _ = var["invalid"]


def test_byte_array_setitem_with_int_and_int():
    """Test ByteArray __setitem__ with int key and int value."""
    var = ByteArray(2, UInt8)
    assert var.data == b"\x00\x00"
    var[1] = 1
    assert var.data == b"\x00\x01"


def test_byte_array_setitem_with_int_and_generic():
    """Test ByteArray __setitem__ with int key and generic value."""
    var = ByteArray(2, UInt16)
    assert var.data == b"\x00\x00\x00\x00"
    var[1] = Word(b"\x00\x01")
    assert var.data == b"\x00\x00\x00\x01"


def test_byte_array_setitem_with_int_and_byte():
    """Test ByteArray __setitem__ with int key and byte value."""
    var = ByteArray(2, UInt8)
    assert var.data == b"\x00\x00"
    var[1] = b"\x01"
    assert var.data == b"\x00\x01"


def test_byte_array_setitem_with_int_and_byteclass():
    """Test ByteArray __setitem__ with int key and byteclass value."""
    var = ByteArray(2, UInt8)
    assert var.data == b"\x00\x00"
    var[1] = UInt32(1)
    assert var.data == b"\x00\x01"


def test_byte_array_setitem_with_int_and_unsupported():
    """Test ByteArray __setitem__ with int key and unsupported value."""
    var = ByteArray(2, UInt8)
    with pytest.raises(NotImplementedError):
        var[1] = "invalid"


def test_byte_array_setitem_with_slice_and_int():
    """Test ByteArray __setitem__ with slice key and int value."""
    var = ByteArray(3, UInt8)
    assert var.data == b"\x00\x00\x00"
    var[:] = 1
    assert var.data == b"\x01\x01\x01"
    var[1:] = 2
    assert var.data == b"\x01\x02\x02"
    var[1:2] = 3
    assert var.data == b"\x01\x03\x02"
    var[::2] = 4
    assert var.data == b"\x04\x03\x04"


def test_byte_array_setitem_with_slice_and_byte():
    """Test ByteArray __setitem__ with slice key and byte value."""
    var = ByteArray(3, UInt8)
    assert var.data == b"\x00\x00\x00"
    var[1:] = b"\x01"
    assert var.data == b"\x00\x01\x01"


def test_byte_array_setitem_with_slice_and_byteclass_number():
    """Test ByteArray __setitem__ with slice key and byteclass number."""
    var = ByteArray(3, UInt8)
    assert var.data == b"\x00\x00\x00"
    var[1:] = UInt8(1)
    assert var.data == b"\x00\x01\x01"


def test_byte_array_setitem_with_slice_and_iterable():
    """Test ByteArray __setitem__ with slice key and iterable."""
    var = ByteArray(3, UInt8)
    assert var.data == b"\x00\x00\x00"
    var[1:] = [1, 2]
    assert var.data == b"\x00\x01\x02"


def test_byte_array_setitem_with_slice_and_not_implemented():
    """Test ByteArray __setitem__ with slice key and not implemented."""
    var = ByteArray(3, UInt8)
    with pytest.raises(NotImplementedError):
        var[1:] = "invalid"


def test_byte_array_setitem_with_not_implemented():
    """Test ByteArray __setitem__ with not implemented key type."""
    var = ByteArray(3, UInt8)
    with pytest.raises(NotImplementedError):
        var["invalid"] = 1


def test_byte_array_set_data_with_short_data():
    """Test ByteArray set data with short data."""
    var = ByteArray(3, UInt8)
    with pytest.raises(ValueError):
        var.data = b"\x00"


def test_byte_array_set_data():
    """Test ByteArray set data."""
    var = ByteArray(3, UInt8)
    var.data = b"\x00\x00\xff"
    assert var.data == b"\x00\x00\xff"


def test_byte_array_items_property():
    """Test ByteArray items property."""
    var = ByteArray(3, UInt8)
    items = var.items
    assert isinstance(items, tuple)
    assert len(items) == 3
    assert isinstance(items[0], UInt8)


def test_byte_array_attach_with_bytes():
    """Test ByteArray attach method with bytes."""
    data = b"\x00\x01\x02\x04"
    var = ByteArray(3, UInt8)
    with pytest.raises(AttributeError):
        var.attach(data)


def test_byte_array_attach_with_bytearray():
    """Test ByteArray attach method with bytearray."""
    data = bytearray(b"\x00\x01\x02\x04")
    var = ByteArray(3, UInt8)
    with pytest.raises(AttributeError):
        var.attach(data[:3])


def test_byte_array_attach_with_memoryview():
    """Test ByteArray attach method with memoryview."""
    data = bytearray(b"\x00\x01\x02\x04")
    mv = memoryview(data)
    var = ByteArray(3, UInt8)
    with pytest.raises(AttributeError):
        var.attach(mv)
    var.attach(mv[:3])
    var[:] = 5
    assert data == b"\x05\x05\x05\x04"
