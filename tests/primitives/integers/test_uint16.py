"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import UInt16, UnderflowError


def test_uint16_instance_properties():
    """Test uint16 instance properties."""
    uint16 = UInt16(0)
    assert uint16.signed is False
    assert uint16.min == 0
    assert uint16.max == 65535
    assert uint16.byte_order.value == b"@"
    assert uint16.endianness == "NATIVE"
    assert uint16.fmt == b"@H"
    uint16.value = 0
    assert uint16 == 0
    uint16.value = 1
    assert uint16 == 1


def test_uint16_bounds():
    """Test uint16 bounds."""
    uint16 = UInt16()
    uint16.value = 65535
    assert uint16 == 65535
    with pytest.raises(OverflowError):
        uint16.value = 65536
    uint16.value = 0
    assert uint16 == 0
    with pytest.raises(UnderflowError):
        uint16.value = -1


def test_uint16_value_to_data():
    """Test uint16 value to data."""
    uint16 = UInt16(0)
    assert uint16.data == b"\x00\x00"
    uint16.value = 1
    assert uint16.data == b"\x01\x00"
    uint16.value = 65535
    assert uint16.data == b"\xff\xff"
