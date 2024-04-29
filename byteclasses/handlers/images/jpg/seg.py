"""Pre-defined JPEG Header Class.

[JFIF Specification](https://web.archive.org/web/20140903080533/http://www.jpeg.org/public/jfif.pdf)
[JPEG](https://docs.fileformat.com/image/jpeg/)
[List of JPEG Markers](https://www.disktuna.com/list-of-jpeg-markers/)
"""

from collections.abc import ByteString
from enum import Enum, IntEnum
from typing import Any

from ...._enums import ByteOrder
from ....types.collections import String, member, structure
from ....types.primitives.byte_enum import ByteEnum
from ....types.primitives.generics import Word
from ....types.primitives.integers import UInt8, UInt16

__all__ = ["Seg", "SegMark", "SegTag"]


class App0Ident(Enum):
    """App 0 Identifier strings."""

    JFIF = "JFIF"


class SegMark(IntEnum):
    """JPEG Segment Tags."""

    SECTION = 0xFF  # New section
    SOF0 = 0xC0  # Start of Frame 0 - Baseline DCT
    SOF1 = 0xC1  # Start of Frame 1 - Extended Sequential DCT
    SOF2 = 0xC2  # Start of Frame 2 - Progressive DCT
    SOF3 = 0xC3  # Start of Frame 3 - Lossless (sequential)

    DHT = 0xC4  # Define Huffman Tables
    SOF5 = 0xC5  # Start of Frame 5 - Differential sequential DCT
    SOF6 = 0xC6  # Start of Frame 6 - 	Differential progressive DCT
    SOF7 = 0xC7  # Start of Frame 7 - Differential lossless (sequential)

    JPG = 0xC8  # JPEG Extensions
    SOF9 = 0xC9  # Start of Frame 9 - Extended sequential DCT, Arithmetic coding
    SOF10 = 0xCA  # Start of Frame 10 - Progressive DCT, Arithmetic coding
    SOF11 = 0xCB  # Start of Frame 11 - Lossless (sequential), Arithmetic coding

    DAC = 0xCC  # Define Arithmetic Coding
    SOF13 = 0xCD  # Start of Frame 13 - Differential sequential DCT, Arithmetic coding
    SOF14 = 0xCE  # Start of Frame 14 - Differential progressive DCT, Arithmetic coding
    SOF15 = 0xCF  # Start of Frame 15 - Differential lossless (sequential), Arithmetic coding

    RST0 = 0xD0  # Restart 0
    RST1 = 0xD1  # Restart 1
    RST2 = 0xD2  # Restart 2
    RST3 = 0xD3  # Restart 3
    RST4 = 0xD4  # Restart 4
    RST5 = 0xD5  # Restart 5
    RST6 = 0xD6  # Restart 6
    RST7 = 0xD7  # Restart 7

    SOI = 0xD8  # Start of Image
    EOI = 0xD9  # End of Image

    SOS = 0xDA  # Start of Scan
    DQT = 0xDB  # Define Quantization Table(s)
    DNL = 0xDC  # Define Number of Lines - (Not common)
    DRI = 0xDD  # Define Restart Interval
    DHP = 0xDE  # Define Hierarchical Progression - (Not common)
    EXP = 0xDF  # Expand Reference Component - (Not common)

    APP0 = 0xE0  # App specific 0 - JFIF - JFIF JPEG image / AVI1 - Motion JPEG (MJPG)
    APP1 = 0xE1  # App specific 1 - EXIF Metadata, TIFF IFD format, JPEG Thumbnail (160×120) / Adobe XMP
    APP2 = 0xE2  # App specific 2 - ICC color profile, FlashPix
    APP3 = 0xE3  # App specific 3 - (Not common) JPS Tag for Stereoscopic JPEG images
    APP4 = 0xE4  # App specific 4 - (Not common)
    APP5 = 0xE5  # App specific 5 - (Not common)
    APP6 = 0xE6  # App specific 6 - (Not common) NITF Lossles profile
    APP7 = 0xE7  # App specific 7 - (Not common)
    APP8 = 0xE8  # App specific 8 - (Not common)
    APP9 = 0xE9  # App specific 9 - (Not common)
    APP10 = 0xEA  # App specific 10 - (Not common) ActiveObject (multimedia messages / captions)
    APP11 = 0xEB  # App specific 11 - (Not common) HELIOS JPEG Resources (OPI Postscript)
    APP12 = 0xEC  # App specific 12 - Picture Info (older digicams), Photoshop Save for Web: Ducky
    APP13 = 0xED  # App specific 13 - Photoshop Save As: IRB, 8BIM, IPTC
    APP14 = 0xEE  # App specific 14 - (Not common)
    APP15 = 0xEF  # App specific 15 - (Not common)

    JPG0 = 0xF0  # JPEG Extension 0 - (Not common)
    JPG1 = 0xF1  # JPEG Extension 1 - (Not common)
    JPG2 = 0xF2  # JPEG Extension 2 - (Not common)
    JPG3 = 0xF3  # JPEG Extension 3 - (Not common)
    JPG4 = 0xF4  # JPEG Extension 4 - (Not common)
    JPG5 = 0xF5  # JPEG Extension 5 - (Not common)
    JPG6 = 0xF6  # JPEG Extension 6 - (Not common)
    JPG7 = 0xF7  # JPEG Extension 7 - JPEG-LS - Lossless JPEG
    SOF48 = JPG7
    JPG8 = 0xF8  # JPEG Extension 8 - JPEG-LS Extension - Lossless JPEG Extension Parameters
    LSE = JPG8
    JPG9 = 0xF9  # JPEG Extension 9 - (Not common)
    JPG10 = 0xFA  # JPEG Extension 10 - (Not common)
    JPG11 = 0xFB  # JPEG Extension 11 - (Not common)
    JPG12 = 0xFC  # JPEG Extension 12 - (Not common)
    JPG13 = 0xFD  # JPEG Extension 13 - (Not common)

    COM = 0xFE  # Comment


