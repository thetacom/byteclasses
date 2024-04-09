"""Unit tests for byteclasses structure collection types."""

from byteclasses.enums import ByteOrder
from byteclasses.types.collections.structure import structure
from byteclasses.types.primitives.integers import Int16, UInt8, UInt64


def test_structure():
    """Test instantiation of a simple structure."""

    @structure
    class SimpleStruct:  # pylint: disable=R0903
        """Test structure class."""

        a: UInt8 = UInt8(1)
        b: Int16 = Int16(2)
        c: UInt64 = UInt64(3)

    d = SimpleStruct()
    assert isinstance(d, SimpleStruct)
    assert d.data == b"\x01\x00\x02\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"
    assert d.a.endianness == ByteOrder.NATIVE.name
    assert d.a.data == b"\x01"
    assert d.a.value == 1
    assert d.b.endianness == ByteOrder.NATIVE.name
    assert d.b.data == b"\x02\x00"
    assert d.b.value == 2
    assert d.c.endianness == ByteOrder.NATIVE.name
    assert d.c.data == b"\x03\x00\x00\x00\x00\x00\x00\x00"
    assert d.c.value == 3
