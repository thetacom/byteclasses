"""Unit tests for fixed integer logical operations."""

from numbers import Integral

import pytest

from byteclasses.types.primitives.integers import UInt8


def test_fixed_int_and_with_fixed_int():
    """Test logical AND between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 & integer2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixed_int_and_with_int():
    """Test logical AND between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer & 0x03
    assert isinstance(result, Integral)
    assert result == 0x01


def test_int_and_with_fixed_int():
    """Test logical AND between int and fixed length integer."""
    integer = UInt8(0x01)
    result = 0x03 & integer
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixed_int_and_unsupported():
    """Test logical AND between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer & "unsupported"


def test_fixed_int_or_with_fixed_int():
    """Test logical OR between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 | integer2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixed_int_or_with_int():
    """Test logical OR between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer | 0x03
    assert isinstance(result, Integral)
    assert result == 0x03


def test_int_or_with_fixed_int():
    """Test logical OR between int and fixed length integer."""
    integer = UInt8(0x01)
    result = 0x03 | integer
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixed_int_or_unsupported():
    """Test logical OR between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer | "unsupported"


def test_fixed_int_xor_with_fixed_int():
    """Test logical XOR between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 ^ integer2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_xor_with_int():
    """Test logical XOR between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer ^ 0x03
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_xor_unsupported():
    """Test logical XOR between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer ^ "unsupported"


def test_fixed_int_rxor_with_int():
    """Test logical reverse XOR between fixed length integer and int."""
    integer = UInt8(0x01)
    result = 0x03 ^ integer
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_rxor_unsupported():
    """Test logical reverse XOR between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = "unsupported" ^ integer


def test_fixed_int_invert():
    """Test logical not of fixed length integer."""
    integer = UInt8(0x01)
    result = ~integer
    assert isinstance(result, Integral)
    assert result == 0xFE


def test_fixed_int_left_shift():
    """Test left shift of fixed length integer."""
    integer = UInt8(0x01)
    result = integer << 1
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_left_shift_overflow():
    """Test left shift of fixed length integer with overflow."""
    integer = UInt8(0xFF)
    with pytest.raises(OverflowError):
        _ = UInt8(integer << 1)


def test_uint8_lshift_with_fixed_int():
    """Test UInt8 binary left shift."""
    var1 = UInt8(1)
    var2 = UInt8(1)
    result = var1 << var2
    assert result == 2


def test_uint8_lshift_with_unsupported():
    """Test UInt8 binary left shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = var1 << "unsupported"


def test_uint8_rlshift_with_int():
    """Test UInt8 binary reverse left shift."""
    var1 = UInt8(1)
    result = 1 << var1
    assert result == 2


def test_uint8_rlshift_with_unsupported():
    """Test UInt8 binary reverse left shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = "unsupported" << var1


def test_fixed_int_right_shift():
    """Test right shift of fixed length integer."""
    integer = UInt8(0x01)
    result = integer >> 1
    assert isinstance(result, Integral)
    assert result == 0x00


def test_uint8_rshift_with_int():
    """Test UInt8 binary right shift."""
    var1 = UInt8(2)
    result = var1 >> 1
    assert result == 1


def test_uint8_rshift_with_fixed_int():
    """Test UInt8 binary right shift."""
    var1 = UInt8(2)
    var2 = UInt8(1)
    result = var1 >> var2
    assert result == 1


def test_uint8_rshift_with_unsupported():
    """Test UInt8 binary right shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = var1 >> "unsupported"


def test_uint8_rrshift_with_int():
    """Test UInt8 binary reverse right shift."""
    var1 = UInt8(1)
    result = 2 >> var1
    assert result == 1


def test_uint8_rrshift_with_unsupported():
    """Test UInt8 binary reverse right shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = "unsupported" >> var1


def test_fixed_int_eq_with_fixed_int():
    """Test equality between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 == integer2
    assert isinstance(result, bool)
    assert result is False
    integer1 = UInt8(0x7F)
    integer2 = UInt8(0x7F)
    result = integer1 == integer2
    assert isinstance(result, bool)
    assert result is True


def test_fixed_int_eq_with_int():
    """Test equality between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer == 0x03
    assert isinstance(result, bool)
    assert result is False
    integer = UInt8(0x7F)
    result = integer == 0x7F
    assert isinstance(result, bool)
    assert result is True


def test_fixed_int_ne_with_fixed_int():
    """Test inequality between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 != integer2
    assert isinstance(result, bool)
    assert result is True
    integer1 = UInt8(0x7F)
    integer2 = UInt8(0x7F)
    result = integer1 != integer2
    assert isinstance(result, bool)
    assert result is False


def test_fixed_int_ne_with_int():
    """Test inequality between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer != 0x03
    assert isinstance(result, bool)
    assert result is True
    integer = UInt8(0x7F)
    result = integer != 0x7F
    assert isinstance(result, bool)
    assert result is False


def test_fixed_int_lt_with_fixed_int():
    """Test less than between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 < integer2
    assert isinstance(result, bool)
    assert result is True
    integer1 = UInt8(0x7F)
    integer2 = UInt8(0x7F)
    result = integer1 < integer2
    assert isinstance(result, bool)
    assert result is False


def test_fixed_int_lt_with_int():
    """Test less than between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer < 0x03
    assert isinstance(result, bool)
    assert result is True
    integer = UInt8(0x7F)
    result = integer < 0x7F
    assert isinstance(result, bool)
    assert result is False


def test_fixed_int_le_with_fixed_int():
    """Test less than or equal between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 <= integer2
    assert isinstance(result, bool)
    assert result is True
    integer1 = UInt8(0x7F)
    integer2 = UInt8(0x7F)
    result = integer1 <= integer2
    assert isinstance(result, bool)
    assert result is True


def test_fixed_int_le_with_int():
    """Test less than or equal between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer <= 0x03
    assert isinstance(result, bool)
    assert result is True
    integer = UInt8(0x7F)
    result = integer <= 0x7F
    assert isinstance(result, bool)
    assert result is True


def test_fixed_int_gt_with_fixed_int():
    """Test greater than between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 > integer2
    assert isinstance(result, bool)
    assert result is False
    integer1 = UInt8(0x7F)
    integer2 = UInt8(0x7F)
    result = integer1 > integer2
    assert isinstance(result, bool)
    assert result is False


def test_fixed_int_gt_with_int():
    """Test greater than between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer > 0x03
    assert isinstance(result, bool)
    assert result is False
    integer = UInt8(0x7F)
    result = integer > 0x7F
    assert isinstance(result, bool)
    assert result is False


def test_fixed_int_ge_with_fixed_int():
    """Test greater than or equal between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 >= integer2
    assert isinstance(result, bool)
    assert result is False
    integer1 = UInt8(0x7F)
    integer2 = UInt8(0x7F)
    result = integer1 >= integer2
    assert isinstance(result, bool)
    assert result is True


def test_fixed_int_ge_with_int():
    """Test greater than or equal between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer >= 0x03
    assert isinstance(result, bool)
    assert result is False
    integer = UInt8(0x7F)
    result = integer >= 0x7F
    assert isinstance(result, bool)
    assert result is True
