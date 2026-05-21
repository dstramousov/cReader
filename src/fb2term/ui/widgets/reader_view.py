"""Reader text viewport widget."""

from __future__ import annotations

from textual.events import Resize
from textual.reactive import reactive
from textual.widgets import Static

from fb2term.layout.document import RenderedDocument


class ReaderView(Static, can_focus=True):
    """A scrollable book text viewport."""

    DEFAULT_CSS = """
    ReaderView {
        height: 1fr;
        padding: 1 2;
    }
    """

    offset: reactive[int] = reactive(0)

    def __init__(self, document: RenderedDocument) -> None:
        """Initialize the reader viewport.

        Args:
            document: Rendered document lines.
        """

        super().__init__("")
        self.document = document

    def on_mount(self) -> None:
        """Refresh content when mounted."""

        self._refresh_content()
        self.focus()

    def on_resize(self, event: Resize) -> None:
        """Refresh content when the widget size changes.

        Args:
            event: Resize event.
        """

        event.stop()
        self.offset = self.document.clamp_offset(
            self.offset,
            viewport_height=self.viewport_height,
        )
        self._refresh_content()

    def watch_offset(self, _old_value: int, _new_value: int) -> None:
        """Refresh content after offset changes.

        Args:
            _old_value: Previous offset.
            _new_value: New offset.
        """

        self._refresh_content()

    @property
    def viewport_height(self) -> int:
        """Return the current viewport height.

        Returns:
            Positive viewport height.
        """

        return max(self.size.height, 1)

    def scroll_page_down(self) -> None:
        """Move the viewport one page down."""

        self.offset = self.document.clamp_offset(
            self.offset + self.viewport_height,
            viewport_height=self.viewport_height,
        )

    def scroll_page_up(self) -> None:
        """Move the viewport one page up."""

        self.offset = self.document.clamp_offset(
            self.offset - self.viewport_height,
            viewport_height=self.viewport_height,
        )

    def _refresh_content(self) -> None:
        lines = self.document.visible_lines(
            offset=self.offset,
            height=self.viewport_height,
        )
        self.update("\n".join(lines))
