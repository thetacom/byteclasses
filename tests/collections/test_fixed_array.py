"""Test suite for FixedArray Byteclass."""

from byteclasses.types.collections.fixed_array import FixedArray
from byteclasses.types.primitives.integers import UInt8, UInt32

NULL_BYTE = b"\x00"


def test_fixed_array_creation():
    """Test FixedArray creation and properties."""
    expected_count = 8
    expected_length = expected_count * len(UInt8())
    fa = FixedArray(expected_count)
    assert len(fa) == expected_count
    assert fa.data == NULL_BYTE * expected_length


def test_fixed_array_creation_with_type():
    """Test FixedArray creation and properties."""
    expected_count = 8
    item_type = UInt32
    expected_length = expected_count * len(item_type())
    fa = FixedArray(expected_count, item_type)
    assert len(fa) == expected_length
    assert fa.data == NULL_BYTE * expected_length
