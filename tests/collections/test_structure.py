"""Test suite for Structure Byteclass."""

from byteclasses._enums import ByteOrder
from byteclasses.types.collections.structure import structure
from byteclasses.types.primitives.integers import Int16, UInt8, UInt64


def test_structure_creation_unpacked():
    """Test simple structure creation."""

    @structure
    class SimpleStruct:  # pylint: disable=R0903
        """Test structure class."""

        a: UInt8 = UInt8(1)
        b: Int16 = Int16(2)
        c: UInt64 = UInt64(3)

    ss = SimpleStruct()
    assert isinstance(ss, SimpleStruct)
    assert len(ss) == 16
    assert ss.data == b"\x01\x00\x02\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00"
    assert ss.a.endianness == ByteOrder.NATIVE.name
    assert ss.a.data == b"\x01"
    assert ss.a.value == 1
    assert ss.b.endianness == ByteOrder.NATIVE.name
    assert ss.b.data == b"\x02\x00"
    assert ss.b.value == 2
    assert ss.c.endianness == ByteOrder.NATIVE.name
    assert ss.c.data == b"\x03\x00\x00\x00\x00\x00\x00\x00"
    assert ss.c.value == 3


def test_structure_creation_packed():
    """Test simple structure creation."""

    @structure(packed=True)
    class PackedStruct:  # pylint: disable=R0903
        """Test structure class."""

        a: UInt8 = UInt8(1)
        b: Int16 = Int16(2)
        c: UInt64 = UInt64(3)

    ps = PackedStruct()
    assert isinstance(ps, PackedStruct)
    assert len(ps) == 11
    assert ps.data == b"\x01\x02\x00\x03\x00\x00\x00\x00\x00\x00\x00"
    assert ps.a.endianness == ByteOrder.NATIVE.name
    assert ps.a.data == b"\x01"
    assert ps.a.value == 1
    assert ps.b.endianness == ByteOrder.NATIVE.name
    assert ps.b.data == b"\x02\x00"
    assert ps.b.value == 2
    assert ps.c.endianness == ByteOrder.NATIVE.name
    assert ps.c.data == b"\x03\x00\x00\x00\x00\x00\x00\x00"
    assert ps.c.value == 3
