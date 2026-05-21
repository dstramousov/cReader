"""Pure table-of-contents formatting helpers."""

from __future__ import annotations

from fb2term.layout.document import ContentsEntry

_EMPTY_CONTENTS_TEXT = "No chapters found."


def clamp_selected_index(index: int, entry_count: int) -> int:
    """Clamp a selected contents index.

    Args:
        index: Requested selected index.
        entry_count: Number of available entries.

    Returns:
        Clamped index. Returns zero when there are no entries.
    """

    if entry_count <= 0:
        return 0
    return min(max(index, 0), entry_count - 1)


def get_contents_window_start(
    *,
    selected_index: int,
    entry_count: int,
    visible_count: int,
) -> int:
    """Return the first visible contents entry index.

    Args:
        selected_index: Current selected entry index.
        entry_count: Total number of entries.
        visible_count: Maximum number of visible entries.

    Returns:
        First visible entry index.
    """

    if entry_count <= 0 or visible_count <= 0:
        return 0
    selected = clamp_selected_index(selected_index, entry_count)
    half_window = visible_count // 2
    max_start = max(entry_count - visible_count, 0)
    return min(max(selected - half_window, 0), max_start)


def format_contents_entries(
    entries: tuple[ContentsEntry, ...],
    *,
    selected_index: int,
    width: int,
    visible_count: int,
) -> tuple[str, ...]:
    """Format a visible contents window.

    Args:
        entries: Available contents entries.
        selected_index: Current selected entry index.
        width: Maximum line width.
        visible_count: Maximum number of visible entries.

    Returns:
        Formatted visible lines.
    """

    if not entries:
        return (_truncate(_EMPTY_CONTENTS_TEXT, width),)
    if visible_count <= 0:
        return ()

    selected = clamp_selected_index(selected_index, len(entries))
    start = get_contents_window_start(
        selected_index=selected,
        entry_count=len(entries),
        visible_count=visible_count,
    )
    end = min(start + visible_count, len(entries))

    lines: list[str] = []
    for absolute_index in range(start, end):
        entry = entries[absolute_index]
        pointer = ">" if absolute_index == selected else " "
        indent = "  " * max(entry.level - 1, 0)
        line_number = absolute_index + 1
        line = f"{pointer} {line_number:>2}. {indent}{entry.title}"
        lines.append(_truncate(line, width))
    return tuple(lines)


def _truncate(text: str, width: int) -> str:
    if width <= 0:
        return ""
    if len(text) <= width:
        return text
    if width == 1:
        return "…"
    return f"{text[: width - 1]}…"
