"""Unit tests for byteclasses primitive integer type constructors."""

import math
import operator

import pytest

from byteclasses.types.primitives.integers import (
    Int8,
    Int16,
    Int32,
    Int64,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UnderflowError,
    _FixedInt,
)


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


def test_fixedint_create_with_invalid_value_type():
    """Test integer instantiation with invalid value type."""
    with pytest.raises(TypeError):
        _ = Int8("invalid")


def test_fixedint_create_with_value():
    """Test integer instantiation with value."""
    var = Int8(123)
    assert var == 123


def test_fixedint_create_with_bytes():
    """Test integer instantiation with bytes."""
    var = Int8(data=b"\x7f")
    assert var == 127


def test_fixedint_create_with_bytearray():
    """Test integer instantiation with bytearray."""
    var = Int8(data=bytearray(b"\x7f"))
    assert var == 127


def test_fixedint_create_with_memoryview():
    """Test integer instantiation with memoryview."""
    data = bytearray(b"\x7f")
    var = Int8(data=bytearray(memoryview(data)))
    assert var == 127


def test_fixedint_create_with_value_and_data():
    """Test integer instantiation with value and data."""
    with pytest.raises(ValueError):
        _ = Int8(1, data=b"\x7f")


def test_fixedint_assign_non_int_value():
    """Test assignment with non-nteger value."""
    var1 = Int8()
    var1.value = 1.1
    assert var1.value == 1


def test_fixedint_attach_data_mv_no_retain():
    """Test attaching external data memoryview to int8 without retaining value."""
    test_mv = memoryview(bytearray(2))
    int1 = Int8(0x12)
    int2 = Int8(0x34)
    int1.attach(test_mv[:1], retain_value=False)
    int2.attach(test_mv[1:], retain_value=False)
    assert int1.value == 0x00
    assert int2.value == 0x00
    assert test_mv == b"\x00\x00"
    test_mv[:] = b"\x12\x34"
    assert int1.value == 0x12
    assert int2.value == 0x34


def test_fixedint_attach_data_mv_with_retain():
    """Test attaching external data memoryview to integer while retaining value."""
    test_mv = memoryview(bytearray(3))
    int1 = Int8(0x12)
    int2 = Int8(0x34)
    int1.attach(test_mv[:1])
    int2.attach(test_mv[2:])
    assert int1.value == 0x12
    assert int2.value == 0x34
    assert test_mv == b"\x12\x00\x34"
    test_mv[:] = b"\x01\x00\x23"
    assert int1.value == 0x01
    assert int2.value == 0x23


def test_fixedint_attach_data_bytearray():
    """Test attaching external data bytearray to integer."""
    test_data = bytearray(3)
    int1 = Int8(0x12)
    int2 = Int8(0x34)
    int1.attach(test_data[:1])
    int2.attach(test_data[2:])
    assert int1.value == 0x12
    assert int2.value == 0x34
    assert test_data == b"\x00\x00\x00"
    test_data[:] = b"\x01\x00\x23"
    assert int1.value == 0x12
    assert int2.value == 0x34


def test_fixedint_attach_data_bytes():
    """Test attaching external data bytes to integer."""
    test_data = bytes(3)
    int1 = Int8(0x12)
    int2 = Int8(0x34)
    int1.attach(test_data[:1])
    int2.attach(test_data[2:])
    assert int1.value == 0x12
    assert int2.value == 0x34
    assert test_data == b"\x00\x00\x00"
    assert int1.value == 0x12
    assert int2.value == 0x34


def test_fixedint_str():
    """Test integer __str__ method."""
    var = Int8(8)
    assert str(var) == "8"


def test_fixedint_clear_data_with_data_none():
    """Test _FixedInt clearing data by setting data attribute to None."""
    var = Int8(8)
    assert var == 8
    var.data = None
    assert var.data == b"\x00"


def test_fixedint_set_partial_data():
    """Test _FixedInt set data with short data."""
    var = UInt32()
    var.value = var.max
    var.data = b"\x00\x00"
    assert var.data == b"\x00\x00\xff\xff"


def test_fixedint_set_oversized_data():
    """Test _FixedInt set data with oversized data."""
    var = UInt32()
    var.value = var.max
    with pytest.raises(ValueError):
        var.data = b"\x00\x00\x00\x00\x00"


def test_fixedint_repr():
    """Test integer __repr__ method."""
    var = Int8(8)
    assert repr(var) == "Int8(8)"


def test_fixedint_bytes():
    """Test integer __bytes__ method."""
    var = Int8(8)
    assert bytes(var) == b"\x08"


def test_fixedint_abs():
    """Test integer __abs__ method."""
    var = Int8(8)
    assert abs(var) == 8
    var.value = -8
    assert abs(var) == 8


