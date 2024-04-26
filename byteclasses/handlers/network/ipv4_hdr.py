"""IPv4 Header class implemented with byteclasses."""

from byteclasses.types.collections import ByteArray, member, structure, union
from byteclasses.types.primitives.generics import BitField, BitPos
from byteclasses.types.primitives.integers import UInt8, UInt16, UInt32


class VerIhl(BitField):
    """IPv4 Version and Header Length BitField."""

    version = BitPos(0, bit_width=4)
    ihl = BitPos(4, bit_width=4)


class DscpEcn(BitField):
    """IPv4 DSCP and ECN BitField."""

    dscp = BitPos(0, bit_width=6)
    ecn = BitPos(6, bit_width=2)


class FlagsOff(BitField):
    """IPv4 Flags BitField."""

    byte_length = 2
    pkt_flags = BitPos(0, bit_width=3)
    fragment_offset = BitPos(3, bit_width=13)


@union(byte_order=b"!")
class IPv4Addr:
    """IPv4 Address."""

    uint8: ByteArray = member(factory=lambda byte_order: ByteArray(4, byte_order=byte_order))  # type: ignore
    uint32: UInt32


@structure(byte_order=b"!", packed=True)
class IPv4Hdr:
    """IPv4 Header Structure."""

    ver_ihl: VerIhl
    dscp_ecn: DscpEcn
    total_length: UInt16
    identification: UInt16
    flags_off: FlagsOff
    time_to_live: UInt8
    protocol: UInt8
    header_checksum: UInt16
    src_ip: IPv4Addr
    dst_ip: IPv4Addr
