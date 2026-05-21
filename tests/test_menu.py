from datetime import datetime

from fb2term.ui.menu import format_clock_text, format_menu_text


def test_format_clock_text_uses_hour_and_minute() -> None:
    assert format_clock_text(datetime(2026, 5, 21, 9, 7)) == "09:07"


def test_format_menu_text_right_aligns_theme_and_clock() -> None:
    text = format_menu_text(width=96, theme_label="Sepia", clock_text="14:37")

    assert text.startswith(" F1 Help  F2 Theme  F3 Contents")
    assert text.endswith("Theme: Sepia 14:37")
    assert len(text) == 96


def test_format_menu_text_uses_compact_menu_when_width_is_limited() -> None:
    text = format_menu_text(width=59, theme_label="Dark", clock_text="01:02")

    assert text.startswith(" F1 Help F2 Theme F3 Contents")
    assert text.endswith("Theme: Dark 01:02")
    assert len(text) == 59


def test_format_menu_text_truncates_when_width_is_too_small() -> None:
    text = format_menu_text(width=10, theme_label="Dark", clock_text="01:02")

    assert text == " F1 Help  "
