from pathlib import Path

import pytest

from fb2term.domain.book import Book, Section
from fb2term.layout.document import (
    DocumentLayoutError,
    LayoutOptions,
    RenderedDocument,
    render_book,
)


def test_render_book_flattens_metadata_and_sections() -> None:
    book = Book(
        id="book-id",
        path=Path("book.fb2"),
        title="Чапаев и Пустота",
        authors=("Victor Pelevin",),
        language="ru",
        annotation=None,
        sections=(
            Section(
                id="body/section[0]",
                title="Глава 1",
                paragraphs=("Первый абзац.", "Второй абзац."),
                children=(
                    Section(
                        id="body/section[0]/section[0]",
                        title="Сон",
                        paragraphs=("Текст сна.",),
                        children=(),
                    ),
                ),
            ),
        ),
    )

    document = render_book(book, options=LayoutOptions(width=20))

    assert "Чапаев и Пустота" in document.lines
    assert "Victor Pelevin" in document.lines
    assert "# Глава 1" in document.lines
    assert "## Сон" in document.lines
    assert "Первый абзац." in document.lines
    assert "Текст сна." in document.lines


def test_rendered_document_clamps_viewport_offset() -> None:
    document = RenderedDocument(lines=("1", "2", "3", "4"))

    assert document.clamp_offset(-10, viewport_height=2) == 0
    assert document.clamp_offset(10, viewport_height=2) == 2
    assert document.visible_lines(offset=2, height=2) == ("3", "4")


def test_rendered_document_rejects_invalid_viewport_height() -> None:
    document = RenderedDocument(lines=("1",))

    with pytest.raises(DocumentLayoutError):
        document.visible_lines(offset=0, height=0)
