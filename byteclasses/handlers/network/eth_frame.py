"""Ethernet Frame Class.

[Specification](https://en.wikipedia.org/wiki/Ethernet_frame)
"""

from collections.abc import ByteString
from enum import IntEnum
from functools import cached_property

from .._data_handler import _DataHandler
from .eth_hdr import EthHdr


class EtherType(IntEnum):
    """Ethernet Frame Types."""

    IPV4 = 0x0800
    ARP = 0x0806
    WOL = 0x0842
    CDP = 0x2000
    SRP = 0x22EA
    AVTP = 0x22F0
    TRILL = 0x22F3
    DEC_MOP = 0x6002
    DECNET_DNA_ROUTING = 0x6003
    DEC_LAT = 0x6004
    RARP = 0x8035
    ETHERTALK = 0x809B
    AARP = 0x80F3
    VLAN_TAGGED = 0x8100
    SLPP = 0x8102
    VLACP = 0x8103
    IPX = 0x8137
    QNX = 0x8204
    IPV6 = 0x86DD
    FLOW_CONTROL = 0x8808
    LACP = 0x8809
    COBRANET = 0x8819
    MPLS_UNICAST = 0x8847
    MPLS_MULTICAST = 0x8848


class EthFrame(_DataHandler):
    """Ethernet Frame Data Handler Class."""

    def __init__(self, data: bytes | bytearray = bytearray(b"")) -> None:
        """Initialize Ethernet Frame instance."""
        super().__init__(data)
        self._hdr = EthHdr()
        try:
            self._hdr.attach(memoryview(self._data))  # type: ignore
        except AttributeError as err:
            raise ValueError("Insufficient data") from err

    def __str__(self) -> str:
        """Return Ether Frame string."""
        return f"{self.__class__.__name__}(src_mac={self.src_mac}, dst_mac={self.dst_mac}, type={self.type})"

    @property
    def hdr(self) -> EthHdr:
        """Return data header."""
        return self._hdr

    @property
    def dst_mac(self) -> str:
        """Return dst mac address."""
        return f"{':'.join([hex(val)[2:].rjust(2,'0') for val in self.hdr.dst_mac])}"

    @property
    def src_mac(self) -> str:
        """Return src mac address."""
        return f"{':'.join([hex(val)[2:].rjust(2,'0') for val in self.hdr.src_mac])}"

    @property
    def type(self) -> str:
        """Return Ethernet Frame Type."""
        try:
            return EtherType(int(self.hdr.ether_type)).name
        except ValueError:
            return hex(self.hdr.ether_type)

    @cached_property
    def payload(self) -> _DataHandler | ByteString:
        """Return frame payload."""
        payload_data = self._data[len(self.hdr) :]  # type: ignore
        # if self.type == EtherType.IPV4:
        #     return IPv4Packet(data=payload_data)
        return payload_data
