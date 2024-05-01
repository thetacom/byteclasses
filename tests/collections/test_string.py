"""Test suite for Fixed Size String Byteclass."""

import pytest

from byteclasses.types import String

NULL_BYTE = b"\x00"


def test_string_creation():
    """Test String creation and properties."""
    expected_length = 8
    string = String(expected_length)
    assert isinstance(string, String)
    assert len(string) == expected_length


def test_string_creation_with_value():
    """Test String creation with initial value."""
    expected_length = 8
    string = String(expected_length, value="test")
    assert string.data == b"test\x00\x00\x00\x00"
    assert string.value == "test"


def test_string_creation_with_long_value():
    """Test String creation with long initial value."""
    expected_length = 8
    string = String(expected_length, value="longvalue")
    assert string.data == b"longval\x00"
    assert string.value == "longval"
    string = String(expected_length, value="longvalue", null_terminated=False)
    assert string.data == b"longvalu"
    assert string.value == "longvalu"


def test_string_creation_with_data():
    """Test String creation with initial data."""
    expected_length = 8
    string = String(expected_length, data=b"test\x00\x00\x00\x00")
    assert string.data == b"test\x00\x00\x00\x00"
    assert string.value == "test"


def test_string_creation_with_invalid_data():
    """Test String creation with invalid initial data."""
    expected_length = 8
    with pytest.raises(ValueError):
        _ = String(expected_length, data=b"test")


def test_string_creation_with_value_and_data():
    """Test String creation with initial value and data."""
    expected_length = 8
    with pytest.raises(ValueError):
        _ = String(expected_length, value="initial", data=b"value\x00\x00\x00")


def test_string_set_value():
    """Test String set value."""
    expected_length = 8
    string = String(expected_length, value="longvalue")
    string.value = "short"
    assert string.data == b"short\x00\x00\x00"
    assert string.value == "short"


def test_string_str_method():
    """Test String __str__ method"""
    expected_length = 8
    string = String(expected_length, value="test")
    assert str(string) == "test"


def test_string_repr_method():
    """Test String __repr__ method"""
    expected_length = 8
    string = String(expected_length, value="test")
    assert repr(string) == "String(8, value='test')"
