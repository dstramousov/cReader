"""Reader help modal screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Static

from fb2term.ui.help import HELP_CLOSE_ENTRIES, READER_HELP_ENTRIES, format_help_entries
from fb2term.ui.theme import Theme


class HelpModal(ModalScreen[None]):
    """A Norton Commander inspired help modal."""

    BINDINGS = [
        Binding("escape", "close_help", "Close help"),
        Binding("q", "close_help", "Close help"),
    ]

    CSS = """
    HelpModal {
        align: center middle;
    }

    #help-dialog {
        width: 58;
        height: auto;
        padding: 1 2;
        border: double $accent;
    }
    """

    def __init__(self, theme: Theme) -> None:
        """Initialize the help modal.

        Args:
            theme: Active UI theme.
        """

        super().__init__()
        self.theme = theme
        self.dialog: Static | None = None

    def compose(self) -> ComposeResult:
        """Compose modal widgets.

        Yields:
            Help dialog widget.
        """

        self.dialog = Static(self._build_help_text(), id="help-dialog")
        yield self.dialog

    def on_mount(self) -> None:
        """Apply active theme colors."""

        self.styles.background = self.theme.background
        if self.dialog is not None:
            self.dialog.styles.background = self.theme.status_background
            self.dialog.styles.color = self.theme.status_foreground
            self.dialog.styles.border = ("double", self.theme.accent)

    def action_close_help(self) -> None:
        """Close the help modal."""

        self.dismiss(None)

    def _build_help_text(self) -> str:
        title = " FB2Term Help "
        reader_lines = format_help_entries(READER_HELP_ENTRIES)
        close_lines = format_help_entries(HELP_CLOSE_ENTRIES)
        lines = [title, "", "Reader keys:", *reader_lines, "", "Help window:", *close_lines]
        return "\n".join(lines)
