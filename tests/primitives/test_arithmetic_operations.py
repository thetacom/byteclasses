"""Unit tests for fixed integer arithmetic operations."""

from numbers import Integral

import pytest

from byteclasses.types.primitives.integers import UInt8, UnderflowError


def test_fixedint_add_to_fixedint():
    """Test add between two _PrimitiveInts."""
    var1 = UInt8(0x01)
    var2 = UInt8(0x02)
    result = var1 + var2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixedint_add_to_int():
    """Test add between a fixed length integer and an integer."""
    var1 = UInt8(0x01)
    var2 = 2
    result = var1 + var2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixedint_add_to_unsupported():
    """Test add between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x01)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var1 + var2


def test_fixedint_radd_to_int():
    """Test radd between a fixed length integer and an integer."""
    var1 = 1
    var2 = UInt8(0x02)
    result = var1 + var2
    assert isinstance(result, Integral)
    assert result == 0x03


def test_fixedint_radd_to_unsupported():
    """Test reverse add between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x01)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var2 + var1


def test_fixedint_add_to_fixedint_with_overflow():
    """Test add between two _PrimitiveInts with overflow."""
    var1 = UInt8(0xFF)
    var2 = UInt8(0x01)
    with pytest.raises(OverflowError):
        _ = UInt8(var1 + var2)


def test_fixedint_add_to_int_with_overflow():
    """Test add between a fixed length integer and an integer with overflow."""
    var1 = UInt8(0xFF)
    var2 = 1
    with pytest.raises(OverflowError):
        _ = UInt8(var1 + var2)


def test_fixedint_radd_to_int_with_overflow():
    """Test radd between a fixed length integer and an integer with overflow."""
    var1 = 255
    var2 = UInt8(0x01)
    with pytest.raises(OverflowError):
        _ = UInt8(var1 + var2)


def test_fixedint_sub_from_fixedint():
    """Test sub between two _PrimitiveInts."""
    var1 = UInt8(0x03)
    var2 = UInt8(0x02)
    result = var1 - var2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixedint_sub_from_fixedint_with_underflow():
    """Test sub between two _PrimitiveInts with underflow error."""
    var1 = UInt8(0x03)
    var2 = UInt8(0x02)
    with pytest.raises(UnderflowError):
        _ = UInt8(var2 - var1)


def test_fixedint_sub_with_int():
    """Test sub between a fixed length integer and an integer."""
    var1 = UInt8(0x03)
    var2 = 2
    result = var1 - var2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixedint_sub_with_unsupported_type():
    """Test sub between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x03)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var1 - var2


def test_fixedint_rsub_from_int():
    """Test rsub between a fixed length integer and an integer."""
    var1 = 3
    var2 = UInt8(0x02)
    result = var1 - var2
    assert isinstance(result, Integral)
    assert result == 0x01


def test_fixedint_rsub_with_unsupported_type():
    """Test reverse sub between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x03)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var2 - var1


def test_fixedint_rsub_from_int_with_underflow():
    """Test sub between two _PrimitiveInts with underflow."""
    var1 = 0x00
    var2 = UInt8(0x01)
    with pytest.raises(UnderflowError):
        _ = UInt8(var1 - var2)


def test_fixedint_sub_from_int_with_underflow():
    """Test sub between a fixed length integer and an integer with underflow."""
    var1 = UInt8(0x00)
    var2 = 1
    with pytest.raises(UnderflowError):
        _ = UInt8(var1 - var2)


def test_fixedint_rsub_from_int_with_overflow():
    """Test rsub between a fixed length integer and an integer with underflow."""
    var1 = 0
    var2 = UInt8(0x01)
    with pytest.raises(UnderflowError):
        _ = UInt8(var1 - var2)


def test_fixedint_mul_to_fixedint():
    """Test mul between two _PrimitiveInts."""
    var1 = UInt8(0x02)
    var2 = UInt8(0x08)
    result = var1 * var2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixedint_mul_to_int():
    """Test mul between a fixed length integer and an integer."""
    var1 = UInt8(0x02)
    var2 = 2
    result = var1 * var2
    assert isinstance(result, Integral)
    assert result == 0x04


