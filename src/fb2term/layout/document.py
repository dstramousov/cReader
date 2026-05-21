"""Book-to-lines layout helpers."""

from __future__ import annotations

from dataclasses import dataclass

from fb2term.domain.book import Book, Section
from fb2term.layout.wrapper import TextWrapError, wrap_paragraph


class DocumentLayoutError(ValueError):
    """Raised when document layout options are invalid."""


@dataclass(frozen=True, slots=True)
class LayoutOptions:
    """Options for rendering a book into terminal lines.

    Attributes:
        width: Maximum terminal cell width for a rendered line.
        paragraph_spacing: Empty lines inserted between paragraphs.
        section_spacing: Empty lines inserted around section headings.
    """

    width: int = 88
    paragraph_spacing: int = 1
    section_spacing: int = 1

    def __post_init__(self) -> None:
        """Validate layout options.

        Raises:
            DocumentLayoutError: If an option value is invalid.
        """

        if self.width <= 0:
            raise DocumentLayoutError("Width must be positive")
        if self.paragraph_spacing < 0:
            raise DocumentLayoutError("Paragraph spacing cannot be negative")
        if self.section_spacing < 0:
            raise DocumentLayoutError("Section spacing cannot be negative")


@dataclass(frozen=True, slots=True)
class ContentsEntry:
    """A jump target in the rendered table of contents.

    Attributes:
        section_id: Stable section identifier.
        title: Display title for the section.
        line_offset: Rendered document line offset for the section.
        level: Nesting level starting at one.
    """

    section_id: str
    title: str
    line_offset: int
    level: int


@dataclass(frozen=True, slots=True)
class RenderedDocument:
    """A book rendered into terminal-display lines.

    Attributes:
        lines: Rendered text lines.
        contents: Jump targets for titled and untitled sections.
    """

    lines: tuple[str, ...]
    contents: tuple[ContentsEntry, ...] = ()

    @property
    def line_count(self) -> int:
        """Return the number of rendered lines.

        Returns:
            Rendered line count.
        """

        return len(self.lines)

    def clamp_offset(self, offset: int, *, viewport_height: int) -> int:
        """Clamp a viewport offset to a valid document range.

        Args:
            offset: Requested top-line offset.
            viewport_height: Number of lines visible in the viewport.

        Returns:
            Clamped offset.

        Raises:
            DocumentLayoutError: If the viewport height is invalid.
        """

        if viewport_height <= 0:
            raise DocumentLayoutError("Viewport height must be positive")
        max_offset = max(self.line_count - viewport_height, 0)
        return min(max(offset, 0), max_offset)

    def visible_lines(self, *, offset: int, height: int) -> tuple[str, ...]:
        """Return lines visible in the requested viewport.

        Args:
            offset: Requested top-line offset.
            height: Number of visible lines.

        Returns:
            Visible document lines.

        Raises:
            DocumentLayoutError: If the viewport height is invalid.
        """

        safe_offset = self.clamp_offset(offset, viewport_height=height)
        return self.lines[safe_offset : safe_offset + height]


def render_book(
    book: Book,
    *,
    options: LayoutOptions | None = None,
) -> RenderedDocument:
    """Render a parsed book into terminal-display lines.

    Args:
        book: Parsed book model.
        options: Optional layout options.

    Returns:
        Rendered document.

    Raises:
        DocumentLayoutError: If rendering options are invalid.
    """

    layout_options = options or LayoutOptions()
    lines: list[str] = []
    contents: list[ContentsEntry] = []

    _append_wrapped(lines, book.title, options=layout_options)
    if book.authors:
        _append_wrapped(lines, ", ".join(book.authors), options=layout_options)
    _append_blank_lines(lines, 1)

    if book.annotation:
        _append_wrapped(lines, "Annotation", options=layout_options)
        _append_paragraph(lines, book.annotation, options=layout_options)
        _append_blank_lines(lines, 1)

    for index, section in enumerate(book.sections, start=1):
        _append_section(
            lines,
            contents,
            section,
            level=1,
            ordinal_path=(index,),
            options=layout_options,
        )

    if not book.sections:
        _append_wrapped(lines, "No readable sections found.", options=layout_options)

    return RenderedDocument(lines=tuple(lines), contents=tuple(contents))


def _append_section(
    lines: list[str],
    contents: list[ContentsEntry],
    section: Section,
    *,
    level: int,
    ordinal_path: tuple[int, ...],
    options: LayoutOptions,
) -> None:
    title = section.title or f"Section {_format_ordinal_path(ordinal_path)}"
    line_offset = len(lines)
    contents.append(
        ContentsEntry(
            section_id=section.id,
            title=title,
            line_offset=line_offset,
            level=level,
        )
    )

    if section.title:
        if lines and lines[-1] != "":
            _append_blank_lines(lines, options.section_spacing)
        marker = "#" * min(level, 6)
        _append_wrapped(lines, f"{marker} {section.title}", options=options)
        _append_blank_lines(lines, options.section_spacing)

    for index, paragraph in enumerate(section.paragraphs):
        if index > 0:
            _append_blank_lines(lines, options.paragraph_spacing)
        _append_paragraph(lines, paragraph, options=options)

    for index, child in enumerate(section.children, start=1):
        _append_section(
            lines,
            contents,
            child,
            level=level + 1,
            ordinal_path=(*ordinal_path, index),
            options=options,
        )


def _format_ordinal_path(ordinal_path: tuple[int, ...]) -> str:
    return ".".join(str(value) for value in ordinal_path)


def _append_paragraph(
    lines: list[str],
    paragraph: str,
    *,
    options: LayoutOptions,
) -> None:
    for wrapped_line in _wrap_text(paragraph, options=options):
        lines.append(wrapped_line)


def _append_wrapped(lines: list[str], text: str, *, options: LayoutOptions) -> None:
    for wrapped_line in _wrap_text(text, options=options):
        lines.append(wrapped_line)


def _wrap_text(text: str, *, options: LayoutOptions) -> tuple[str, ...]:
    try:
        return wrap_paragraph(text, width=options.width)
    except TextWrapError as exc:
        raise DocumentLayoutError(str(exc)) from exc


def _append_blank_lines(lines: list[str], count: int) -> None:
    for _ in range(count):
        if lines and lines[-1] == "":
            continue
        lines.append("")
