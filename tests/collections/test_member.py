"""Test suite for byteclass collection member constructor function."""

import pytest

from byteclasses import ByteOrder
from byteclasses.types import UInt8, member
from byteclasses.types.collections._collection_class_spec import _CollectionClassSpec
from byteclasses.types.collections.member import Member, _get_member, _init_member


class TestBaseClass:
    """An empty base class for testing."""

    __test__ = False


test_spec = _CollectionClassSpec(
    TestBaseClass, "test", byte_order=ByteOrder.NATIVE, packed=False, methods={}, self_name="self"
)


def test_member_creation():
    """Test collection member creation."""
    mbr = member(factory=UInt8)
    assert isinstance(mbr, Member)
    assert str(mbr) == (
        "Member(self.name=None,self.type=None,self.factory=<class "
        "'byteclasses.types.primitives.integers.UInt8'>,self.metadata=mappingproxy({}),self.member_type=None)"
    )
    assert repr(mbr) == (
        "Member(self.name=None,self.type=None,self.factory=<class "
        "'byteclasses.types.primitives.integers.UInt8'>,self.metadata=mappingproxy({}),self.member_type=None)"
    )


def test_init_member_with_no_name():
    """Test `init_member` function on member with no name."""
    mbr = member(factory=UInt8)
    with pytest.raises(ValueError):
        _ = _init_member(test_spec, mbr, {})


def test_init_member_with_no_factory():
    """Test `init_member` function on member with no factory."""
    mbr = member()
    mbr.name = "name"
    result = _init_member(test_spec, mbr, {})
    assert result == "BUILTINS.object.__setattr__(self,'name',_init_name(byte_order=ByteOrder.NATIVE))"


def test_get_member_with_invalid_type():
    """Test `get_member` function on class with invalid member type."""

    class TestClass:
        """A class for testing."""

        member1: int

    with pytest.raises(TypeError):
        _ = _get_member(TestClass, "member1", int)
