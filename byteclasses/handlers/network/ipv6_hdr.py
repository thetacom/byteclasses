"""IPv6 Header class implemented with byteclasses."""

from byteclasses.types.collections import ByteArray, member, structure, union
from byteclasses.types.primitives.generics import BitField, BitPos
from byteclasses.types.primitives.integers import UInt8, UInt16, UInt32, UInt64


class VTF(BitField):
    """IPv6 Version/Traffic/Flow Label BitField."""

    byte_length = 4
    version = BitPos(0, bit_width=4)
    traffic_class = BitPos(4, bit_width=8)
    flow_label = BitPos(12, bit_width=20)


@union(byte_order=b"!")
class IPv6Addr:
    """IPv6 Address."""

    uint8: ByteArray = member(factory=lambda byte_order: ByteArray(16, byte_order=byte_order))  # type: ignore
    uint32: UInt32 = member(factory=lambda byte_order: ByteArray(4, UInt32, byte_order=byte_order))  # type: ignore
    uint64: UInt32 = member(factory=lambda byte_order: ByteArray(2, UInt64, byte_order=byte_order))  # type: ignore


@structure(byte_order=b"!", packed=True)
class IPv6Hdr:
    """IPv6 Header Structure."""

    vtf: VTF
    payload_length: UInt16
    next_hdr: UInt8
    hop_limit: UInt8
    src_addr: IPv6Addr
    dst_addr: IPv6Addr


@structure(byte_order=b"!", packed=True)
class HopByHopExtHdr:
    """Hop-by-Hop Options extension header."""

    next_hdr: UInt8
    hdr_ext_length: UInt8
    options: ByteArray = member(factory=lambda byte_order: ByteArray(14, byte_order=byte_order))  # type: ignore


@structure(byte_order=b"!", packed=True)
class RoutingExtHdr:
    """Routing extension header."""

    next_hdr: UInt8
    hdr_ext_length: UInt8
    routing_type: UInt8
    segments_left: UInt8
    type_data: ByteArray = member(factory=lambda byte_order: ByteArray(12, byte_order=byte_order))


class FragmentBitField(BitField):
    """IPv6 Fragment Offset and more follows flag bitfield."""

    byte_length = 2
    frag_offset = BitPos(0, bit_width=13)
    reserved = BitPos(13, bit_width=2)
    more = BitPos(15)


@structure(byte_order=b"!", packed=True)
class FragmentExtHdr:
    """Fragment extension header."""

    next_hdr: UInt8
    reserved: UInt8
    fragment: FragmentBitField
    identification: UInt32
