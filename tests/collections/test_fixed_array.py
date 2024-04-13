"""Test suite for FixedArray Byteclass."""

from byteclasses.types.collections.fixed_array import FixedArray
from byteclasses.types.primitives.integers import UInt8

NULL_BYTE = b"\x00"


def test_fixed_array_creation():
    """Test FixedArray creation and properties."""
    expected_length = 8
    fa = FixedArray(UInt8, expected_length)
    assert len(fa) == expected_length
    assert fa.data == NULL_BYTE * expected_length
