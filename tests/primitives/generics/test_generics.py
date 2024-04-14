"""Test suite for generic primitives."""

import pytest

from byteclasses.types.primitives.generics import Bit, Byte, DWord, QWord, Word

DATA_BYTE = b"\x00"


def test_bit_primitive():
    """Test Bit primitive"""
    zero_bit = Bit(0)
    one_bit = Bit(1)
    assert zero_bit == 0
    assert one_bit == 1


def test_byte_primitive():
    """Test Byte primitive."""
    expected_length = 1
    byte = Byte()
    assert len(byte) == expected_length
    assert byte.value == DATA_BYTE * expected_length
    assert byte.data == DATA_BYTE * expected_length


def test_byte_init_with_value():
    """Test Byte init with value."""
    byte = Byte(b"\x01")
    assert byte.data == b"\x01"


def test_byte_init_with_data():
    """Test Byte init with data."""
    byte = Byte(data=b"\x01")
    assert byte.data == b"\x01"


def test_byte_init_with_value_and_data():
    """Test Byte init with value_and_data."""
    with pytest.raises(ValueError):
        _ = Byte(b"\x00", data=b"\x01")


def test_byte_init_with_invalid_value():
    """Test Byte init with invalid value."""
    with pytest.raises(TypeError):
        _ = Byte("invalid")


def test_word_primitive():
    """Test Word primitive."""

    expected_length = 2
    word = Word()
    assert len(word) == expected_length
    assert word.value == DATA_BYTE * expected_length
    assert word.data == DATA_BYTE * expected_length


def test_dword_primitive():
    """Test DWord primitive."""

    expected_length = 4
    dword = DWord()
    assert len(dword) == expected_length
    assert dword.value == DATA_BYTE * expected_length
    assert dword.data == DATA_BYTE * expected_length


def test_qword_primitive():
    """Test QWord primitive."""

    expected_length = 8
    qword = QWord()
    assert len(qword) == expected_length
    assert qword.value == DATA_BYTE * expected_length
    assert qword.data == DATA_BYTE * expected_length
