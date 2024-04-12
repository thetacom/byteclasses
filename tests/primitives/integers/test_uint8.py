"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import UInt8, UnderflowError


def test_uint8_instance_properties():
    """Test uint8 instance properties."""
    uint8 = UInt8(0)
    assert uint8.signed is False
    assert uint8.min == 0
    assert uint8.max == 255
    assert uint8.byte_order.value == b"@"
    assert uint8.endianness == "NATIVE"
    assert uint8.fmt == b"@B"
    uint8.value = 0
    assert uint8 == 0
    uint8.value = 1
    assert uint8 == 1


def test_uint8_bounds():
    """Test uint8 bounds."""
    uint8 = UInt8()
    uint8.value = 255
    assert uint8 == 255
    with pytest.raises(OverflowError):
        uint8.value = 256
    uint8.value = 0
    assert uint8 == 0
    with pytest.raises(UnderflowError):
        uint8.value = -1


def test_uint8_value_to_data():
    """Test uint8 value to data."""
    uint8 = UInt8(0)
    assert uint8.data == b"\x00"
    uint8.value = 1
    assert uint8.data == b"\x01"
    uint8.value = 255
    assert uint8.data == b"\xff"
    uint8.value = 0
    assert uint8.data == b"\x00"
