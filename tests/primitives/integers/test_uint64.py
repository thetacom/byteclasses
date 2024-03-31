"""Unit tests for byteclasses primitive integer type constructors."""

import pytest

from byteclasses.types.primitives.integers import UInt64, UnderflowError


def test_uint64_instance_properties():
    """Test uint64 instance properties."""
    uint64 = UInt64(0)
    assert uint64.signed is False
    assert uint64.min == 0
    assert uint64.max == 18446744073709551615
    assert uint64.byte_order == b"@"
    assert uint64.endianness == "NATIVE"
    assert uint64.fmt == b"@Q"
    uint64.value = 0
    assert uint64 == 0
    uint64.value = 1
    assert uint64 == 1


def test_uint64_bounds():
    """Test uint64 bounds."""
    uint64 = UInt64()
    uint64.value = 18446744073709551615
    assert uint64 == 18446744073709551615
    with pytest.raises(OverflowError):
        uint64.value = 18446744073709551616
    uint64.value = 0
    assert uint64 == 0
    with pytest.raises(UnderflowError):
        uint64.value = -1


def test_uint64_value_to_data():
    """Test uint64 value to data."""
    uint64 = UInt64(0)
    assert uint64.data == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    uint64.value = 1
    assert uint64.data == b"\x01\x00\x00\x00\x00\x00\x00\x00"
    uint64.value = 18446744073709551615
    assert uint64.data == b"\xff\xff\xff\xff\xff\xff\xff\xff"
