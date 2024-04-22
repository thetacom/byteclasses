"""Byteclasses Print Module."""

from collections.abc import ByteString
from itertools import cycle
from typing import TYPE_CHECKING, Any, Optional

from rich.panel import Panel  # pylint: disable=E0401
from rich.pretty import get_console  # pylint: disable=E0401
from rich.table import Table  # pylint: disable=E0401
from rich.text import Text  # pylint: disable=E0401

from .types._fixed_size_type import _FixedSizeType
from .types.collections.member import _MEMBERS, is_fixed_collection
from .util import is_byteclass_instance

if TYPE_CHECKING:
    from rich.console import Console

COLOR_NAMES = (
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
)

FILL_COLOR = "white"


def byteclass_info(
    obj: Any,
    /,
    *,
    console: Optional["Console"] = None,
) -> None:
    """Print byteclass collection in a table."""
    if not is_byteclass_instance(obj):
        raise TypeError("Object is not a byteclass object.")
    table = Table(title="Byteclass Info")
    table.add_column("Property")
    table.add_column("Value")

    colors = cycle(COLOR_NAMES)
    properties = {
        "type()": obj.__class__.__name__,
        "mro": " -> ".join([cls.__name__ for cls in obj.__class__.__mro__]),
        "len()": len(obj),
        "str()": str(obj),
        "repr()": repr(obj),
        ".data": obj.data,
    }
    if isinstance(obj, _FixedSizeType):
        properties.update({".value": obj.value})
    for name, val in properties.items():
        table.add_row(Text(name, style="bold"), str(val), style=next(colors))
    _console = get_console() if console is None else console
    _console.print(table)


def _info_line(name: str, val: str, color: str) -> str:
    """Generate an info line."""
    return f"[{color}][bold]{name.title()}:[/bold] {val}[/{color}]\n"


def byteclass_table(
    obj: Any,
    /,
    *,
    show_data: bool = True,
    title: str | None = None,
    console: Optional["Console"] = None,
) -> None:
    """Print byteclass instance in a table."""
    if not is_byteclass_instance(obj):
        raise TypeError("Object is not a byteclass instance.")
    if is_fixed_collection(obj):
        collection_table(obj, show_data=show_data, title=title, console=console)
    else:
        primitive_table(obj, show_data=show_data, title=title, console=console)


def collection_table(
    obj: Any,
    /,
    *,
    show_data: bool = True,
    title: str | None = None,
    console: Optional["Console"] = None,
) -> None:
    """Print byteclass collection in a table."""
    if not is_fixed_collection(obj):
        raise TypeError("Object is not a byteclass collection.")
    table = Table(title=title) if title else Table(title=obj.__class__.__name__)
    table.add_column("Member")
    table.add_column("Value")
    if show_data:
        table.add_column("Data")

    colors = cycle(COLOR_NAMES)
    for member in getattr(obj, _MEMBERS):
        attr = getattr(obj, member)
        if show_data:
            table.add_row(Text(member, style="bold"), str(attr), str(attr.data), style=next(colors))
        else:
            table.add_row(Text(member, style="bold"), str(attr), style=next(colors))

    _console = get_console() if console is None else console
    _console.print(table)


def primitive_table(
    obj: Any,
    /,
    *,
    show_data: bool = True,
    title: str | None = None,
    console: Optional["Console"] = None,
) -> None:
    """Print byteclass primitive in a table."""
    table = Table(title=title) if title else Table(title=obj.__class__.__name__)
    table.add_column("Value")
    if show_data:
        table.add_column("Data")

    colors = cycle(COLOR_NAMES)
    if show_data:
        table.add_row(Text(str(obj), style="bold"), str(obj.data), style=next(colors))
    else:
        table.add_row(Text(str(obj), style="bold"), style=next(colors))

    _console = get_console() if console is None else console
    _console.print(table)


def _data_str(data: ByteString, color: str | None = None) -> str:
    """Return a hexedecimal string from a sequence of bytes."""
    data_str = " ".join([f"{byte_:02x}" for byte_ in data])
    if color is not None:
        return f"[{color}]{data_str}[/{color}]"
    return " ".join([f"{byte_:02x}" for byte_ in data])


def byteclass_inspect(
    obj: Any,
    /,
    *,
    legend: bool = True,
    byte_width: int = 32,
    console: Optional["Console"] = None,
) -> None:
    """Print byteclass collection in a table."""
    if not is_byteclass_instance(obj):
        raise TypeError("Object is not a byteclass instance.")
    if is_fixed_collection(obj):
        _print_byteclass_collection_panel(obj, byte_width=byte_width, console=console)
    else:
        _print_byteclass_primitive_panel(obj, byte_width=byte_width, console=console)
    if legend:
        byteclass_table(obj, show_data=False, title="Legend")


