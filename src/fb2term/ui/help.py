"""Keyboard help definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class HelpEntry:
    """A single keyboard help entry.

    Attributes:
        key: Key or key group shown to the user.
        action: Human-readable action description.
    """

    key: str
    action: str


READER_HELP_ENTRIES: Final[tuple[HelpEntry, ...]] = (
    HelpEntry("F1", "Show this help window"),
    HelpEntry("F2", "Switch theme"),
    HelpEntry("F3", "Show table of contents"),
    HelpEntry("↑ / ↓", "Scroll one line"),
    HelpEntry("PgDown / Space", "Next page"),
    HelpEntry("PgUp", "Previous page"),
    HelpEntry("q / F10", "Exit reader"),
)


HELP_CLOSE_ENTRIES: Final[tuple[HelpEntry, ...]] = (
    HelpEntry("Esc / q", "Close help window"),
)


def format_help_entries(entries: tuple[HelpEntry, ...]) -> tuple[str, ...]:
    """Format help entries as aligned text lines.

    Args:
        entries: Help entries to format.

    Returns:
        Formatted help lines.
    """

    if not entries:
        return ()
    key_width = max(len(entry.key) for entry in entries)
    return tuple(f"{entry.key:<{key_width}}  {entry.action}" for entry in entries)