class SegTag(Enum):
    """JPEG Segment Tags."""

    SOF0 = bytes((SegMark.SECTION, SegMark.SOF0))
    SOF1 = bytes((SegMark.SECTION, SegMark.SOF1))
    SOF2 = bytes((SegMark.SECTION, SegMark.SOF2))
    SOF3 = bytes((SegMark.SECTION, SegMark.SOF3))

    DHT = bytes((SegMark.SECTION, SegMark.DHT))
    SOF5 = bytes((SegMark.SECTION, SegMark.SOF5))
    SOF6 = bytes((SegMark.SECTION, SegMark.SOF6))
    SOF7 = bytes((SegMark.SECTION, SegMark.SOF7))

    JPG = bytes((SegMark.SECTION, SegMark.JPG))
    SOF9 = bytes((SegMark.SECTION, SegMark.SOF9))
    SOF10 = bytes((SegMark.SECTION, SegMark.SOF10))
    SOF11 = bytes((SegMark.SECTION, SegMark.SOF11))

    DAC = bytes((SegMark.SECTION, SegMark.DAC))
    SOF13 = bytes((SegMark.SECTION, SegMark.SOF13))
    SOF14 = bytes((SegMark.SECTION, SegMark.SOF14))
    SOF15 = bytes((SegMark.SECTION, SegMark.SOF15))

    RST0 = bytes((SegMark.SECTION, SegMark.RST0))
    RST1 = bytes((SegMark.SECTION, SegMark.RST1))
    RST2 = bytes((SegMark.SECTION, SegMark.RST2))
    RST3 = bytes((SegMark.SECTION, SegMark.RST3))
    RST4 = bytes((SegMark.SECTION, SegMark.RST4))
    RST5 = bytes((SegMark.SECTION, SegMark.RST5))
    RST6 = bytes((SegMark.SECTION, SegMark.RST6))
    RST7 = bytes((SegMark.SECTION, SegMark.RST7))

    SOI = bytes((SegMark.SECTION, SegMark.SOI))
    EOI = bytes((SegMark.SECTION, SegMark.EOI))

    SOS = bytes((SegMark.SECTION, SegMark.SOS))
    DQT = bytes((SegMark.SECTION, SegMark.DQT))
    DNL = bytes((SegMark.SECTION, SegMark.DNL))
    DRI = bytes((SegMark.SECTION, SegMark.DRI))
    DHP = bytes((SegMark.SECTION, SegMark.DHP))
    EXP = bytes((SegMark.SECTION, SegMark.EXP))

    APP0 = bytes((SegMark.SECTION, SegMark.APP0))
    APP1 = bytes((SegMark.SECTION, SegMark.APP1))
    APP2 = bytes((SegMark.SECTION, SegMark.APP2))
    APP3 = bytes((SegMark.SECTION, SegMark.APP3))
    APP4 = bytes((SegMark.SECTION, SegMark.APP4))
    APP5 = bytes((SegMark.SECTION, SegMark.APP5))
    APP6 = bytes((SegMark.SECTION, SegMark.APP6))
    APP7 = bytes((SegMark.SECTION, SegMark.APP7))
    APP8 = bytes((SegMark.SECTION, SegMark.APP8))
    APP9 = bytes((SegMark.SECTION, SegMark.APP9))
    APP10 = bytes((SegMark.SECTION, SegMark.APP10))
    APP11 = bytes((SegMark.SECTION, SegMark.APP11))
    APP12 = bytes((SegMark.SECTION, SegMark.APP12))
    APP13 = bytes((SegMark.SECTION, SegMark.APP13))
    APP14 = bytes((SegMark.SECTION, SegMark.APP14))
    APP15 = bytes((SegMark.SECTION, SegMark.APP15))

    JPG0 = bytes((SegMark.SECTION, SegMark.JPG0))
    JPG1 = bytes((SegMark.SECTION, SegMark.JPG1))
    JPG2 = bytes((SegMark.SECTION, SegMark.JPG2))
    JPG3 = bytes((SegMark.SECTION, SegMark.JPG3))
    JPG4 = bytes((SegMark.SECTION, SegMark.JPG4))
    JPG5 = bytes((SegMark.SECTION, SegMark.JPG5))
    JPG6 = bytes((SegMark.SECTION, SegMark.JPG6))
    JPG7 = bytes((SegMark.SECTION, SegMark.JPG7))
    JPG8 = bytes((SegMark.SECTION, SegMark.JPG8))
    JPG9 = bytes((SegMark.SECTION, SegMark.JPG9))
    JPG10 = bytes((SegMark.SECTION, SegMark.JPG10))
    JPG11 = bytes((SegMark.SECTION, SegMark.JPG11))
    JPG12 = bytes((SegMark.SECTION, SegMark.JPG12))
    JPG13 = bytes((SegMark.SECTION, SegMark.JPG13))

    COM = bytes((SegMark.SECTION, SegMark.COM))


