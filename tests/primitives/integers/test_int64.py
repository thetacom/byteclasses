"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import Int64, UnderflowError


def test_int64_instance_properties():
    """Test int64 instance properties."""
    int64 = Int64(0)
    assert int64.signed is True
    assert int64.min == -9223372036854775808
    assert int64.max == 9223372036854775807
    assert int64.byte_order.value == b"@"
    assert int64.endianness == "NATIVE"
    assert int64.fmt == b"@q"
    int64.value = 0
    assert int64 == 0
    int64.value = 1
    assert int64 == 1


def test_int64_bounds():
    """Test int64 bounds."""
    int64 = Int64()
    int64.value = 9223372036854775807
    assert int64 == 9223372036854775807
    with pytest.raises(OverflowError):
        int64.value = 9223372036854775808
    int64.value = -9223372036854775808
    assert int64 == -9223372036854775808
    with pytest.raises(UnderflowError):
        int64.value = -9223372036854775809


def test_int64_value_to_data():
    """Test int64 value to data."""
    int64 = Int64(0)
    assert int64.data == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    int64.value = 1
    assert int64.data == b"\x01\x00\x00\x00\x00\x00\x00\x00"
    int64.value = 9223372036854775807
    assert int64.data == b"\xff\xff\xff\xff\xff\xff\xff\x7f"
    int64.value = -9223372036854775808
    assert int64.data == b"\x00\x00\x00\x00\x00\x00\x00\x80"
    int64.value = -1
    assert int64.data == b"\xff\xff\xff\xff\xff\xff\xff\xff"
