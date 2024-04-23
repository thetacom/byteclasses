"""PE Data Directory Class."""

from ....types.collections import structure
from ....types.primitives.integers import Ptr32, UInt32

__all__ = [
    "DataDir",
]


@structure
class DataDir:
    """PE Data Directory Class."""

    vaddr: Ptr32
    size: UInt32
