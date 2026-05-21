"""Reader status bar widget."""

from __future__ import annotations

from textual.widgets import Static


class StatusBar(Static):
    """A compact reader status bar."""

    DEFAULT_CSS = """
    StatusBar {
        dock: bottom;
        height: 1;
        padding: 0 1;
    }
    """

    def update_status(
        self,
        *,
        title: str,
        offset: int,
        total_lines: int,
        viewport_height: int,
        theme_label: str,
    ) -> None:
        """Update the displayed reader status.

        Args:
            title: Book title.
            offset: Current viewport offset.
            total_lines: Total rendered line count.
            viewport_height: Visible viewport height.
            theme_label: Active UI theme label.
        """

        progress = _calculate_progress(
            offset=offset,
            total_lines=total_lines,
            viewport_height=viewport_height,
        )
        self.update(f"{title} | {progress:5.1f}% | theme: {theme_label} | q: quit")


def _calculate_progress(
    *,
    offset: int,
    total_lines: int,
    viewport_height: int,
) -> float:
    if total_lines <= 0:
        return 100.0
    visible_end = min(max(offset, 0) + max(viewport_height, 1), total_lines)
    return visible_end / total_lines * 100.0
