"""Ethernet Header implemented with byteclasses."""

from ...types.collections import FixedArray, member, structure
from ...types.primitives.integers import UInt16


@structure(byte_order=b"!", packed=True)
class EthHdr:
    """Ethernet Header Class."""

    dst_mac: FixedArray = member(default_factory=lambda: FixedArray(6))  # type: ignore
    src_mac: FixedArray = member(default_factory=lambda: FixedArray(6))  # type: ignore
    ether_type: UInt16
