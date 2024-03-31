"""Unit tests for fixed integer arithmetic operations."""

from numbers import Integral

import pytest

from byteclasses.types.primitives.integers import UInt8, UnderflowError


def test_fixed_int_add_to_fixed_int():
    """Test add between two fixed length integers."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x02)
    result = integer1 + integer2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixed_int_add_to_int():
    """Test add between a fixed length integer and an integer."""
    integer1 = UInt8(0x01)
    integer2 = 2
    result = integer1 + integer2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixed_int_radd_to_int():
    """Test radd between a fixed length integer and an integer."""
    integer1 = 1
    integer2 = UInt8(0x02)
    result = integer1 + integer2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixed_int_add_to_fixed_int_with_overflow():
    """Test add between two fixed length integers with overflow."""
    integer1 = UInt8(0xFF)
    integer2 = UInt8(0x01)
    with pytest.raises(OverflowError):
        _ = UInt8(integer1 + integer2)


def test_fixed_int_add_to_int_with_overflow():
    """Test add between a fixed length integer and an integer with overflow."""
    integer1 = UInt8(0xFF)
    integer2 = 1
    with pytest.raises(OverflowError):
        _ = UInt8(integer1 + integer2)


def test_fixed_int_radd_to_int_with_overflow():
    """Test radd between a fixed length integer and an integer with overflow."""
    integer1 = 255
    integer2 = UInt8(0x01)
    with pytest.raises(OverflowError):
        _ = UInt8(integer1 + integer2)


def test_fixed_int_sub_from_fixed_int():
    """Test sub between two fixed length integers."""
    integer1 = UInt8(0x03)
    integer2 = UInt8(0x02)
    result = integer1 - integer2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixed_int_sub_from_fixed_int_with_underflow():
    """Test sub between two fixed length integers with underflow error."""
    integer1 = UInt8(0x03)
    integer2 = UInt8(0x02)
    with pytest.raises(UnderflowError):
        _ = UInt8(integer2 - integer1)


def test_fixed_int_sub_from_int():
    """Test sub between a fixed length integer and an integer."""
    integer1 = UInt8(0x03)
    integer2 = 2
    result = integer1 - integer2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixed_int_rsub_from_int():
    """Test rsub between a fixed length integer and an integer."""
    integer1 = 3
    integer2 = UInt8(0x02)
    result = integer1 - integer2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixed_int_rsub_from_int_with_underflow():
    """Test sub between two fixed length integers with underflow."""
    integer1 = 0x00
    integer2 = UInt8(0x01)
    with pytest.raises(UnderflowError):
        _ = UInt8(integer1 - integer2)


def test_fixed_int_sub_from_int_with_underflow():
    """Test sub between a fixed length integer and an integer with underflow."""
    integer1 = UInt8(0x00)
    integer2 = 1
    with pytest.raises(UnderflowError):
        _ = UInt8(integer1 - integer2)


def test_fixed_int_rsub_from_int_with_overflow():
    """Test rsub between a fixed length integer and an integer with underflow."""
    integer1 = 0
    integer2 = UInt8(0x01)
    with pytest.raises(UnderflowError):
        _ = UInt8(integer1 - integer2)


def test_fixed_int_mul_to_fixed_int():
    """Test mul between two fixed length integers."""
    integer1 = UInt8(0x02)
    integer2 = UInt8(0x08)
    result = integer1 * integer2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixed_int_mul_to_int():
    """Test mul between a fixed length integer and an integer."""
    integer1 = UInt8(0x02)
    integer2 = 2
    result = integer1 * integer2
    assert isinstance(result, Integral)
    assert result == 0x04


def test_fixed_int_rmul_to_int():
    """Test rmul between a fixed length integer and an integer."""
    integer1 = 2
    integer2 = UInt8(0x02)
    result = integer1 * integer2
    assert isinstance(result, Integral)
    assert result == 0x04


def test_fixed_int_mul_to_fixed_int_with_overflow():
    """Test mul between two fixed length integers with overflow."""
    integer1 = UInt8(0xFF)
    integer2 = UInt8(0x02)
    with pytest.raises(OverflowError):
        _ = UInt8(integer1 * integer2)


def test_fixed_int_mul_to_int_with_overflow():
    """Test mul between a fixed length integer and an integer with overflow."""
    integer1 = UInt8(0xFF)
    integer2 = 2
    with pytest.raises(OverflowError):
        _ = UInt8(integer1 * integer2)


def test_fixed_int_rmul_to_int_with_overflow():
    """Test rmul between a fixed length integer and an integer with overflow."""
    integer1 = 255
    integer2 = UInt8(0x02)
    with pytest.raises(OverflowError):
        _ = UInt8(integer1 * integer2)


def test_fixed_int_div_with_fixed_int():
    """Test div between two fixed length integers."""
    integer1 = UInt8(0x10)
    integer2 = UInt8(0x08)
    result = integer1 / integer2
    assert result == 0x2


def test_fixed_int_div_with_int():
    """Test div between a fixed length integer and an integer."""
    integer1 = UInt8(0x10)
    integer2 = 0x08
    result = integer1 / integer2
    assert result == 0x2


def test_fixed_int_rdiv_with_int():
    """Test rdiv between a fixed length integer and an integer."""
    integer1 = 0x10
    integer2 = UInt8(0x08)
    result = integer1 / integer2
    assert result == 0x2


def test_fixed_int_div_with_fixed_int_with_div_error():
    """Test div between two fixed length integers with division by zero error."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = integer1 / integer2


