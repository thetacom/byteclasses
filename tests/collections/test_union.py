"""Unit tests for byteclasses union collection types."""

from byteclasses.types import UInt8, UInt16, UInt32, UInt64, union


def test_union_init():
    """Test initializing a union instance."""

    @union
    class TestUnion:
        """A test union class."""

        a: UInt64
        b: UInt32
        c: UInt16
        d: UInt8

    data = TestUnion()
    assert len(data) == 8
