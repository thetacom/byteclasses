"""Test suite for utility functions."""

from byteclasses.types.collections import structure
from byteclasses.types.primitives.integers import UInt8
from byteclasses.util import (
    is_byteclass,
    is_byteclass_collection,
    is_byteclass_collection_instance,
    is_byteclass_instance,
    is_byteclass_primitive,
    is_byteclass_primitive_instance,
)


def test_check_non_byteclass():
    """Test util functions against non-byteclass."""
    var = "invalid"
    assert is_byteclass(var) is False
    assert is_byteclass_instance(var) is False
    assert is_byteclass_primitive(var) is False
    assert is_byteclass_primitive_instance(var) is False
    assert is_byteclass_collection(var) is False
    assert is_byteclass_collection_instance(var) is False


def test_check_byteclass_primitive_class():
    """Test util functions against byteclass primitive class."""
    var = UInt8
    assert is_byteclass(var) is True
    assert is_byteclass_instance(var) is False
    assert is_byteclass_primitive(var) is True
    assert is_byteclass_primitive_instance(var) is False
    assert is_byteclass_collection(var) is False
    assert is_byteclass_collection_instance(var) is False


def test_check_byteclass_primitive_instance():
    """Test util functions against byteclass primitive instance."""
    var = UInt8(1)
    assert is_byteclass(var) is False
    assert is_byteclass_instance(var) is True
    assert is_byteclass_primitive(var) is True
    assert is_byteclass_primitive_instance(var) is True
    assert is_byteclass_collection(var) is False
    assert is_byteclass_collection_instance(var) is False


def test_check_byteclass_collection_class():
    """Test util functions against byteclass collection class."""

    @structure
    class TestStruct:
        """Test Structure."""

        var1: UInt8

    assert is_byteclass(TestStruct) is True
    assert is_byteclass_instance(TestStruct) is False
    assert is_byteclass_primitive(TestStruct) is False
    assert is_byteclass_primitive_instance(TestStruct) is False
    assert is_byteclass_collection(TestStruct) is True
    assert is_byteclass_collection_instance(TestStruct) is False


def test_check_byteclass_collection_instance():
    """Test util functions against byteclass collection instance."""

    @structure
    class TestStruct:
        """Test Structure."""

        var1: UInt8

    var = TestStruct()
    assert is_byteclass(var) is False
    assert is_byteclass_instance(var) is True
    assert is_byteclass_primitive(var) is False
    assert is_byteclass_primitive_instance(var) is False
    assert is_byteclass_collection(var) is False
    assert is_byteclass_collection_instance(var) is True
