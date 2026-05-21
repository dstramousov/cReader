"""Command-line interface for FB2Term."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from fb2term import __version__
from fb2term.fb2 import BookLoadError, load_book
from fb2term.ui.theme import DEFAULT_THEME_NAME, DEFAULT_THEME_REGISTRY

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
        "--theme",
        choices=DEFAULT_THEME_REGISTRY.names(),
        default=DEFAULT_THEME_NAME,
        help="UI theme name.",
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
        book = load_book(args.book_path)
    except BookLoadError as exc:
        LOGGER.debug("Failed to load book", exc_info=True)
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        from fb2term.app import run_reader
    except ImportError:
        LOGGER.debug("Failed to import Textual reader", exc_info=True)
        print(
            "error: Textual UI dependency is not installed. "
            "Install the project with dependencies first.",
            file=sys.stderr,
        )
        return 1

    try:
        run_reader(book, theme_name=args.theme)
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
