"""Test suite for Structure Byteclass."""

import pytest

from byteclasses._enums import ByteOrder
from byteclasses.types import Int16, UInt8, UInt64, member, structure


def test_structure_creation_with_member_default():
    """Test simple structure creation with member default."""

    with pytest.raises(ValueError):

        @structure
        class BadStruct:  # pylint: disable=R0903
            """Test structure class."""

            a: UInt8 = UInt8(1)

        _ = BadStruct()


def test_structure_creation_with_member_factory():
    """Test simple structure creation with member factory."""

    @structure
    class FactoryStruct:  # pylint: disable=R0903
        """Factory structure class."""

        a: UInt8 = member(factory=UInt8)

    fs = FactoryStruct()

    assert isinstance(fs, FactoryStruct)
    assert len(fs) == 1


def test_structure_creation_with_lambda_factory():
    """Test simple structure creation with lambda factory."""

    @structure
    class LambdaStruct:  # pylint: disable=R0903
        """Lambda structure class."""

        a: UInt8 = member(factory=lambda byte_order: UInt8(8, byte_order=byte_order))

    ls = LambdaStruct()

    assert isinstance(ls, LambdaStruct)
    assert len(ls) == 1
    assert ls.a == 8


def test_structure_creation_unpacked():
    """Test simple structure creation."""

    @structure
    class SimpleStruct:  # pylint: disable=R0903
        """Test structure class."""

        a: UInt8
        b: Int16
        c: UInt64

    ss = SimpleStruct()
    assert isinstance(ss, SimpleStruct)
    assert len(ss) == 16
    assert ss.data == b"\x00" * len(ss)
    assert ss.a.endianness == ByteOrder.NATIVE.name
    assert ss.a.data == b"\x00"
    assert ss.a.value == 0
    assert ss.b.endianness == ByteOrder.NATIVE.name
    assert ss.b.data == b"\x00\x00"
    assert ss.b.value == 0
    assert ss.c.endianness == ByteOrder.NATIVE.name
    assert ss.c.data == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert ss.c.value == 0


def test_structure_creation_packed():
    """Test simple structure creation."""

    @structure(packed=True)
    class PackedStruct:  # pylint: disable=R0903
        """Test structure class."""

        a: UInt8
        b: Int16
        c: UInt64

    ps = PackedStruct()
    assert isinstance(ps, PackedStruct)
    assert len(ps) == 11
    assert ps.data == b"\x00" * len(ps)
    assert ps.a.endianness == ByteOrder.NATIVE.name
    assert ps.a.data == b"\x00"
    assert ps.a.value == 0
    assert ps.b.endianness == ByteOrder.NATIVE.name
    assert ps.b.data == b"\x00\x00"
    assert ps.b.value == 0
    assert ps.c.endianness == ByteOrder.NATIVE.name
    assert ps.c.data == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert ps.c.value == 0
