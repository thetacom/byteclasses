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
    from .console import Console

COLOR_NAMES = (
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
)


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


def _data_str(data: ByteString) -> str:
    """Return a hexedecimal string from a sequence of bytes."""
    return " ".join([f"{byte_:02x}" for byte_ in data])


member_colors = cycle(COLOR_NAMES)


def _mbr_line(obj, member) -> str:
    """Generate member line."""
    attr = getattr(obj, member)
    data_str = _data_str(attr.data)
    return data_str


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
    lines.extend(_generate_collection_lines(obj, v_offset_width, byte_width, line_length))

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
    lines.extend(_generate_primitive_lines(obj, v_offset_width, byte_width, line_length))

    _console = get_console() if console is None else console
    byte_panel = Panel("\n".join(lines), title="Byteclass Inspect", width=panel_width)
    _console.print(byte_panel)


def _generate_header_lines(v_offset_width: int, byte_width: int) -> list[str]:
    """Generate panel header lines."""
    h_offsets = [f"{i:02x}" for i in range(byte_width)]
    h_offset_line = f"{' ' * (v_offset_width + 1)}{' '.join(h_offsets)}"
    separator_line = "-" * len(h_offset_line)
    return [h_offset_line, separator_line]


def _generate_collection_lines(obj, v_offset_width: int, byte_width, line_length) -> list[str]:
    """Generate collection data lines from object."""
    lines = []
    v_offset = 0
    current_line_len = 0
    data_line = ""
    for member in getattr(obj, _MEMBERS):
        color = next(member_colors)
        mbr_data_line = _mbr_line(obj, member)
        mbr_line_len = len(mbr_data_line)
        if current_line_len + mbr_line_len + v_offset_width + 1 < line_length:
            current_line_len += mbr_line_len + 1
            data_line += f"|[{color}]" + mbr_data_line + f"[/{color}]"
        else:
            remainder = line_length - v_offset_width - current_line_len
            data_line += f"|[{color}]" + mbr_data_line[: remainder + 1] + f"[/{color}]"
            lines.append(f"{hex(v_offset).ljust(v_offset_width, ' ')}" + data_line)
            current_line_len = len(mbr_data_line[remainder + 1 :]) + 1
            data_line = f"[{color}]" + mbr_data_line[remainder + 1 :] + f"[/{color}]"
            v_offset += byte_width

    if data_line:
        lines.append(f"{hex(v_offset).ljust(v_offset_width, ' ')}" + data_line)
    return lines


def _generate_primitive_lines(obj, v_offset_width: int, byte_width, line_length) -> list[str]:
    """Generate primitive data lines from object."""
    lines = []
    v_offset = 0
    current_line_len = 0
    data_line = ""
    color = next(member_colors)
    data_line = _data_str(obj.data)
    line_len = len(data_line)
    if current_line_len + line_len + v_offset_width + 1 < line_length:
        current_line_len += line_len + 1
        data_line += f"|[{color}]" + data_line + f"[/{color}]"
    else:
        remainder = line_length - v_offset_width - current_line_len
        data_line += f"|[{color}]" + data_line[: remainder + 1] + f"[/{color}]"
        lines.append(f"{hex(v_offset).ljust(v_offset_width, ' ')}" + data_line)
        current_line_len = len(data_line[remainder + 1 :]) + 1
        data_line = f"[{color}]" + data_line[remainder + 1 :] + f"[/{color}]"
        v_offset += byte_width

    if data_line:
        lines.append(f"{hex(v_offset).ljust(v_offset_width, ' ')}" + data_line)
    return lines
