"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import UInt32, UnderflowError


def test_uint32_instance_properties():
    """Test uint32 instance properties."""
    uint32 = UInt32(0)
    assert uint32.signed is False
    assert uint32.min == 0
    assert uint32.max == 4294967295
    assert uint32.byte_order.value == b"@"
    assert uint32.endianness == "NATIVE"
    assert uint32.fmt == b"@I"
    uint32.value = 0
    assert uint32 == 0
    uint32.value = 1
    assert uint32 == 1


def test_uint32_bounds():
    """Test uint32 bounds."""
    uint32 = UInt32()
    uint32.value = 4294967295
    assert uint32 == 4294967295
    with pytest.raises(OverflowError):
        uint32.value = 4294967296
    uint32.value = 0
    assert uint32 == 0
    with pytest.raises(UnderflowError):
        uint32.value = -1


def test_uint32_value_to_data():
    """Test uint32 value to data."""
    uint32 = UInt32(0)
    assert uint32.data == b"\x00\x00\x00\x00"
    uint32.value = 1
    assert uint32.data == b"\x01\x00\x00\x00"
    uint32.value = 4294967295
    assert uint32.data == b"\xff\xff\xff\xff"
