import json
from pathlib import Path

from fb2term.storage import StateStore


def test_state_store_saves_and_loads_position(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.json")

    store.save_position("book-id", 42)

    assert store.load_position("book-id") == 42


def test_state_store_returns_none_for_missing_book(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.json")

    assert store.load_position("missing") is None


def test_state_store_clamps_negative_offsets(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.json")

    store.save_position("book-id", -5)

    assert store.load_position("book-id") == 0


def test_state_store_ignores_corrupt_json(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    path.write_text("{broken", encoding="utf-8")
    store = StateStore(path)

    assert store.load_position("book-id") is None


def test_state_store_preserves_existing_books(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "books": {
                    "old-book": {
                        "line_offset": 7,
                        "updated_at": "2026-05-21T00:00:00+00:00",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    store = StateStore(path)

    store.save_position("new-book", 11)

    assert store.load_position("old-book") == 7
    assert store.load_position("new-book") == 11
