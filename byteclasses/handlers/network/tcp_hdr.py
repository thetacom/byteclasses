"""TCP Header implemented with byteclasses."""

from ...types import BitField, BitPos, UInt16, UInt32, structure


class OffFlag(BitField):
    """Offset and Flag BitField."""

    byte_length = 2
    data_offset = BitPos(0, bit_width=4)
    tcp_flags = BitPos(4, bit_width=12)


@structure(byte_order=b"!", packed=True)
class TCPHdr:
    """TCP Header Class."""

    src_port: UInt16
    dst_port: UInt16
    seq_number: UInt32
    ack_number: UInt32
    off_flag: OffFlag
    window_size: UInt16
    checksum: UInt16
    urgent_pointer: UInt16