EMPTY_SECTIONS = (
    SegTag.SOI.value,
    SegTag.EOI.value,
)


@structure(byte_order=ByteOrder.BE, packed=True)
class App0Jfif:
    """JPEG App 0 Segment."""

    identifier: String = member(factory=lambda byte_order: String(5))
    ver_major: UInt8
    ver_minor: UInt8
    density_unit: UInt8
    width_density: UInt16
    height_density: UInt16
    width_thumbnail: UInt8
    height_thumbnail: UInt8


def parse_app0(mv: memoryview) -> App0Jfif | dict[str, Any]:
    """Parse App0 Segment data."""
    for idx, val in enumerate(mv):
        if val == 0x00:
            identifier_len = idx + 1
            break
    identifier = String(identifier_len)
    identifier.attach(mv[:identifier_len])
    if identifier.value == App0Ident.JFIF.value:
        hdr: App0Jfif = App0Jfif()
        hdr.attach(mv)  # type: ignore
        return hdr
    attr: dict[str, Any] = {"identifier": identifier}
    return attr


def parse_app1(mv: memoryview) -> dict[str, Any]:
    """Parse App1 Segment data."""
    offset = 0
    result: dict[str, Any] = {}
    for idx, val in enumerate(mv):
        if val == 0x00:
            identifier_len = idx + 1
            break
    identifier = String(identifier_len)
    identifier.attach(mv[:identifier_len])
    result["identifier"] = identifier
    offset += len(identifier)
    # fields = {"unused": UInt8, "header": Word, "tag_mark": Word}
    # for field, field_cls in fields.items():
    #     var = field_cls()
    #     var_len = len(var)
    #     var.attach(mv[offset : offset + var_len])
    #     result[field] = var
    #     offset += var_len

    return result


SEG_MAP = {
    SegTag.APP0.name: parse_app0,
    SegTag.APP1.name: parse_app1,
}


class Seg:
    """JPEG Segment."""

    def __init__(self, data: ByteString) -> None:
        """Initialize instance."""
        mv = data if isinstance(data, memoryview) else memoryview(data)
        self._parts: dict[str, Any] = {}
        self.marker = ByteEnum(SegTag, Word)
        self.marker.attach(mv[:2], retain_value=False)
        if self.marker.value not in EMPTY_SECTIONS:
            length = UInt16(byte_order=ByteOrder.BE)
            length.attach(mv[2:4], retain_value=False)
            self._parts["length"] = length
            payload_end = 2 + length
            payload = mv[4:payload_end]
            self._parts["payload"] = payload
            if self.marker.name in SEG_MAP:
                hdr = SEG_MAP[self.marker.name](payload)
                self._parts["hdr"] = hdr
            if self.marker.name is SegTag.SOS.name:
                # Scan through data to locate next segment
                for idx in range(payload_end, len(mv)):
                    if mv[idx] == 0xFF and mv[idx + 1] != 0x00:
                        next_segment = idx
                        break
                self._parts["image_data"] = mv[payload_end:next_segment]

    def __len__(self) -> int:
        """Return instance length."""
        segment_length = int(self._parts.get("length", 0))
        image_data_length = len(self._parts.get("image_data", b""))
        return 2 + segment_length + image_data_length

    def __repr__(self) -> str:
        """Return instance raw representation."""
        return f"{self.__class__.__name__}({self.marker.name})"

    def __str__(self) -> str:
        """Return instance string representation."""
        parts = []
        for key, value in self._parts.items():
            parts.append(f"{key}={value!r}")
        return f"<{self.__class__.__name__}({self.marker.name}): {', '.join(parts)}>"

    @property
    def marker(self) -> ByteEnum:
        """Return instance marker."""
        return self._marker

    @marker.setter
    def marker(self, value: ByteEnum) -> None:
        """Set instance marker."""
        self._marker = value