def test_fixedint_bool():
    """Test integer __bool__ method."""
    var = Int8(8)
    assert bool(var) is True
    var.value = 0
    assert bool(var) is False


def test_fixedint_ceil():
    """Test integer __ceil__ method."""
    var = Int8(8)
    assert math.ceil(var) == 8


def test_fixedint_int():
    """Test integer __int__ method."""
    var = Int8(8)
    assert int(var) == 8


def test_fixedint_complex():
    """Test integer __complex__ method."""
    var1 = Int8(8)
    var2 = complex(var1)
    assert isinstance(var2, complex)
    assert var2.real == 8
    assert var2.imag == 0


def test_fixedint_eq_with_unsupported():
    """Test integer __eq__ method with unsupported."""
    var1 = Int8(8)
    var2 = "unsupported"
    assert var1 != var2


def test_fixedint_float():
    """Test integer __float__ method."""
    var1 = Int8(8)
    var2 = float(var1)
    assert isinstance(var2, float)
    assert var2 == 8.0


def test_fixedint_floor():
    """Test integer __floor__ method."""
    var1 = Int8(8)
    var2 = math.floor(var1)
    assert isinstance(var2, int)
    assert var2 == 8


def test_fixedint_hash():
    """Test integer __hash__ method."""
    var1 = Int8(8)
    var2 = Int8(9)
    assert isinstance(hash(var1), int)
    assert hash(var1) != hash(var2)


def test_fixedint_neg():
    """Test integer __neg__ method."""
    var1 = Int8(8)
    assert -var1 == -8


def test_fixedint_pos():
    """Test integer __pos__ method."""
    var1 = Int8(-8)
    assert +var1 == 8


def test_fixedint_round():
    """Test integer __round__ method."""
    var1 = Int8(8)
    assert round(var1) == 8
    var1.value = 111
    assert round(var1, 2) == 111


def test_fixedint_truncate():
    """Test _FixedInt __trunc__ method."""
    var1 = Int8(10)
    result = math.trunc(var1)
    assert result == 10


def test_fixedint_index():
    """Test _FixedInt __index__ method."""
    var1 = Int8(10)
    result = operator.index(var1)
    assert result == 10


# Check attributes of each fixed size integer


def test_int8_instance_properties():
    """Test int8 instance properties."""
    int8 = Int8(0)
    assert int8.signed is True
    assert int8.min == -128
    assert int8.max == 127
    assert int8.byte_order.value == b"@"
    assert int8.endianness == "NATIVE"
    assert int8.fmt == b"@b"
    assert int8.bit_length == 8
    assert len(int8) == 1
    int8.value = 0
    assert int8 == 0
    int8.value = 1
    assert int8 == 1


def test_int8_bounds():
    """Test int8 bounds."""
    int8 = Int8()
    assert int8.allow_overflow is False
    int8.value = 127
    assert int8 == 127
    with pytest.raises(OverflowError):
        int8.value = 128
    int8.value = -128
    assert int8 == -128
    with pytest.raises(UnderflowError):
        int8.value = -129


def test_int8_bounds_allow_overflow():
    """Test int8 bounds allow_overflow."""
    int8 = Int8(allow_overflow=True)
    assert int8.allow_overflow is True
    int8.value = 127
    assert int8 == 127
    int8.value = 128
    assert int8 == -128
    int8.value = -129
    assert int8 == 127


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


def test_uint8_instance_properties():
    """Test uint8 instance properties."""
    uint8 = UInt8(0)
    assert uint8.signed is False
    assert uint8.min == 0
    assert uint8.max == 255
    assert uint8.byte_order.value == b"@"
    assert uint8.endianness == "NATIVE"
    assert uint8.fmt == b"@B"
    assert uint8.bit_length == 8
    assert len(uint8) == 1
    uint8.value = 0
    assert uint8 == 0
    uint8.value = 1
    assert uint8 == 1


def test_uint8_bounds():
    """Test UInt8 bounds."""
    uint8 = UInt8()
    assert uint8.allow_overflow is False
    uint8.value = 255
    assert uint8 == 255
    with pytest.raises(OverflowError):
        uint8.value = 256
    uint8.value = 0
    assert uint8 == 0
    with pytest.raises(UnderflowError):
        uint8.value = -1


def test_uint8_bounds_allow_overflow():
    """Test uint8 bounds allow_overflow."""
    uint8 = UInt8(allow_overflow=True)
    assert uint8.allow_overflow is True
    uint8.value = 255
    assert uint8 == 255
    uint8.value = 256
    assert uint8 == 0
    uint8.value = -1
    assert uint8 == 255


