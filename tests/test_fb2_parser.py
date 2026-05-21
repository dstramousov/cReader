from pathlib import Path

import pytest

from fb2term.fb2 import Fb2ParseError, parse_fb2_text


MINIMAL_FB2 = """<?xml version="1.0" encoding="utf-8"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">
  <description>
    <title-info>
      <genre>prose</genre>
      <author>
        <first-name>Victor</first-name>
        <last-name>Pelevin</last-name>
      </author>
      <book-title>Чапаев и Пустота</book-title>
      <annotation>
        <p>Аннотация с <emphasis>разметкой</emphasis>.</p>
      </annotation>
      <lang>ru</lang>
    </title-info>
  </description>
  <body>
    <section>
      <title><p>Глава 1</p></title>
      <p>Первый абзац.</p>
      <p>Второй <strong>абзац</strong>.</p>
      <section>
        <title><p>Вложенная глава</p></title>
        <p>Текст внутри.</p>
      </section>
    </section>
  </body>
</FictionBook>
"""


def test_parse_fb2_metadata_and_sections() -> None:
    book = parse_fb2_text(MINIMAL_FB2, source_path=Path("book.fb2"))

    assert book.title == "Чапаев и Пустота"
    assert book.authors == ("Victor Pelevin",)
    assert book.language == "ru"
    assert book.annotation == "Аннотация с разметкой."
    assert len(book.id) == 24
    assert book.path == Path("book.fb2")

    assert len(book.sections) == 1
    section = book.sections[0]
    assert section.id == "body/section[0]"
    assert section.title == "Глава 1"
    assert section.paragraphs == ("Первый абзац.", "Второй абзац.")
    assert len(section.children) == 1
    assert section.children[0].id == "body/section[0]/section[0]"
    assert section.children[0].title == "Вложенная глава"


def test_parse_fb2_rejects_invalid_xml() -> None:
    with pytest.raises(Fb2ParseError):
        parse_fb2_text("<not-closed>")


def test_parse_fb2_rejects_non_fb2_root() -> None:
    with pytest.raises(Fb2ParseError):
        parse_fb2_text("<root />")
