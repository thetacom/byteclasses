"""Byteclasses Utility Module."""

from types import GenericAlias
from typing import Any

from .constants import _BYTECLASS, _MEMBERS
from .types.primitives._primitive import _Primitive


def is_byteclass_instance(obj: Any) -> bool:
    """Return True if obj is a byteclass instance."""
    return hasattr(type(obj), _BYTECLASS)


def is_byteclass(obj: Any) -> bool:
    """Return True if obj is a byteclass or byteclass instance."""
    cls = obj if isinstance(obj, type) and not isinstance(obj, GenericAlias) else type(obj)
    return isinstance(obj, type) and hasattr(cls, _BYTECLASS)


def is_byteclass_collection_instance(obj: Any) -> bool:
    """Return True if obj is an instance of a fixed collection."""
    return is_byteclass_instance(obj) and hasattr(type(obj), _MEMBERS)


def is_byteclass_collection(obj: Any) -> bool:
    """Return True if obj is a class or instance of a fixed collection."""
    cls = obj if isinstance(obj, type) and not isinstance(obj, GenericAlias) else type(obj)
    return is_byteclass(obj) and hasattr(cls, _MEMBERS)


def is_byteclass_primitive_instance(obj: Any) -> bool:
    """Return True if obj is an instance of a byteclass primitive."""
    return isinstance(obj, _Primitive)


def is_byteclass_primitive(obj: Any) -> bool:
    """Return True if obj is a class or instance of a byteclass primitive."""
    cls = obj if isinstance(obj, type) and not isinstance(obj, GenericAlias) else type(obj)
    return issubclass(cls, _Primitive)
