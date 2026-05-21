"""Main reader screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.timer import Timer

from fb2term.domain.book import Book
from fb2term.layout.document import LayoutOptions, render_book
from fb2term.ui.screens.help_modal import HelpModal
from fb2term.ui.theme import Theme, get_next_theme_name, get_theme
from fb2term.ui.widgets.menu_bar import MenuBar
from fb2term.ui.widgets.reader_view import ReaderView
from fb2term.ui.widgets.status_bar import StatusBar


class ReaderScreen(Screen[None]):
    """Screen that displays a single opened book."""

    BINDINGS = [
        Binding("f1", "show_help", "Help"),
        Binding("f2", "switch_theme", "Theme"),
        Binding("q", "quit_app", "Quit"),
        Binding("f10", "quit_app", "Quit"),
        Binding("pagedown", "page_down", "Next page"),
        Binding("space", "page_down", "Next page"),
        Binding("pageup", "page_up", "Previous page"),
    ]

    CSS = """
    ReaderScreen {
        layout: vertical;
    }
    """

    def __init__(
        self,
        book: Book,
        *,
        theme_name: str | None = None,
        line_width: int = 88,
    ) -> None:
        """Initialize the reader screen.

        Args:
            book: Parsed book to display.
            theme_name: Optional UI theme name.
            line_width: Preferred rendered text width.
        """

        super().__init__()
        self.book = book
        self.theme: Theme = get_theme(theme_name)
        self.document = render_book(book, options=LayoutOptions(width=line_width))
        self.menu_bar: MenuBar | None = None
        self.reader_view: ReaderView | None = None
        self.status_bar: StatusBar | None = None
        self._clock_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        """Compose screen widgets.

        Yields:
            Top menu, reader viewport, and status bar widgets.
        """

        self.menu_bar = MenuBar()
        self.reader_view = ReaderView(self.document)
        self.status_bar = StatusBar("")
        yield self.menu_bar
        yield self.reader_view
        yield self.status_bar

    def on_mount(self) -> None:
        """Apply theme and initialize dynamic bars."""

        self._apply_theme()
        self._update_menu()
        self._update_status()
        self._clock_timer = self.set_interval(30.0, self._update_menu)

    def action_show_help(self) -> None:
        """Open keyboard help modal."""

        self.app.push_screen(HelpModal(self.theme))

    def action_switch_theme(self) -> None:
        """Switch to the next registered reader theme."""

        self.theme = get_theme(get_next_theme_name(self.theme.name))
        self._apply_theme()
        self._update_menu()
        self._update_status()

    def action_page_down(self) -> None:
        """Handle page-down navigation."""

        if self.reader_view is None:
            return
        self.reader_view.scroll_page_down()
        self._update_status()

    def action_page_up(self) -> None:
        """Handle page-up navigation."""

        if self.reader_view is None:
            return
        self.reader_view.scroll_page_up()
        self._update_status()

    def action_quit_app(self) -> None:
        """Exit the application."""

        self.app.exit()

    def _apply_theme(self) -> None:
        self.styles.background = self.theme.background
        self.styles.color = self.theme.foreground

        if self.menu_bar is not None:
            self.menu_bar.styles.background = self.theme.status_background
            self.menu_bar.styles.color = self.theme.status_foreground

        if self.reader_view is not None:
            self.reader_view.styles.background = self.theme.background
            self.reader_view.styles.color = self.theme.foreground

        if self.status_bar is not None:
            self.status_bar.styles.background = self.theme.status_background
            self.status_bar.styles.color = self.theme.status_foreground

    def _update_menu(self) -> None:
        if self.menu_bar is None:
            return
        self.menu_bar.update_menu(theme_label=self.theme.label)

    def _update_status(self) -> None:
        if self.reader_view is None or self.status_bar is None:
            return
        self.status_bar.update_status(
            title=self.book.title,
            offset=self.reader_view.offset,
            total_lines=self.document.line_count,
            viewport_height=self.reader_view.viewport_height,
            theme_label=self.theme.label,
        )
