"""Mach-O Load Command Module."""

from ....types.collections import structure
from ....types.primitives.integers import UInt32

__all__ = ["LoadCommand"]


@structure
class LoadCommand:
    """Mach-O Load Command."""

    cmd: UInt32
    cmdsize: UInt32
