"""Mach-O UUID Command Module.

[OS X ABI Mach-O File Format Reference](https://github.com/aidansteele/osx-abi-macho-file-format-reference)
[llvm::MachO Namespace Reference](https://llvm.org/doxygen/namespacellvm_1_1MachO.html)
"""

from ....types import ByteArray, Ptr32, UInt32, member, structure

__all__ = ["UUIDCmd"]


@structure
class UUIDCmd:
    """Mach-O UUID Command."""

    cmd: Ptr32
    cmdsize: UInt32
    uuid: ByteArray = member(factory=lambda byte_order: ByteArray(16))  # type: ignore
