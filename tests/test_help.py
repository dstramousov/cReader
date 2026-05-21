from fb2term.ui.help import (
    HELP_CLOSE_ENTRIES,
    READER_HELP_ENTRIES,
    HelpEntry,
    format_help_entries,
)


def test_reader_help_entries_include_all_reader_bindings() -> None:
    keys = {entry.key for entry in READER_HELP_ENTRIES}

    assert "F1" in keys
    assert "F2" in keys
    assert "PgDown / Space" in keys
    assert "PgUp" in keys
    assert "q / F10" in keys


def test_help_close_entries_include_modal_close_keys() -> None:
    assert HELP_CLOSE_ENTRIES == (HelpEntry("Esc / q", "Close help window"),)


def test_format_help_entries_aligns_actions() -> None:
    lines = format_help_entries(
        (
            HelpEntry("F1", "Help"),
            HelpEntry("PgDown / Space", "Next page"),
        )
    )

    assert lines == (
        "F1              Help",
        "PgDown / Space  Next page",
    )


def test_format_help_entries_handles_empty_input() -> None:
    assert format_help_entries(()) == ()
