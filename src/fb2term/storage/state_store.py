"""Reader state persistence."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fb2term.paths import get_state_path

LOGGER = logging.getLogger(__name__)
_STATE_VERSION = 1


class StateStore:
    """JSON-backed reader state store."""

    def __init__(self, path: Path) -> None:
        """Initialize the store.

        Args:
            path: State file path.
        """

        self.path = path.expanduser()

    @classmethod
    def default(cls) -> "StateStore":
        """Create a store using the default state path.

        Returns:
            Default state store.
        """

        return cls(get_state_path())

    def load_position(self, book_id: str) -> int | None:
        """Load saved line offset for a book.

        Args:
            book_id: Stable book identifier.

        Returns:
            Saved non-negative line offset, or None when unavailable.
        """

        data = self._read_data()
        books = data.get("books")
        if not isinstance(books, dict):
            return None
        book_data = books.get(book_id)
        if not isinstance(book_data, dict):
            return None
        line_offset = book_data.get("line_offset")
        if not isinstance(line_offset, int):
            return None
        return max(line_offset, 0)

    def save_position(self, book_id: str, line_offset: int) -> None:
        """Persist reader line offset for a book.

        Args:
            book_id: Stable book identifier.
            line_offset: Current rendered document line offset.
        """

        data = self._read_data()
        books = data.setdefault("books", {})
        if not isinstance(books, dict):
            books = {}
            data["books"] = books

        books[book_id] = {
            "line_offset": max(line_offset, 0),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        data["version"] = _STATE_VERSION
        self._write_data(data)

    def _read_data(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": _STATE_VERSION, "books": {}}

        try:
            raw_data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            LOGGER.debug("Failed to read reader state", exc_info=True)
            return {"version": _STATE_VERSION, "books": {}}

        if not isinstance(raw_data, dict):
            return {"version": _STATE_VERSION, "books": {}}
        if not isinstance(raw_data.get("books"), dict):
            raw_data["books"] = {}
        raw_data["version"] = _STATE_VERSION
        return raw_data

    def _write_data(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_name(f"{self.path.name}.tmp")
        payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        temp_path.write_text(f"{payload}\n", encoding="utf-8")
        temp_path.replace(self.path)
