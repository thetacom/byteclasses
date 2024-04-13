"""Unit tests for byteclasses primitive integer type constructors."""

import math
import operator

import pytest

from byteclasses.types.primitives.integers import Int8, UnderflowError, _FixedInt


def test_fixedint_missing_type_char_property():
    """Test _FixedInt instance with no `_type_char` class attribute."""

    class InvalidInt(_FixedInt):
        """Invalid Fixed Int Class definition."""

        _length = 1
        _signed = False

    with pytest.raises(NotImplementedError):
        _ = InvalidInt()


def test_fixedint_missing_length_property():
    """Test _FixedInt instance with no `_length` class attribute."""

    class InvalidInt(_FixedInt):
        """Invalid Fixed Int Class definition."""

        _type_char = b"b"
        _signed = False

    with pytest.raises(NotImplementedError):
        _ = InvalidInt()


def test_fixedint_missing_signed_property():
    """Test _FixedInt instance with no `_signed` class attribute."""

    class InvalidInt(_FixedInt):
        """Invalid Fixed Int Class definition."""

        _type_char: bytes = b"b"
        _length: int = 1

    with pytest.raises(NotImplementedError):
        _ = InvalidInt()


def test_int8_set_bad_value():
    """Test int8 set bad value."""
    with pytest.raises(NotImplementedError):
        _ = _FixedInt()


def test_int8_instance_properties():
    """Test int8 instance properties."""
    int8 = Int8(0)
    assert int8.signed is True
    assert int8.min == -128
    assert int8.max == 127
    assert int8.byte_order.value == b"@"
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


def test_int8_assign_non_int_value():
    """Test assignment with non-nteger value."""
    var1 = Int8()
    var1.value = 1.1
    assert var1.value == 1


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


def test_int8_attach_mv_no_retain():
    """Test attaching memoryview to int8 without retaining value."""
    test_mv = memoryview(bytearray(2))
    int8_1 = Int8(0x12)
    int8_2 = Int8(0x34)
    int8_1.attach(test_mv[:1], retain_value=False)
    int8_2.attach(test_mv[1:], retain_value=False)
    assert int8_1.value == 0x00
    assert int8_2.value == 0x00
    assert test_mv == b"\x00\x00"
    test_mv[:] = b"\x12\x34"
    assert int8_1.value == 0x12
    assert int8_2.value == 0x34


def test_int8_attach_mv_with_retain():
    """Test attaching memoryview to int8 while retaining value."""
    test_mv = memoryview(bytearray(3))
    int8_1 = Int8(0x12)
    int8_2 = Int8(0x34)
    int8_1.attach(test_mv[:1])
    int8_2.attach(test_mv[2:])
    assert int8_1.value == 0x12
    assert int8_2.value == 0x34
    assert test_mv == b"\x12\x00\x34"
    test_mv[:] = b"\x01\x00\x23"
    assert int8_1.value == 0x01
    assert int8_2.value == 0x23


def test_int8_int_dunder():
    """Test Int8 __int__ method."""
    var = Int8(8)
    assert int(var) == 8


def test_int8_truncate():
    """Test Int8 __trunc__ method."""
    var1 = Int8(10)
    result = math.trunc(var1)
    assert result == 10


def test_int8_index():
    """Test Int8 __index__ method."""
    var1 = Int8(10)
    result = operator.index(var1)
    assert result == 10
