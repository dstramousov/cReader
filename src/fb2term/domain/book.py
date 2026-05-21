"""Book-related domain models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Section:
    """A logical section of a parsed book.

    Attributes:
        id: Stable section identifier derived from the XML tree path.
        title: Optional section title.
        paragraphs: Text paragraphs that belong directly to this section.
        children: Nested subsections.
    """

    id: str
    title: str | None
    paragraphs: tuple[str, ...]
    children: tuple["Section", ...]


@dataclass(frozen=True, slots=True)
class Book:
    """A parsed FB2 book.

    Attributes:
        id: Stable book identifier for state and bookmarks.
        path: Source file path.
        title: Book title.
        authors: Book authors.
        language: Optional book language.
        annotation: Optional annotation text.
        sections: Top-level book sections.
    """

    id: str
    path: Path
    title: str
    authors: tuple[str, ...]
    language: str | None
    annotation: str | None
    sections: tuple[Section, ...]
