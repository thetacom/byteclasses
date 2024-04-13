"""Test suite for character primitives."""

import pytest

from byteclasses.types.primitives.characters import UChar


def test_uchar_instantiation():
    """Test UChar instantiation."""
    var1 = UChar()
    assert len(var1) == 1
    assert var1.data == b"\x00"
    assert var1.value == "\x00"


def test_uchar_str_method():
    """Test UChar __str__ method."""
    var1 = UChar()
    assert str(var1) == "\x00"


def test_uchar_repr_method():
    """Test UChar __repr__ method."""
    var1 = UChar()
    assert repr(var1) == "UChar('\\x00')"


def test_uchar_set_invalid_value():
    """Test set invalid UChar value."""
    var1 = UChar()
    with pytest.raises(ValueError):
        var1.value = ""
