"""Norton Commander inspired top menu bar."""

from __future__ import annotations

from textual.widgets import Static


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

        super().__init__(" F1 Help   PgUp Prev   PgDn/Space Next   F10 Quit ")
