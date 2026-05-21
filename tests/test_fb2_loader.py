from pathlib import Path

import pytest

from fb2term.fb2.loader import (
    BookNotFoundError,
    UnsupportedBookFormatError,
    load_book,
)


MINIMAL_FB2 = """<?xml version="1.0" encoding="utf-8"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">
  <description>
    <title-info>
      <book-title>Test Book</book-title>
      <author><first-name>Ada</first-name><last-name>Lovelace</last-name></author>
      <lang>en</lang>
    </title-info>
  </description>
  <body><section><p>Hello world.</p></section></body>
</FictionBook>
"""


def test_load_book_reads_fb2_file(tmp_path: Path) -> None:
    path = tmp_path / "book.fb2"
    path.write_text(MINIMAL_FB2, encoding="utf-8")

    book = load_book(path)

    assert book.title == "Test Book"
    assert book.authors == ("Ada Lovelace",)
    assert book.path == path


def test_load_book_rejects_missing_path(tmp_path: Path) -> None:
    with pytest.raises(BookNotFoundError):
        load_book(tmp_path / "missing.fb2")


def test_load_book_rejects_unsupported_extension(tmp_path: Path) -> None:
    path = tmp_path / "book.txt"
    path.write_text("not fb2", encoding="utf-8")

    with pytest.raises(UnsupportedBookFormatError):
        load_book(path)
