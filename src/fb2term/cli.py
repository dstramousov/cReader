"""Command-line interface for FB2Term."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from fb2term import __version__
from fb2term.fb2 import Fb2ParseError, parse_fb2_file

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        Configured argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="fb2term",
        description="Minimal terminal reader for FB2 books.",
    )
    parser.add_argument(
        "book_path",
        nargs="?",
        type=Path,
        help="Path to an FB2 book.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"fb2term {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI entrypoint.

    Args:
        argv: Optional command-line arguments. Uses sys.argv when omitted.

    Returns:
        Process exit code.
    """

    logging.basicConfig(level=logging.WARNING)
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.book_path is None:
        parser.print_help()
        return 0

    try:
        book = parse_fb2_file(args.book_path)
    except Fb2ParseError as exc:
        LOGGER.debug("Failed to parse FB2 file", exc_info=True)
        print(f"error: {exc}", file=sys.stderr)
        return 1

    authors = ", ".join(book.authors) if book.authors else "Unknown author"
    section_count = len(book.sections)
    print(f"{book.title}\n{authors}\nsections: {section_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