def test_fixed_int_div_with_int_with_div_error():
    """Test div between a fixed length integer and an integer with div by zero error."""
    integer1 = UInt8(0x01)
    integer2 = 0
    with pytest.raises(ZeroDivisionError):
        _ = integer1 / integer2


def test_fixed_int_rdiv_with_int_with_div_error():
    """Test rdiv between a fixed length integer and an integer with div by zero error."""
    integer1 = 1
    integer2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = integer1 / integer2


def test_fixed_int_mod_with_fixed_int():
    """Test mod between two fixed length integers."""
    integer1 = UInt8(0x10)
    integer2 = UInt8(0x07)
    result = integer1 % integer2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_mod_with_int():
    """Test mod between a fixed length integer and an integer."""
    integer1 = UInt8(0x10)
    integer2 = 7
    result = integer1 % integer2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_rmod_with_int():
    """Test rmod between a fixed length integer and an integer."""
    integer1 = 16
    integer2 = UInt8(0x07)
    result = integer1 % integer2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixed_int_mod_with_fixed_int_with_div_error():
    """Test mod between two fixed length integers with div by zero error."""
    integer1 = UInt8(0x01)
    integer2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = integer1 % integer2


def test_fixed_int_mod_with_int_with_div_error():
    """Test mod between a fixed length integer and an integer with div by zero error."""
    integer1 = UInt8(0x01)
    integer2 = 0
    with pytest.raises(ZeroDivisionError):
        _ = integer1 % integer2


def test_fixed_int_rmod_with_int_with_div_error():
    """Test rmod between a fixed length integer and an integer with div by zero error."""
    integer1 = 1
    integer2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = integer1 % integer2


def test_fixed_int_pow_with_fixed_int():
    """Test pow between two fixed length integers."""
    integer1 = UInt8(0x04)
    integer2 = UInt8(0x02)
    result = integer1**integer2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixed_int_pow_with_int():
    """Test pow between a fixed length integer and an integer."""
    integer1 = UInt8(0x04)
    integer2 = 2
    result = integer1**integer2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixed_int_rpow_with_int():
    """Test rpow between a fixed length integer and an integer."""
    integer1 = 4
    integer2 = UInt8(0x02)
    result = integer1**integer2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixed_int_pow_with_fixed_int_with_overflow():
    """Test pow between two fixed length integers with overflow."""
    integer1 = UInt8(0xFF)
    integer2 = UInt8(0xFF)
    with pytest.raises(OverflowError):
        _ = UInt8(integer1**integer2)


def test_fixed_int_pow_with_int_with_overflow():
    """Test pow between a fixed length integer and an integer with overflow."""
    integer1 = UInt8(0xFF)
    integer2 = 255
    with pytest.raises(OverflowError):
        _ = UInt8(integer1**integer2)


def test_fixed_int_rpow_with_int_with_overflow():
    """Test rpow between a fixed length integer and an integer with overflow."""
    integer1 = 255
    integer2 = UInt8(0xFF)
    with pytest.raises(OverflowError):
        _ = UInt8(integer1**integer2)
