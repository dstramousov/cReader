"""Minimal FB2 parser."""

from __future__ import annotations

import hashlib
import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Final

from fb2term.domain.book import Book, Section

LOGGER = logging.getLogger(__name__)
_WHITESPACE_RE: Final[re.Pattern[str]] = re.compile(r"\s+")
_SECTION_TEXT_TAGS: Final[frozenset[str]] = frozenset(
    {"p", "subtitle", "poem", "cite", "text-author"}
)


class Fb2ParseError(Exception):
    """Raised when an FB2 document cannot be parsed."""


def parse_fb2_file(path: Path) -> Book:
    """Parse an FB2 file from disk.

    Args:
        path: Path to an FB2 file.

    Returns:
        Parsed book model.

    Raises:
        Fb2ParseError: If the file cannot be read or parsed.
    """

    source_path = path.expanduser()
    try:
        data = source_path.read_bytes()
    except OSError as exc:
        raise Fb2ParseError(f"Cannot read FB2 file: {source_path}") from exc

    return parse_fb2_bytes(data, source_path=source_path)


def parse_fb2_text(text: str, *, source_path: Path | None = None) -> Book:
    """Parse an FB2 document from a string.

    Args:
        text: FB2 XML text.
        source_path: Optional source path used for metadata and book ID.

    Returns:
        Parsed book model.

    Raises:
        Fb2ParseError: If XML parsing fails.
    """

    return parse_fb2_bytes(text.encode("utf-8"), source_path=source_path)


def parse_fb2_bytes(data: bytes, *, source_path: Path | None = None) -> Book:
    """Parse an FB2 document from bytes.

    Args:
        data: FB2 XML bytes.
        source_path: Optional source path used for metadata and book ID.

    Returns:
        Parsed book model.

    Raises:
        Fb2ParseError: If XML parsing fails or the root is not FB2-like.
    """

    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise Fb2ParseError("Invalid FB2 XML") from exc

    if _local_name(root.tag) != "FictionBook":
        raise Fb2ParseError("XML root is not FictionBook")

    title_info = _find_first_descendant(root, "title-info")
    title = _extract_title(title_info)
    authors = _extract_authors(title_info)
    language = _extract_text_from_child(title_info, "lang")
    annotation = _extract_annotation(title_info)
    sections = _extract_sections(root)
    effective_path = source_path or Path("")

    return Book(
        id=_build_book_id(effective_path, title, authors, data),
        path=effective_path,
        title=title,
        authors=authors,
        language=language,
        annotation=annotation,
        sections=sections,
    )


def _build_book_id(
    source_path: Path,
    title: str,
    authors: tuple[str, ...],
    data: bytes,
) -> str:
    digest = hashlib.sha256()
    digest.update(str(source_path).encode("utf-8", errors="replace"))
    digest.update(b"\0")
    digest.update(title.encode("utf-8", errors="replace"))
    digest.update(b"\0")
    digest.update("|".join(authors).encode("utf-8", errors="replace"))
    digest.update(b"\0")
    digest.update(data[:1_048_576])
    return digest.hexdigest()[:24]


def _extract_title(title_info: ET.Element[str] | None) -> str:
    title = _extract_text_from_child(title_info, "book-title")
    return title or "Untitled"


def _extract_authors(title_info: ET.Element[str] | None) -> tuple[str, ...]:
    if title_info is None:
        return ()

    authors: list[str] = []
    for author in _iter_direct_children(title_info, "author"):
        parts = [
            _extract_text_from_child(author, "first-name"),
            _extract_text_from_child(author, "middle-name"),
            _extract_text_from_child(author, "last-name"),
            _extract_text_from_child(author, "nickname"),
        ]
        name = _normalize_text(" ".join(part for part in parts if part))
        if not name:
            name = _extract_plain_text(author)
        if name:
            authors.append(name)

    return tuple(authors)


def _extract_annotation(title_info: ET.Element[str] | None) -> str | None:
    annotation = _find_direct_child(title_info, "annotation")
    if annotation is None:
        return None

    paragraphs = [
        _extract_plain_text(child)
        for child in annotation
        if _local_name(child.tag) in _SECTION_TEXT_TAGS
    ]
    normalized = [paragraph for paragraph in paragraphs if paragraph]
    if normalized:
        return "\n\n".join(normalized)

    fallback = _extract_plain_text(annotation)
    return fallback or None


def _extract_sections(root: ET.Element[str]) -> tuple[Section, ...]:
    body = _find_first_descendant(root, "body")
    if body is None:
        LOGGER.debug("FB2 document has no body element")
        return ()

    sections = [
        _parse_section(section, section_path=f"body/section[{index}]")
        for index, section in enumerate(_iter_direct_children(body, "section"))
    ]
    if sections:
        return tuple(sections)

    paragraphs = _extract_direct_paragraphs(body)
    if not paragraphs:
        LOGGER.debug("FB2 body has no sections or direct paragraphs")
        return ()

    return (
        Section(
            id="body",
            title=None,
            paragraphs=paragraphs,
            children=(),
        ),
    )


def _parse_section(section: ET.Element[str], *, section_path: str) -> Section:
    title = _extract_section_title(section)
    paragraphs = _extract_direct_paragraphs(section)
    children = tuple(
        _parse_section(child, section_path=f"{section_path}/section[{index}]")
        for index, child in enumerate(_iter_direct_children(section, "section"))
    )

    return Section(
        id=section_path,
        title=title,
        paragraphs=paragraphs,
        children=children,
    )


def _extract_section_title(section: ET.Element[str]) -> str | None:
    title_node = _find_direct_child(section, "title")
    if title_node is None:
        return None

    paragraphs = [
        _extract_plain_text(child)
        for child in _iter_direct_children(title_node, "p")
    ]
    title = " ".join(paragraph for paragraph in paragraphs if paragraph)
    return _normalize_text(title) or None


def _extract_direct_paragraphs(parent: ET.Element[str]) -> tuple[str, ...]:
    paragraphs: list[str] = []
    for child in parent:
        tag_name = _local_name(child.tag)
        if tag_name in {"section", "title", "empty-line"}:
            continue
        if tag_name not in _SECTION_TEXT_TAGS:
            continue
        text = _extract_plain_text(child)
        if text:
            paragraphs.append(text)
    return tuple(paragraphs)


def _extract_text_from_child(
    parent: ET.Element[str] | None,
    child_name: str,
) -> str | None:
    child = _find_direct_child(parent, child_name)
    if child is None:
        return None
    return _extract_plain_text(child) or None


def _extract_plain_text(element: ET.Element[str]) -> str:
    return _normalize_text("".join(element.itertext()))


def _normalize_text(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def _find_first_descendant(
    parent: ET.Element[str],
    child_name: str,
) -> ET.Element[str] | None:
    for element in parent.iter():
        if _local_name(element.tag) == child_name:
            return element
    return None


def _find_direct_child(
    parent: ET.Element[str] | None,
    child_name: str,
) -> ET.Element[str] | None:
    if parent is None:
        return None
    for child in parent:
        if _local_name(child.tag) == child_name:
            return child
    return None


def _iter_direct_children(
    parent: ET.Element[str],
    child_name: str,
) -> tuple[ET.Element[str], ...]:
    return tuple(child for child in parent if _local_name(child.tag) == child_name)


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", maxsplit=1)[1]
    return tag
