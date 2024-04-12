"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import Int16, UnderflowError


def test_int16_instance_properties():
    """Test int16 instance properties."""
    int16 = Int16(0)
    assert int16.signed is True
    assert int16.min == -32768
    assert int16.max == 32767
    assert int16.byte_order.value == b"@"
    assert int16.endianness == "NATIVE"
    assert int16.fmt == b"@h"
    int16.value = 0
    assert int16 == 0
    int16.value = 1
    assert int16 == 1


def test_int16_bounds():
    """Test int16 bounds."""
    int16 = Int16()
    int16.value = 32767
    assert int16 == 32767
    with pytest.raises(OverflowError):
        int16.value = 32768
    int16.value = -32768
    assert int16 == -32768
    with pytest.raises(UnderflowError):
        int16.value = -32769


def test_int16_value_to_data():
    """Test int16 value to data."""
    int16 = Int16(0)
    assert int16.data == b"\x00\x00"
    int16.value = 1
    assert int16.data == b"\x01\x00"
    int16.value = 32767
    assert int16.data == b"\xff\x7f"
    int16.value = -32768
    assert int16.data == b"\x00\x80"
    int16.value = -1
    assert int16.data == b"\xff\xff"
