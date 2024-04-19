"""Byteclasses Utility Module."""

from types import GenericAlias
from typing import Any

from .constants import _BYTECLASS


def is_byteclass_instance(obj: Any) -> bool:
    """Return True if obj is a byteclass instance."""
    return hasattr(type(obj), _BYTECLASS)


def is_byteclass(obj: Any) -> bool:
    """Return True if obj is a byteclass or byteclass instance."""
    cls = obj if isinstance(obj, type) and not isinstance(obj, GenericAlias) else type(obj)
    return isinstance(obj, type) and hasattr(cls, _BYTECLASS)
