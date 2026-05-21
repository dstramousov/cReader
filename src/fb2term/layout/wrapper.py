"""Terminal-aware text wrapping helpers."""

from __future__ import annotations

from collections.abc import Iterable

from wcwidth import wcwidth, wcswidth


class TextWrapError(ValueError):
    """Raised when text wrapping options are invalid."""


def display_width(text: str) -> int:
    """Return terminal display width for text.

    Args:
        text: Source text.

    Returns:
        Terminal cell width.
    """

    width = wcswidth(text)
    if width >= 0:
        return width
    return sum(max(wcwidth(character), 0) for character in text)


def wrap_paragraph(paragraph: str, *, width: int) -> tuple[str, ...]:
    """Wrap one paragraph by terminal display width.

    Args:
        paragraph: Source paragraph text.
        width: Maximum terminal cell width for a line.

    Returns:
        Wrapped lines.

    Raises:
        TextWrapError: If width is not positive.
    """

    if width <= 0:
        raise TextWrapError("Width must be positive")

    normalized = " ".join(paragraph.split())
    if not normalized:
        return ("",)

    lines: list[str] = []
    current = ""
    for word in normalized.split(" "):
        current = _append_word(lines, current, word, width)

    if current:
        lines.append(current)

    return tuple(lines)


def wrap_paragraphs(
    paragraphs: Iterable[str],
    *,
    width: int,
    paragraph_spacing: int = 1,
) -> tuple[str, ...]:
    """Wrap multiple paragraphs by terminal display width.

    Args:
        paragraphs: Source paragraphs.
        width: Maximum terminal cell width for a line.
        paragraph_spacing: Empty lines inserted between paragraphs.

    Returns:
        Wrapped lines.

    Raises:
        TextWrapError: If options are invalid.
    """

    if paragraph_spacing < 0:
        raise TextWrapError("Paragraph spacing cannot be negative")

    result: list[str] = []
    spacing = ("",) * paragraph_spacing
    for paragraph in paragraphs:
        if result and spacing:
            result.extend(spacing)
        result.extend(wrap_paragraph(paragraph, width=width))
    return tuple(result)


def _append_word(lines: list[str], current: str, word: str, width: int) -> str:
    if display_width(word) > width:
        return _append_long_word(lines, current, word, width)

    candidate = word if not current else f"{current} {word}"
    if display_width(candidate) <= width:
        return candidate

    if current:
        lines.append(current)
    return word


def _append_long_word(lines: list[str], current: str, word: str, width: int) -> str:
    if current:
        lines.append(current)

    chunk = ""
    for character in word:
        candidate = f"{chunk}{character}"
        if chunk and display_width(candidate) > width:
            lines.append(chunk)
            chunk = character
        else:
            chunk = candidate

    return chunk
