"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import Int32, UnderflowError


def test_int32_instance_properties():
    """Test int32 instance properties."""
    int32 = Int32(0)
    assert int32.signed is True
    assert int32.min == -2147483648
    assert int32.max == 2147483647
    assert int32.byte_order == b"@"
    assert int32.endianness == "NATIVE"
    assert int32.fmt == b"@i"
    int32.value = 0
    assert int32 == 0
    int32.value = 1
    assert int32 == 1


def test_int32_bounds():
    """Test int32 bounds."""
    int32 = Int32()
    int32.value = 2147483647
    assert int32 == 2147483647
    with pytest.raises(OverflowError):
        int32.value = 2147483648
    int32.value = -2147483648
    assert int32 == -2147483648
    with pytest.raises(UnderflowError):
        int32.value = -2147483649


def test_int32_value_to_data():
    """Test int32 value to data."""
    int32 = Int32(0)
    assert int32.data == b"\x00\x00\x00\x00"
    int32.value = 1
    assert int32.data == b"\x01\x00\x00\x00"
    int32.value = 2147483647
    assert int32.data == b"\xff\xff\xff\x7f"
    int32.value = -2147483648
    assert int32.data == b"\x00\x00\x00\x80"
    int32.value = -1
    assert int32.data == b"\xff\xff\xff\xff"
