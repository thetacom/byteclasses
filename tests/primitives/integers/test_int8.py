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
