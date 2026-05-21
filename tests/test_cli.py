from pathlib import Path

from fb2term.cli import build_parser


def test_cli_parser_accepts_theme_and_book_path() -> None:
    args = build_parser().parse_args(["--theme", "sepia", "book.fb2"])

    assert args.theme == "sepia"
    assert args.book_path == Path("book.fb2")
