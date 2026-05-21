"""Reader table-of-contents modal screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Static

from fb2term.layout.document import ContentsEntry
from fb2term.ui.contents import clamp_selected_index, format_contents_entries
from fb2term.ui.theme import Theme

_CONTENTS_WIDTH = 68
_VISIBLE_ENTRY_COUNT = 16


class ContentsModal(ModalScreen[int | None]):
    """A Norton Commander inspired table-of-contents modal."""

    BINDINGS = [
        Binding("up", "select_previous", "Previous chapter"),
        Binding("down", "select_next", "Next chapter"),
        Binding("enter", "go_to_selected", "Go to chapter"),
        Binding("escape", "close_contents", "Close contents"),
        Binding("q", "close_contents", "Close contents"),
    ]

    CSS = """
    ContentsModal {
        align: center middle;
        background: transparent;
    }

    #contents-dialog {
        width: 74;
        height: auto;
        padding: 1 2;
        border: double $accent;
    }
    """

    selected_index: reactive[int] = reactive(0)

    def __init__(self, theme: Theme, entries: tuple[ContentsEntry, ...]) -> None:
        """Initialize the contents modal.

        Args:
            theme: Active UI theme.
            entries: Available table-of-contents entries.
        """

        super().__init__()
        self.theme = theme
        self.entries = entries
        self.dialog: Static | None = None

    def compose(self) -> ComposeResult:
        """Compose modal widgets.

        Yields:
            Contents dialog widget.
        """

        self.dialog = Static(self._build_contents_text(), id="contents-dialog")
        yield self.dialog

    def on_mount(self) -> None:
        """Apply active theme colors."""

        if self.dialog is not None:
            self.dialog.styles.background = self.theme.status_background
            self.dialog.styles.color = self.theme.status_foreground
            self.dialog.styles.border = ("double", self.theme.accent)

    def watch_selected_index(self, _old_value: int, _new_value: int) -> None:
        """Refresh content after selection changes.

        Args:
            _old_value: Previous selected index.
            _new_value: New selected index.
        """

        self._refresh_content()

    def action_select_previous(self) -> None:
        """Move selection to the previous contents entry."""

        self.selected_index = clamp_selected_index(
            self.selected_index - 1,
            len(self.entries),
        )

    def action_select_next(self) -> None:
        """Move selection to the next contents entry."""

        self.selected_index = clamp_selected_index(
            self.selected_index + 1,
            len(self.entries),
        )

    def action_go_to_selected(self) -> None:
        """Dismiss the modal with the selected line offset."""

        if not self.entries:
            self.dismiss(None)
            return
        selected = clamp_selected_index(self.selected_index, len(self.entries))
        self.dismiss(self.entries[selected].line_offset)

    def action_close_contents(self) -> None:
        """Close the contents modal without navigation."""

        self.dismiss(None)

    def _refresh_content(self) -> None:
        if self.dialog is not None:
            self.dialog.update(self._build_contents_text())

    def _build_contents_text(self) -> str:
        title = " FB2Term Contents "
        entries = format_contents_entries(
            self.entries,
            selected_index=self.selected_index,
            width=_CONTENTS_WIDTH,
            visible_count=_VISIBLE_ENTRY_COUNT,
        )
        footer = "↑/↓ Select  Enter Go  Esc/q Close"
        lines = [title, "", *entries, "", footer]
        return "\n".join(lines)
