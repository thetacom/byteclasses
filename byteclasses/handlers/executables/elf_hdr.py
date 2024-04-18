"""Pre-defined Unix/Linux Executable Header Class.

[ELF Specification](https://www.man7.org/linux/man-pages/man5/elf.5.html)
[elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)
"""

from ...types.collections import String, member, structure, union
from ...types.primitives.characters import UChar
from ...types.primitives.generics import BitField
from ...types.primitives.integers import Int32, Int64, UInt16, UInt32, UInt64

__all__ = [
    "Elf32Hdr",
    "Elf32PHdr",
    "Elf32SHdr",
    "Elf32Sym",
    "Elf32Rel",
    "Elf32RelA",
    "Elf32Dyn",
    "Elf32NoteHdr",
    "Elf64Hdr",
    "Elf64PHdr",
    "Elf64SHdr",
    "Elf64Sym",
    "Elf64Rel",
    "Elf64RelA",
    "Elf64Dyn",
    "Elf64NoteHdr",
]


class BitField32(BitField):
    """32-bit BitField."""

    byte_length = 4


class BitField64(BitField):
    """64-bit BitField."""

    byte_length = 8


@structure
class Elf32Hdr:
    """32-bit Elf Header Class."""

    e_ident: String = member(default_factory=lambda: String(16))  # type: ignore
    e_type: UInt16
    e_machine: UInt16
    e_version: UInt32
    e_entry: UInt32
    e_phoff: UInt32
    e_shoff: UInt32
    e_flags: BitField32
    e_ehsize: UInt16
    e_phentsize: UInt16
    e_phnum: UInt16
    e_shentsize: UInt16
    e_shnum: UInt16
    e_shstrndx: UInt16


@structure
class Elf64Hdr:
    """64-bit Elf Header Class."""

    e_ident: String = member(default_factory=lambda: String(16))  # type: ignore
    e_type: UInt16
    e_machine: UInt16
    e_version: UInt32
    e_entry: UInt64
    e_phoff: UInt64
    e_shoff: UInt64
    e_flags: BitField32
    e_ehsize: UInt16
    e_phentsize: UInt16
    e_phnum: UInt16
    e_shentsize: UInt16
    e_shnum: UInt16
    e_shstrndx: UInt16


@structure
class Elf32PHdr:
    """32-bit Elf Program Header."""

    p_type: UInt32
    p_offset: UInt32
    p_vaddr: UInt32
    p_paddr: UInt32
    p_filesz: UInt32
    p_flags: BitField32
    p_align: UInt32


@structure
class Elf64PHdr:
    """64-bit Elf Program Header."""

    p_type: UInt32
    p_flags: BitField32
    p_offset: UInt64
    p_vaddr: UInt64
    p_paddr: UInt64
    p_filesz: UInt64
    p_memsz: UInt64
    p_align: UInt64


@structure
class Elf32SHdr:
    """32-bit Elf Section Header."""

    sh_name: UInt32
    sh_type: UInt32
    sh_flags: BitField32
    sh_addr: UInt32
    sh_offset: UInt32
    sh_size: UInt32
    sh_link: UInt32
    sh_info: UInt32
    sh_addralign: UInt32
    sh_entsize: UInt32


@structure
class Elf64SHdr:
    """64-bit Elf Section Header."""

    sh_name: UInt32
    sh_type: UInt32
    sh_flags: BitField64
    sh_addr: UInt64
    sh_offset: UInt64
    sh_size: UInt64
    sh_link: UInt32
    sh_info: UInt32
    sh_addralign: UInt64
    sh_entsize: UInt64


@structure
class Elf32Sym:
    """32-bit Elf Symbol Header."""

    st_name: UInt32
    st_value: UInt32
    st_size: UInt32
    st_info: UChar
    st_other: UChar
    st_shndx: UInt16


@structure
class Elf64Sym:
    """64-bit Elf Symbol Header."""

    st_name: UInt32
    st_info: UChar
    st_other: UChar
    st_shndx: UInt16
    st_value: UInt64
    st_size: UInt64


@structure
class Elf32Rel:
    """32-bit Elf Relocation Entry."""

    r_offset: UInt32
    r_info: UInt32


@structure
class Elf64Rel:
    """64-bit Elf Relocation Entry."""

    r_offset: UInt64
    r_info: UInt64


@structure
class Elf32RelA:
    """32-bit Elf Relocation Addend Entry."""

    r_offset: UInt32
    r_info: UInt32
    r_addend: UInt32


@structure
class Elf64RelA:
    """64-bit Elf Relocation Addend Entry."""

    r_offset: UInt64
    r_info: UInt64
    r_addend: UInt32


@union
class DUn32:
    """32-bit Elf Dynamic Entry Union."""

    d_val: UInt32
    d_ptr: UInt32


@structure
class Elf32Dyn:
    """32-bit Elf Dynamic Entry."""

    d_tag: Int32
    d_un: DUn32


@union
class DUn64:
    """64-bit Elf Dynamic Entry Union."""

    d_val: UInt64
    d_ptr: UInt64


@structure
class Elf64Dyn:
    """64-bit Elf Dynamic Entry."""

    d_tag: Int64
    d_un: DUn64


@structure
class Elf32NoteHdr:
    """32-bit Elf Note Header."""

    n_namesz: UInt32
    n_descsz: UInt32
    n_type: UInt32


@structure
class Elf64NoteHdr:
    """64-bit Elf Note Header."""

    n_namesz: UInt64
    n_descsz: UInt64
    n_type: UInt64
