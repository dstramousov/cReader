"""Pure menu formatting helpers for the reader UI."""

from __future__ import annotations

from datetime import datetime
from typing import Final

MENU_LEFT_TEXT: Final[str] = " F1 Help  F2 Theme  PgUp Prev  PgDn/Space Next  F10 Quit "


def format_clock_text(now: datetime | None = None) -> str:
    """Format menu clock text.

    Args:
        now: Optional datetime. Uses current local time when omitted.

    Returns:
        Clock text in HH:MM format.
    """

    value = now or datetime.now()
    return value.strftime("%H:%M")


def format_menu_text(*, width: int, theme_label: str, clock_text: str) -> str:
    """Format the top menu line with right-aligned clock.

    Args:
        width: Available widget width.
        theme_label: Active theme label.
        clock_text: Already formatted clock text.

    Returns:
        One-line menu text.
    """

    theme_text = f" Theme: {theme_label} " if theme_label else ""
    right_text = f"{theme_text}{clock_text}".strip()
    left_text = MENU_LEFT_TEXT
    if width <= 0:
        return left_text
    if len(left_text) + len(right_text) + 1 > width:
        compact_left = " F1 Help F2 Theme F10 Quit "
        if len(compact_left) + len(right_text) + 1 <= width:
            left_text = compact_left
        else:
            return left_text[:width]
    padding = max(width - len(left_text) - len(right_text), 1)
    return f"{left_text}{' ' * padding}{right_text}"
