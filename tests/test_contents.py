from fb2term.layout.document import ContentsEntry
from fb2term.ui.contents import (
    clamp_selected_index,
    format_contents_entries,
    get_contents_window_start,
)


def test_clamp_selected_index_handles_empty_entries() -> None:
    assert clamp_selected_index(10, 0) == 0


def test_clamp_selected_index_keeps_selection_in_range() -> None:
    assert clamp_selected_index(-1, 3) == 0
    assert clamp_selected_index(10, 3) == 2
    assert clamp_selected_index(1, 3) == 1


def test_get_contents_window_start_centers_selection_when_possible() -> None:
    assert get_contents_window_start(
        selected_index=8,
        entry_count=20,
        visible_count=5,
    ) == 6


def test_format_contents_entries_marks_selected_entry() -> None:
    entries = (
        ContentsEntry("s1", "Глава 1", 10, 1),
        ContentsEntry("s2", "Сон", 20, 2),
    )

    lines = format_contents_entries(
        entries,
        selected_index=1,
        width=40,
        visible_count=10,
    )

    assert lines == (
        "   1. Глава 1",
        ">  2.   Сон",
    )


def test_format_contents_entries_handles_empty_contents() -> None:
    assert format_contents_entries((), selected_index=0, width=40, visible_count=10) == (
        "No chapters found.",
    )


def test_format_contents_entries_truncates_long_titles() -> None:
    entries = (ContentsEntry("s1", "Очень длинное название главы", 0, 1),)

    lines = format_contents_entries(
        entries,
        selected_index=0,
        width=12,
        visible_count=10,
    )

    assert lines == (">  1. Очень…",)
