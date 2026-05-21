import pytest

from fb2term.layout.wrapper import TextWrapError, display_width, wrap_paragraph, wrap_paragraphs


def test_display_width_handles_cyrillic() -> None:
    assert display_width("Привет") == 6


def test_wrap_paragraph_by_terminal_width() -> None:
    lines = wrap_paragraph("один два три четыре", width=9)

    assert lines == ("один два", "три", "четыре")
    assert all(display_width(line) <= 9 for line in lines)


def test_wrap_paragraph_breaks_long_words() -> None:
    lines = wrap_paragraph("сверхдлинноеслово", width=6)

    assert lines == ("сверхд", "линное", "слово")
    assert all(display_width(line) <= 6 for line in lines)


def test_wrap_paragraphs_inserts_spacing() -> None:
    lines = wrap_paragraphs(["один два", "три"], width=20, paragraph_spacing=1)

    assert lines == ("один два", "", "три")


def test_wrap_rejects_invalid_width() -> None:
    with pytest.raises(TextWrapError):
        wrap_paragraph("text", width=0)