def test_fixedint_mul_to_unsupported():
    """Test mul between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x02)
    var2 = complex(1, 1)
    with pytest.raises(TypeError):
        _ = var1 * var2


def test_fixedint_rmul_to_int():
    """Test rmul between a fixed length integer and an integer."""
    var1 = 2
    var2 = UInt8(0x02)
    result = var1 * var2
    assert isinstance(result, Integral)
    assert result == 0x04


def test_fixedint_rmul_to_str():
    """Test rmul between a fixed length integer and an str."""
    var1 = "A"
    var2 = UInt8(0x02)
    result = var1 * var2
    assert isinstance(result, str)
    assert result == "AA"


def test_fixedint_rmul_to_unsupported():
    """Test reverse mul between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x02)
    var2 = complex(1, 1)
    with pytest.raises(TypeError):
        _ = var2 * var1


def test_fixedint_mul_to_fixedint_with_overflow():
    """Test mul between two _PrimitiveInts with overflow."""
    var1 = UInt8(0xFF)
    var2 = UInt8(0x02)
    with pytest.raises(OverflowError):
        _ = UInt8(var1 * var2)


def test_fixedint_mul_to_int_with_overflow():
    """Test mul between a fixed length integer and an integer with overflow."""
    var1 = UInt8(0xFF)
    var2 = 2
    with pytest.raises(OverflowError):
        _ = UInt8(var1 * var2)


def test_fixedint_rmul_to_int_with_overflow():
    """Test rmul between a fixed length integer and an integer with overflow."""
    var1 = 255
    var2 = UInt8(0x02)
    with pytest.raises(OverflowError):
        _ = UInt8(var1 * var2)


def test_fixedint_truediv_with_fixedint():
    """Test truediv between two _PrimitiveInts."""
    var1 = UInt8(0x10)
    var2 = UInt8(0x08)
    result = var1 / var2
    assert result == 0x2


def test_fixedint_truediv_with_int():
    """Test truediv between a fixed length integer and an integer."""
    var1 = UInt8(0x10)
    var2 = 0x08
    result = var1 / var2
    assert result == 0x2


def test_fixedint_truediv_with_unsupported_type():
    """Test truediv between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x03)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var1 / var2


def test_fixedint_rtruediv_with_int():
    """Test reverse truediv between a fixed length integer and an integer."""
    var1 = 0x10
    var2 = UInt8(0x08)
    result = var1 / var2
    assert result == 0x2


def test_fixedint_rtruediv_with_unsupported_type():
    """Test reverse truediv between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x03)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var2 / var1


def test_fixedint_div_with_fixedint_with_div_error():
    """Test div between two _PrimitiveInts with division by zero error."""
    var1 = UInt8(0x01)
    var2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = var1 / var2


def test_fixedint_div_with_int_with_div_error():
    """Test div between a fixed length integer and an integer with div by zero error."""
    var1 = UInt8(0x01)
    var2 = 0
    with pytest.raises(ZeroDivisionError):
        _ = var1 / var2


def test_fixedint_rdiv_with_int_with_div_error():
    """Test rdiv between a fixed length integer and an integer with div by zero error."""
    var1 = 1
    var2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = var1 / var2


def test_fixedint_mod_with_fixedint():
    """Test mod between two _PrimitiveInts."""
    var1 = UInt8(0x10)
    var2 = UInt8(0x07)
    result = var1 % var2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_mod_with_int():
    """Test mod between a fixed length integer and an integer."""
    var1 = UInt8(0x10)
    var2 = 7
    result = var1 % var2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_mod_with_unsupported():
    """Test mod between a _PrimitiveInt and an unsupported type."""
    var1 = UInt8(0x5)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var1 % var2


def test_fixedint_rmod_with_int():
    """Test rmod between a fixed length integer and an integer."""
    var1 = 16
    var2 = UInt8(0x07)
    result = var1 % var2
    assert isinstance(result, Integral)
    assert result == 0x02


def test_fixedint_rmod_with_unsupported():
    """Test reverse mod between a _PrimitiveInt and an unsupported type."""
    var1 = UInt8(0x5)
    var2 = complex(1, 1)
    with pytest.raises(TypeError):
        _ = var2 % var1


def test_fixedint_mod_with_fixedint_with_div_error():
    """Test mod between two _PrimitiveInts with div by zero error."""
    var1 = UInt8(0x01)
    var2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = var1 % var2


def test_fixedint_mod_with_int_with_div_error():
    """Test mod between a fixed length integer and an integer with div by zero error."""
    var1 = UInt8(0x01)
    var2 = 0
    with pytest.raises(ZeroDivisionError):
        _ = var1 % var2


