"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import Int8, UnderflowError


def test_int8_instance_properties():
    """Test int8 instance properties."""
    int8 = Int8(0)
    assert int8.signed is True
    assert int8.min == -128
    assert int8.max == 127
    assert int8.byte_order == b"@"
    assert int8.endianness == "NATIVE"
    assert int8.fmt == b"@b"
    int8.value = 0
    assert int8 == 0
    int8.value = 1
    assert int8 == 1


def test_int8_bounds():
    """Test int8 bounds."""
    int8 = Int8()
    int8.value = 127
    assert int8 == 127
    with pytest.raises(OverflowError):
        int8.value = 128
    int8.value = -128
    assert int8 == -128
    with pytest.raises(UnderflowError):
        int8.value = -129


def test_int8_value_to_data():
    """Test int8 value to data."""
    int8 = Int8(0)
    assert int8.data == b"\x00"
    int8.value = 1
    assert int8.data == b"\x01"
    int8.value = 127
    assert int8.data == b"\x7f"
    int8.value = -128
    assert int8.data == b"\x80"
    int8.value = -1
    assert int8.data == b"\xff"


def test_int8_data_replacement():
    """Test replacement of int8 data."""
    test_mv = memoryview(bytearray(2))
    int8_1 = Int8(0x12)
    int8_2 = Int8(0x34)
    int8_1.data = test_mv[:1]
    int8_2.data = test_mv[1:]
    assert int8_1.value == 0x12
    assert int8_2.value == 0x34
    assert test_mv == b"\x12\x34"
    test_mv[:] = b"\x01\x23"
    assert int8_1.value == 0x01
    assert int8_2.value == 0x23
