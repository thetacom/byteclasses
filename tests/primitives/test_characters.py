"""Test suite for character primitives."""

import pytest

from byteclasses.types import UChar


def test_uchar_creation_no_value():
    """Test UChar creation."""
    var1 = UChar()
    assert len(var1) == 1
    assert var1.data == b"\x00"
    assert var1.value == "\x00"


def test_uchar_creation_with_value():
    """Test UChar creation with value."""
    var1 = UChar("A")
    assert len(var1) == 1
    assert var1.data == b"\x41"
    assert var1.value == "A"


def test_uchar_creation_with_invalid_value():
    """Test UChar creation with invalid value."""
    with pytest.raises(ValueError):
        _ = UChar("invalid")


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
