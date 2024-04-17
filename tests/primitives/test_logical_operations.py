"""Unit tests for fixed integer logical operations."""

from numbers import Integral

import pytest

from byteclasses.types.primitives.integers import UInt8


def test_fixedint_and_with_fixed_int():
    """Test logical AND between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 & integer2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixedint_and_with_int():
    """Test logical AND between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer & 0x03
    assert isinstance(result, Integral)
    assert result == 0x01


def test_int_and_with_fixedint():
    """Test logical AND between int and fixed length integer."""
    integer = UInt8(0x01)
    result = 0x03 & integer
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixedint_and_unsupported():
    """Test logical AND between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer & "unsupported"


def test_fixedint_or_with_fixed_int():
    """Test logical OR between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 | integer2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixedint_or_with_int():
    """Test logical OR between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer | 0x03
    assert isinstance(result, Integral)
    assert result == 0x03


def test_int_or_with_fixedint():
    """Test logical OR between int and fixed length integer."""
    integer = UInt8(0x01)
    result = 0x03 | integer
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixedint_or_unsupported():
    """Test logical OR between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer | "unsupported"


def test_fixedint_xor_with_fixedint():
    """Test logical XOR between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x03)
    result = integer1 ^ integer2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_xor_with_int():
    """Test logical XOR between fixed length integer and int."""
    integer = UInt8(0x01)
    result = integer ^ 0x03
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_xor_unsupported():
    """Test logical XOR between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer ^ "unsupported"


def test_fixedint_rxor_with_int():
    """Test logical reverse XOR between fixed length integer and int."""
    integer = UInt8(0x01)
    result = 0x03 ^ integer
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_rxor_unsupported():
    """Test logical reverse XOR between fixed length integer and unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = "unsupported" ^ integer


def test_fixedint_invert():
    """Test logical not of fixed length integer."""
    integer = UInt8(0x01)
    result = ~integer
    assert isinstance(result, Integral)
    assert result == 0xFE


def test_fixedint_left_shift():
    """Test left shift of fixed length integer."""
    integer = UInt8(0x01)
    result = integer << 1
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_left_shift_overflow():
    """Test left shift of fixed length integer with overflow."""
    integer = UInt8(0xFF)
    with pytest.raises(OverflowError):
        _ = UInt8(integer << 1)


def test_fixedint_lshift_with_fixedint():
    """Test _FixedInt binary left shift."""
    var1 = UInt8(1)
    var2 = UInt8(1)
    result = var1 << var2
    assert result == 2


def test_fixedint_lshift_with_unsupported():
    """Test _FixedInt binary left shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = var1 << "unsupported"


def test_fixedint_rlshift_with_int():
    """Test _FixedInt binary reverse left shift."""
    var1 = UInt8(1)
    result = 1 << var1
    assert result == 2


def test_fixedint_rlshift_with_unsupported():
    """Test _FixedInt binary reverse left shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = "unsupported" << var1


def test_fixedint_right_shift():
    """Test right shift of _FixedInt."""
    integer = UInt8(0x01)
    result = integer >> 1
    assert isinstance(result, Integral)
    assert result == 0x00


def test_fixedint_rshift_with_int():
    """Test _FixedInt binary right shift."""
    var1 = UInt8(2)
    result = var1 >> 1
    assert result == 1


def test_fixedint_rshift_with_fixedint():
    """Test _FixedInt binary right shift."""
    var1 = UInt8(2)
    var2 = UInt8(1)
    result = var1 >> var2
    assert result == 1


def test_uint8_rshift_with_unsupported():
    """Test UInt8 binary right shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = var1 >> "unsupported"


def test_fixeding_rrshift_with_int():
    """Test _FixedInt binary reverse right shift."""
    var1 = UInt8(1)
    result = 2 >> var1
    assert result == 1


def test_fixedint_rrshift_with_unsupported():
    """Test _FixedInt binary reverse right shift."""
    var1 = UInt8(1)
    with pytest.raises(TypeError):
        _ = "unsupported" >> var1


def test_fixedint_eq_with_fixedint():
    """Test equality between two _FixedInts."""
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


def test_fixedint_eq_with_int():
    """Test equality between _FixedInt and int."""
    integer = UInt8(0x01)
    result = integer == 0x03
    assert isinstance(result, bool)
    assert result is False
    integer = UInt8(0x7F)
    result = integer == 0x7F
    assert isinstance(result, bool)
    assert result is True


def test_fixedint_ne_with_fixedint():
    """Test inequality between two _FixedInts."""
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


def test_fixedint_ne_with_int():
    """Test inequality between _FixedInt and int."""
    integer = UInt8(0x01)
    result = integer != 0x03
    assert isinstance(result, bool)
    assert result is True
    integer = UInt8(0x7F)
    result = integer != 0x7F
    assert isinstance(result, bool)
    assert result is False


def test_fixedint_lt_with_fixed_int():
    """Test less than between two _FixedInts."""
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


def test_fixedint_lt_with_int():
    """Test less than between _FixedInt and int."""
    integer = UInt8(0x01)
    result = integer < 0x03
    assert isinstance(result, bool)
    assert result is True
    integer = UInt8(0x7F)
    result = integer < 0x7F
    assert isinstance(result, bool)
    assert result is False


def test_fixedint_lt_with_unsupported():
    """Test less than between _FixedInt and an unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer < "invalid"


def test_fixedint_le_with_fixedint():
    """Test less than or equal between two _FixedInts."""
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


def test_fixedint_le_with_int():
    """Test less than or equal between _FixedInt and int."""
    integer = UInt8(0x01)
    result = integer <= 0x03
    assert isinstance(result, bool)
    assert result is True
    integer = UInt8(0x7F)
    result = integer <= 0x7F
    assert isinstance(result, bool)
    assert result is True


def test_fixedint_le_with_unsupported():
    """Test less than or equal between _FixedInt and an unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer <= "invalid"


def test_fixedint_gt_with_fixedint():
    """Test greater than between two _FixedInts."""
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


def test_fixedint_gt_with_int():
    """Test greater than between _FixedInt and int."""
    integer = UInt8(0x01)
    result = integer > 0x03
    assert isinstance(result, bool)
    assert result is False
    integer = UInt8(0x7F)
    result = integer > 0x7F
    assert isinstance(result, bool)
    assert result is False


def test_fixedint_gt_with_unsupported():
    """Test greater than between _FixedInt and an unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer > "invalid"


def test_fixedint_ge_with_fixedint():
    """Test greater than or equal between two _FixedInts."""
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


def test_fixedint_ge_with_int():
    """Test greater than or equal between _FixedInt and int."""
    integer = UInt8(0x01)
    result = integer >= 0x03
    assert isinstance(result, bool)
    assert result is False
    integer = UInt8(0x7F)
    result = integer >= 0x7F
    assert isinstance(result, bool)
    assert result is True


def test_fixedint_ge_with_unsupported():
    """Test greater than or equal between _FixedInt and an unsupported type."""
    integer = UInt8(0x01)
    with pytest.raises(TypeError):
        _ = integer >= "invalid"
