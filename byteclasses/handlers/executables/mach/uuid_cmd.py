"""Mach-O UUID Command Module.

[OS X ABI Mach-O File Format Reference](https://github.com/aidansteele/osx-abi-macho-file-format-reference)
[llvm::MachO Namespace Reference](https://llvm.org/doxygen/namespacellvm_1_1MachO.html)
"""

from ....types.collections import FixedArray, member, structure
from ....types.primitives.integers import Ptr32, UInt32

__all__ = ["UUIDCmd"]


@structure
class UUIDCmd:
    """Mach-O UUID Command."""

    cmd: Ptr32
    cmdsize: UInt32
    uuid: FixedArray = member(factory=lambda byte_order: FixedArray(16))  # type: ignore
