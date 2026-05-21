"""Norton Commander inspired top menu bar."""

from __future__ import annotations

from datetime import datetime

from textual.events import Resize
from textual.widgets import Static

from fb2term.ui.menu import format_clock_text, format_menu_text


class MenuBar(Static):
    """A compact top command menu bar."""

    DEFAULT_CSS = """
    MenuBar {
        dock: top;
        height: 1;
        padding: 0 1;
        text-style: bold;
    }
    """

    def __init__(self) -> None:
        """Initialize the menu bar."""

        super().__init__("")
        self._theme_label = ""
        self._clock_text = format_clock_text()

    def on_mount(self) -> None:
        """Render menu text when mounted."""

        self._refresh_content()

    def on_resize(self, event: Resize) -> None:
        """Re-render menu text after terminal resize.

        Args:
            event: Resize event.
        """

        event.stop()
        self._refresh_content()

    def update_menu(self, *, theme_label: str, now: datetime | None = None) -> None:
        """Update dynamic menu fields.

        Args:
            theme_label: Active theme label.
            now: Optional clock source for deterministic tests.
        """

        self._theme_label = theme_label
        self._clock_text = format_clock_text(now)
        self._refresh_content()

    def _refresh_content(self) -> None:
        self.update(
            format_menu_text(
                width=self.size.width if self.size.width > 0 else 80,
                theme_label=self._theme_label,
                clock_text=self._clock_text,
            )
        )
