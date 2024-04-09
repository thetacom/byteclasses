""""Utility functions."""

from collections.abc import Iterable
from types import FunctionType
from typing import Any

from .member import Member


def _tuple_str(obj_name: str, members_: Iterable[Member]) -> str:
    """Return a string representing each member of obj_name as a tuple member.

    If members is ['x', 'y'] and obj_name is "self", return "(self.x,self.y)".
    """
    # Special case for the 0-tuple.
    if not members_:
        return "(,)"
    # Note the trailing comma, needed if this turns out to be a 1-tuple.
    return f'({",".join([f"{obj_name}.{member_.name}" for member_ in members_])},)'


def _set_qualname(cls, func):
    # Ensure that the functions returned from _create_fn uses the proper
    # __qualname__ (the class they belong to).
    if isinstance(func, FunctionType):
        func.__qualname__ = f"{cls.__qualname__}.{func.__name__}"
    return func


def _set_new_attribute(cls, name: str, value: Any, force: bool = False) -> bool:
    """Set a new attribute on a class.

    Do not override existing attributes if not forced.
    Returns True if the attribute already exists.
    """
    if name in cls.__dict__ and not force:
        return True
    _set_qualname(cls, value)
    setattr(cls, name, value)
    return False
