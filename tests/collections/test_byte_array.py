"""Test suite for ByteArray Byteclass."""

from byteclasses.types.collections.byte_array import ByteArray
from byteclasses.types.primitives.integers import UInt8, UInt32

NULL_BYTE = b"\x00"


def test_byte_array_creation():
    """Test ByteArray creation and properties."""
    expected_count = 8
    expected_length = expected_count * len(UInt8())
    fa = ByteArray(expected_count)
    assert len(fa) == expected_count
    assert fa.data == NULL_BYTE * expected_length


def test_byte_array_creation_with_type():
    """Test ByteArray creation and properties."""
    expected_count = 8
    item_type = UInt32
    expected_length = expected_count * len(item_type())
    fa = ByteArray(expected_count, item_type)
    assert len(fa) == expected_length
    assert fa.data == NULL_BYTE * expected_length
