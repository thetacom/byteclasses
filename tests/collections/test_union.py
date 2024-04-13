"""Unit tests for byteclasses union collection types."""

from byteclasses.types.collections.union import union
from byteclasses.types.primitives.integers import UInt8, UInt16, UInt32, UInt64


def test_union_init():
    """Test initializing a union instance."""

    @union
    class TestUnion:
        """A test union class."""

        a: UInt64 = UInt64(0)
        b: UInt32 = UInt32(0)
        c: UInt16 = UInt16(0)
        d: UInt8 = UInt8(0)

    data = TestUnion()
    assert len(data) == 8