def test_fixedint_rmod_with_int_with_div_error():
    """Test rmod between a fixed length integer and an integer with div by zero error."""
    var1 = 1
    var2 = UInt8(0x00)
    with pytest.raises(ZeroDivisionError):
        _ = var1 % var2


def test_fixedint_divmod_with_fixedint():
    """Test divmod between two _PrimitiveInts."""
    var1 = UInt8(0x5)
    var2 = UInt8(0x2)
    quotient, remainder = divmod(var1, var2)
    assert quotient == 2
    assert remainder == 1


def test_fixedint_divmod_with_int():
    """Test divmod between a _PrimitiveInt and an int."""
    var1 = UInt8(0x5)
    var2 = 0x2
    quotient, remainder = divmod(var1, var2)
    assert quotient == 2
    assert remainder == 1


def test_fixedint_divmod_with_unsupported():
    """Test divmod between a _PrimitiveInt and an unsupported type."""
    var1 = UInt8(0x5)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = divmod(var1, var2)


def test_fixedint_rdivmod_with_int():
    """Test reverse divmod between a _PrimitiveInt and an int."""
    var1 = UInt8(0x2)
    var2 = 0x5
    quotient, remainder = divmod(var2, var1)
    assert quotient == 2
    assert remainder == 1


def test_fixedint_rdivmod_with_unsupported():
    """Test reverse divmod between a _PrimitiveInt and an unsupported type."""
    var1 = UInt8(0x5)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = divmod(var2, var1)


def test_fixedint_floordiv_with_fixedint():
    """Test floordiv between two _PrimitiveInts."""
    var1 = UInt8(0x5)
    var2 = UInt8(0x2)
    result = var1 // var2
    assert result == 2


def test_fixedint_floordiv_with_int():
    """Test floordiv between a _PrimitiveInt and an int."""
    var1 = UInt8(0x5)
    var2 = 0x2
    result = var1 // var2
    assert result == 2


def test_fixedint_floordiv_with_unsupported():
    """Test floordiv between a _PrimitiveInt and an unsupported type."""
    var1 = UInt8(0x5)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var1 // var2


def test_fixedint_rfloordiv_with_int():
    """Test reverse floordiv between a _PrimitiveInt and an int."""
    var1 = UInt8(0x2)
    var2 = 0x5
    result = var2 // var1
    assert result == 2


def test_fixedint_rfloordiv_with_unsupported():
    """Test reverse floordiv between a _PrimitiveInt and an unsupported type."""
    var1 = UInt8(0x5)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var2 // var1


def test_fixedint_pow_with_fixedint():
    """Test pow between two _PrimitiveInts."""
    var1 = UInt8(0x04)
    var2 = UInt8(0x02)
    result = var1**var2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixedint_pow_with_int():
    """Test pow between a fixed length integer and an integer."""
    var1 = UInt8(0x04)
    var2 = 2
    result = var1**var2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixedint_pow_with_unsupported_type():
    """Test pow between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x04)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var1**var2


def test_fixedint_rpow_with_int():
    """Test rpow between a fixed length integer and an integer."""
    var1 = 4
    var2 = UInt8(0x02)
    result = var1**var2
    assert isinstance(result, Integral)
    assert result == 0x10


def test_fixedint_rpow_with_unsupported_type():
    """Test reverse pow between a fixed length integer and an unsupported type."""
    var1 = UInt8(0x04)
    var2 = "invalid"
    with pytest.raises(TypeError):
        _ = var2**var1


def test_fixedint_pow_with_fixedint_with_overflow():
    """Test pow between two _PrimitiveInts with overflow."""
    var1 = UInt8(0xFF)
    var2 = UInt8(0xFF)
    with pytest.raises(OverflowError):
        _ = UInt8(var1**var2)


def test_fixedint_pow_with_int_with_overflow():
    """Test pow between a fixed length integer and an integer with overflow."""
    var1 = UInt8(0xFF)
    var2 = 255
    with pytest.raises(OverflowError):
        _ = UInt8(var1**var2)


def test_fixedint_rpow_with_int_with_overflow():
    """Test rpow between a fixed length integer and an integer with overflow."""
    var1 = 255
    var2 = UInt8(0xFF)
    with pytest.raises(OverflowError):
        _ = UInt8(var1**var2)
