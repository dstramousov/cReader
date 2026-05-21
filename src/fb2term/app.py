"""Textual application entrypoint."""

from __future__ import annotations

from textual.app import App

from fb2term.domain.book import Book
from fb2term.ui.screens.reader_screen import ReaderScreen


class Fb2TermApp(App[None]):
    """Minimal Textual application for reading one FB2 book."""

    TITLE = "FB2Term Reader"

    def __init__(self, book: Book, *, theme_name: str | None = None) -> None:
        """Initialize the application.

        Args:
            book: Parsed book to display.
            theme_name: Optional UI theme name.
        """

        super().__init__()
        self.book = book
        self.theme_name = theme_name

    def on_mount(self) -> None:
        """Open the reader screen on startup."""

        self.push_screen(ReaderScreen(self.book, theme_name=self.theme_name))


def run_reader(book: Book, *, theme_name: str | None = None) -> None:
    """Run the Textual reader app.

    Args:
        book: Parsed book to display.
        theme_name: Optional UI theme name.
    """

    Fb2TermApp(book, theme_name=theme_name).run()