def test_uint8_value_to_data():
    """Test UInt8 value to data."""
    uint8 = UInt8(0)
    assert uint8.data == b"\x00"
    uint8.value = 1
    assert uint8.data == b"\x01"
    uint8.value = 255
    assert uint8.data == b"\xff"
    uint8.value = 0
    assert uint8.data == b"\x00"


def test_int16_instance_properties():
    """Test Int16 instance properties."""
    int16 = Int16(0)
    assert int16.signed is True
    assert int16.min == -32768
    assert int16.max == 32767
    assert int16.byte_order.value == b"@"
    assert int16.endianness == "NATIVE"
    assert int16.fmt == b"@h"
    assert int16.bit_length == 16
    assert len(int16) == 2
    int16.value = 0
    assert int16 == 0
    int16.value = 1
    assert int16 == 1


def test_int16_bounds():
    """Test Int16 bounds."""
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
    """Test Int16 value to data."""
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


def test_uint16_instance_properties():
    """Test UInt16 instance properties."""
    uint16 = UInt16(0)
    assert uint16.signed is False
    assert uint16.min == 0
    assert uint16.max == 65535
    assert uint16.byte_order.value == b"@"
    assert uint16.endianness == "NATIVE"
    assert uint16.fmt == b"@H"
    assert uint16.bit_length == 16
    assert len(uint16) == 2
    uint16.value = 0
    assert uint16 == 0
    uint16.value = 1
    assert uint16 == 1


def test_uint16_bounds():
    """Test UInt16 bounds."""
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
    """Test UInt16 value to data."""
    uint16 = UInt16(0)
    assert uint16.data == b"\x00\x00"
    uint16.value = 1
    assert uint16.data == b"\x01\x00"
    uint16.value = 65535
    assert uint16.data == b"\xff\xff"


def test_int32_instance_properties():
    """Test Int32 instance properties."""
    int32 = Int32(0)
    assert int32.signed is True
    assert int32.min == -2147483648
    assert int32.max == 2147483647
    assert int32.byte_order.value == b"@"
    assert int32.endianness == "NATIVE"
    assert int32.fmt == b"@i"
    assert int32.bit_length == 32
    assert len(int32) == 4
    int32.value = 0
    assert int32 == 0
    int32.value = 1
    assert int32 == 1


def test_int32_bounds():
    """Test Int32 bounds."""
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
    """Test Int32 value to data."""
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


def test_uint32_instance_properties():
    """Test UInt32 instance properties."""
    uint32 = UInt32(0)
    assert uint32.signed is False
    assert uint32.min == 0
    assert uint32.max == 4294967295
    assert uint32.byte_order.value == b"@"
    assert uint32.endianness == "NATIVE"
    assert uint32.fmt == b"@I"
    assert uint32.bit_length == 32
    assert len(uint32) == 4
    uint32.value = 0
    assert uint32 == 0
    uint32.value = 1
    assert uint32 == 1


def test_uint32_bounds():
    """Test UInt32 bounds."""
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
    """Test UInt32 value to data."""
    uint32 = UInt32(0)
    assert uint32.data == b"\x00\x00\x00\x00"
    uint32.value = 1
    assert uint32.data == b"\x01\x00\x00\x00"
    uint32.value = 4294967295
    assert uint32.data == b"\xff\xff\xff\xff"


def test_int64_instance_properties():
    """Test Int64 instance properties."""
    int64 = Int64(0)
    assert int64.signed is True
    assert int64.min == -9223372036854775808
    assert int64.max == 9223372036854775807
    assert int64.byte_order.value == b"@"
    assert int64.endianness == "NATIVE"
    assert int64.fmt == b"@q"
    assert int64.bit_length == 64
    assert len(int64) == 8
    int64.value = 0
    assert int64 == 0
    int64.value = 1
    assert int64 == 1


def test_int64_bounds():
    """Test Int64 bounds."""
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
    """Test Int64 value to data."""
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


def test_uint64_instance_properties():
    """Test UInt64 instance properties."""
    uint64 = UInt64(0)
    assert uint64.signed is False
    assert uint64.min == 0
    assert uint64.max == 18446744073709551615
    assert uint64.byte_order.value == b"@"
    assert uint64.endianness == "NATIVE"
    assert uint64.fmt == b"@Q"
    assert uint64.bit_length == 64
    assert len(uint64) == 8
    uint64.value = 0
    assert uint64 == 0
    uint64.value = 1
    assert uint64 == 1


def test_uint64_bounds():
    """Test UInt64 bounds."""
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
    """Test UInt64 value to data."""
    uint64 = UInt64(0)
    assert uint64.data == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    uint64.value = 1
    assert uint64.data == b"\x01\x00\x00\x00\x00\x00\x00\x00"
    uint64.value = 18446744073709551615
    assert uint64.data == b"\xff\xff\xff\xff\xff\xff\xff\xff"
