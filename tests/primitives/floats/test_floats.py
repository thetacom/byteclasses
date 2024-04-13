"""Fixed Size Float Test Suite."""

import pytest

from byteclasses.types.primitives.floats import Double, Float, Float16, Float32, Float64, Half


def test_float16():
    """Test Float16 instantiation."""
    var = Float16()
    assert var == 0
    assert len(var) == 2
    assert var.data == b"\x00\x00"
    assert Float16 == Half


def test_float32():
    """Test Float32 instantiation."""
    var = Float32()
    assert var == 0
    assert len(var) == 4
    assert var.data == b"\x00\x00\x00\x00"
    assert Float32 == Float


def test_float64():
    """Test Float64 instantiation."""
    var = Float64()
    assert var == 0
    assert len(var) == 8
    assert var.data == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert Float64 == Double


def test_get_float_value():
    """Test getting float value using `float` attribute."""
    var = Float()
    assert var.value == 0.0


def test_set_float_value():
    """Test setting float value using `float` attribute."""
    var = Float()
    assert var.data == b"\x00\x00\x00\x00"
    var.value = 1.0
    assert var.data == b"\x00\x00\x80\x3f"


def test_set_float_invalid_value_type():
    """Test setting invalid value type."""
    var = Float()
    with pytest.raises(TypeError):
        var.value = "invalid"


def test_set_float_value_from_fixed_numeric():
    """Test setting value to fixed numeric type."""
    var1 = Float16(0)
    var2 = Float32(2)
    var1.value = var2
    assert var1.value == 2
