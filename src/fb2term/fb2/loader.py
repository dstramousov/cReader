"""Book loading service."""

from __future__ import annotations

from pathlib import Path

from fb2term.domain.book import Book
from fb2term.fb2.parser import Fb2ParseError, parse_fb2_file


class BookLoadError(Exception):
    """Base error raised when a book cannot be loaded."""


class BookNotFoundError(BookLoadError):
    """Raised when a requested book path does not exist."""


class UnsupportedBookFormatError(BookLoadError):
    """Raised when a requested book format is unsupported."""


class BookParseError(BookLoadError):
    """Raised when a supported book cannot be parsed."""


def load_book(path: Path) -> Book:
    """Load a supported book from disk.

    Args:
        path: Path to a supported book file.

    Returns:
        Parsed book model.

    Raises:
        BookNotFoundError: If the path does not exist.
        UnsupportedBookFormatError: If the file format is unsupported.
        BookParseError: If the file cannot be parsed.
    """

    source_path = path.expanduser()
    if not source_path.exists():
        raise BookNotFoundError(f"Book file not found: {source_path}")
    if not source_path.is_file():
        raise BookNotFoundError(f"Book path is not a file: {source_path}")
    if source_path.suffix.lower() != ".fb2":
        raise UnsupportedBookFormatError(
            f"Unsupported book format: {source_path.suffix or '<none>'}"
        )

    try:
        return parse_fb2_file(source_path)
    except Fb2ParseError as exc:
        raise BookParseError(str(exc)) from exc
