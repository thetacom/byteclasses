"""Ethernet Header implemented with byteclasses."""

from ...types.collections import ByteArray, member, structure
from ...types.primitives.integers import UInt16


@structure(byte_order=b"!", packed=True)
class EthHdr:
    """Ethernet Header Class."""

    dst_mac: ByteArray = member(factory=lambda byte_order: ByteArray(6))  # type: ignore
    src_mac: ByteArray = member(factory=lambda byte_order: ByteArray(6))  # type: ignore
    ether_type: UInt16
