"""UDP Header implemented with byteclasses."""

from byteclasses.types.collections import structure
from byteclasses.types.primitives.integers import UInt16


@structure(byte_order=b"!", packed=True)
class UDPHdr:
    """UDP Header Class."""

    src_port: UInt16
    dst_port: UInt16
    length: UInt16
    checksum: UInt16
