"""Test suite for ByteEnum class."""

from enum import IntEnum

import pytest

from byteclasses import ByteOrder
from byteclasses.types.primitives.byte_enum import ByteEnum
from byteclasses.types.primitives.integers import UInt8, UInt16, UInt32, UInt64

INT_CLASSES = [UInt8, UInt16, UInt32, UInt64]


class TestEnum(IntEnum):
    """IntEnum class for use in ByteEnum tests."""

    __test__ = False

    ZERO = 0
    ONE = 0b1
    TWO = 0x2
    FOUR = 0x4
    UINT8_MAX = 0xFF
    UINT16_MAX = 0xFFFF
    UINT32_MAX = 0xFFFFFFFF
    UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def test_byte_enum_creation():
    """Test ByteEnum Creation."""
    expected_len = 1
    expected_names = ["UINT8_MAX", "UINT16_MAX", "UINT32_MAX", "UINT64_MAX"]
    for int_cls, name in zip(INT_CLASSES, expected_names):
        var = ByteEnum(TestEnum, int_cls)
        assert isinstance(var, ByteEnum)
        assert var.value == 0
        assert len(var) == expected_len
        assert str(var) == "ZERO"
        assert repr(var) == "<TestEnum.ZERO: 0x0>"
        var.value = 3
        assert str(var) == "UNKNOWN"
        assert repr(var) == "<TestEnum.UNKNOWN: 0x3>"
        new_val = var._var.max  # pylint: disable=W0212
        var.value = new_val
        assert str(var) == name
        assert repr(var) == f"<TestEnum.{name}: {hex(new_val)}>"
        expected_len *= 2


def test_byte_enum_creation_invalid_params():
    """Test ByteEnum Creation with invalid params."""

    class BadEnum:
        """Bad Enum class."""

        ONE = "one"

    with pytest.raises(ValueError):
        _ = ByteEnum(BadEnum, UInt8)

    with pytest.raises(ValueError):
        _ = ByteEnum(TestEnum, int)


def test_byte_enum_creation_with_data():
    """Test ByteEnum Creation with data."""
    var = ByteEnum(TestEnum, UInt8, data=b"\x04")
    assert var.value == 4
    assert var.data == b"\x04"
    assert var.name == "FOUR"


def test_byte_enum_bytes_dunder():
    """Test ByteEnum __bytes__."""
    var = ByteEnum(TestEnum, UInt8, data=b"\x04")
    assert bytes(var) == b"\x04"


def test_byte_enum_str_dunder():
    """Test ByteEnum __str__."""
    var = ByteEnum(TestEnum, UInt8, data=b"\x04")
    assert str(var) == "FOUR"


def test_byte_enum_repr_dunder():
    """Test ByteEnum __repr__."""
    var = ByteEnum(TestEnum, UInt8, data=b"\x04")
    assert repr(var) == "<TestEnum.FOUR: 0x4>"


def test_byte_enum_byte_order():
    """Test ByteEnum byte_order property."""
    var = ByteEnum(TestEnum, UInt8)
    assert var.byte_order is ByteOrder.NATIVE
    var.byte_order = ByteOrder.NET
    assert var.byte_order is ByteOrder.NET


def test_byte_enum_attach():
    """Test ByteEnum attach."""
    data = bytearray(b"\x00\x00")
    var = ByteEnum(TestEnum, UInt16)
    var.attach(memoryview(data))
    var.value = TestEnum.UINT16_MAX.value
    assert data == b"\xff\xff"
    var.data = b"\xaa\xaa"
    assert data == b"\xaa\xaa"