def _print_byteclass_collection_panel(obj, *, byte_width: int, console):
    """Print a byteview of collection object data to console."""
    lines = []
    v_offset_width = len(hex(len(obj))) + 1
    line_length = byte_width * 3 + 4
    panel_width = line_length + v_offset_width

    lines.extend(_generate_header_lines(v_offset_width, byte_width))
    lines.extend(_generate_collection_lines(obj, v_offset_width, byte_width))

    _console = get_console() if console is None else console
    byte_panel = Panel("\n".join(lines), title="Byteclass Inspect", width=panel_width)
    _console.print(byte_panel)


def _print_byteclass_primitive_panel(obj, *, byte_width: int, console):
    """Print a byteview of primitive object data to console."""
    lines = []
    v_offset_width = len(hex(len(obj))) + 1
    panel_padding = 6
    line_length = byte_width * 3
    panel_width = line_length + v_offset_width + panel_padding

    lines.extend(_generate_header_lines(v_offset_width, byte_width))
    lines.extend(_generate_primitive_lines(obj, v_offset_width, byte_width))

    _console = get_console() if console is None else console
    byte_panel = Panel("\n".join(lines), title="Byteclass Inspect", width=panel_width)
    _console.print(byte_panel)


def _generate_header_lines(v_offset_width: int, byte_width: int) -> list[str]:
    """Generate panel header lines."""
    h_offsets = [f"{i:02x}" for i in range(byte_width)]
    h_offset_line = f"{' ' * (v_offset_width + 1)}{' '.join(h_offsets)}"
    separator_line = "-" * len(h_offset_line)
    return [h_offset_line, separator_line]


def _generate_data_line(data_str: str, v_offset: int, v_offset_width: int) -> str:
    """Generate a data line."""
    return f"{hex(v_offset).ljust(v_offset_width, ' ')}{data_str}"


def _generate_collection_lines(obj, v_offset_width: int, byte_width: int) -> list[str]:
    """Generate collection data lines from object."""
    member_colors = cycle(COLOR_NAMES)
    lines = []
    curr_offset = 0
    line_offset = 0
    data_str = ""
    for member_name in getattr(obj, _MEMBERS):
        print(member_name)
        member = getattr(obj, member_name)
        color = next(member_colors)
        mbr_len = len(member)
        # Insert padding
        if curr_offset != member.offset:
            print("Inserting padding")
            padding_len = member.offset - curr_offset
            if line_offset + padding_len < byte_width:
                data_str += (
                    f"[{FILL_COLOR}]|"
                    + _data_str(obj.data[curr_offset : member.offset], FILL_COLOR)
                    + f"[/{FILL_COLOR}]"
                )
                curr_offset += padding_len
                line_offset += padding_len
            else:
                part1_len = byte_width - line_offset
                part2_len = padding_len - part1_len
                data_str += (
                    f"[{FILL_COLOR}]|"
                    + _data_str(obj.data[curr_offset : curr_offset + part1_len], color)
                    + f"[/{FILL_COLOR}]"
                )
                lines.append(_generate_data_line(data_str, (curr_offset // byte_width) * byte_width, v_offset_width))
                data_str = (
                    f"[{FILL_COLOR}]|"
                    + _data_str(obj.data[curr_offset + part1_len : member.offset], color)
                    + f"[/{FILL_COLOR}]"
                )
                curr_offset += padding_len
                line_offset = part2_len

        if line_offset + mbr_len < byte_width:
            data_str += f"[{FILL_COLOR}]|[/{FILL_COLOR}]" + _data_str(member.data, color)
            curr_offset += mbr_len
            line_offset += mbr_len
        else:
            part1_len = byte_width - line_offset
            part2_len = mbr_len - part1_len
            data_str += f"[{FILL_COLOR}]|[/{FILL_COLOR}]" + _data_str(member.data[:part1_len], color)
            lines.append(_generate_data_line(data_str, (curr_offset // byte_width) * byte_width, v_offset_width))
            data_str = _data_str(member.data[part1_len:], color)
            curr_offset += mbr_len
            line_offset = part2_len
    if data_str:
        lines.append(_generate_data_line(data_str, (curr_offset // byte_width) * byte_width, v_offset_width))
    return lines


def _generate_primitive_lines(obj, v_offset_width: int, byte_width) -> list[str]:
    """Generate primitive data lines from object."""
    member_colors = cycle(COLOR_NAMES)
    color = next(member_colors)
    lines = []
    obj_len = len(obj)
    curr_offset = 0
    while curr_offset < obj_len:
        if obj_len - curr_offset < byte_width:
            data_str = f"[{FILL_COLOR}]|[/{FILL_COLOR}]" + _data_str(obj.data[curr_offset:], color)
            curr_offset = obj_len
        else:
            data_str = f"[{FILL_COLOR}]|[/{FILL_COLOR}]" + _data_str(
                obj.data[curr_offset : curr_offset + byte_width], color
            )
            lines.append(_generate_data_line(data_str, (curr_offset // byte_width) * byte_width, v_offset_width))
            curr_offset += byte_width
    if data_str:
        lines.append(_generate_data_line(data_str, (curr_offset // byte_width) * byte_width, v_offset_width))
    return lines
