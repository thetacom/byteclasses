"""Unit tests for byteclasses union collection types."""

from byteclasses.types.collections.union import union
from byteclasses.types.primitives.integers import UInt8, UInt16, UInt32, UInt64


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
