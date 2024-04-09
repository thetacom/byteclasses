"""Unit tests for byteclasses bitfield primitive type."""

import pytest

from byteclasses.types.primitives.bit_pos import BitPos
from byteclasses.types.primitives.bitfield import BitField


def test_generic_bitfield_creation():
    """Create generic bitfield."""
    bf = BitField()
    assert bf.bit_length == 8
    assert len(bf) == 1
    assert bf.data == b"\x00"
    bf[0] = 1
    bf[7] = 1
    assert bf.data == b"\x81"
    with pytest.raises(IndexError):
        print(bf[8])
    with pytest.raises(IndexError):
        bf[8] = 1


def test_custom_bitfield_creation():
    """Create custom bitfield."""

    class CustomBitField(BitField):
        """Custom BitField"""

        byte_length = 2
        first_bit = BitPos(0)
        last_bit = BitPos(15)

    bf = CustomBitField()
    assert bf.bit_length == 16
    assert len(bf) == 2
    assert bf.data == b"\x00\x00"
    assert bf.first_bit is False
    assert bf.last_bit is False
    bf[0] = 1
    bf[15] = 1
    assert bf.data == b"\x01\x80"
    assert bf.first_bit is True
    assert bf.last_bit is True
