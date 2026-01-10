"""
CLI entry point for the book builder.

Usage:
    python -m book_builder build <book-id> [options]
    python -m book_builder list

Examples:
    python -m book_builder build beginner-to-expert-250
    python -m book_builder build beginner-to-expert-250 --chapters-only
    python -m book_builder build beginner-to-expert-250 --output custom.pdf
"""

import argparse
import logging
import sys
from pathlib import Path

# Configure ReportLab BEFORE any reportlab imports to prevent Helvetica registration
from .config import DEFAULT_FONTS
from reportlab import rl_config

rl_config.canvas_basefontname = DEFAULT_FONTS["body"]

from .builder import build_book, build_chapters_only, build_puzzles_only
from .config import BookConfig
from src.pdf_generation.fonts import register_fonts


def setup_logging(verbose: bool = False):
    """Configure logging for CLI output."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def find_books_dir() -> Path:
    """Find the books directory relative to the project root."""
    # Try common locations
    candidates = [
        Path("books"),
        Path(__file__).parent.parent.parent / "books",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError("Could not find 'books' directory")


def list_books():
    """List all available books."""
    books_dir = find_books_dir()
    print(f"\nAvailable books in {books_dir}:\n")

    for book_dir in sorted(books_dir.iterdir()):
        if book_dir.is_dir() and (book_dir / "book.yaml").exists():
            try:
                config = BookConfig.from_yaml(book_dir / "book.yaml")
                print(f"  {book_dir.name}")
                print(f"    Title: {config.metadata.title}")
                print(f"    Author: {config.metadata.author}")
                print()
            except Exception as e:
                print(f"  {book_dir.name} (error loading: {e})")


def cmd_validate(args):
    """Handle the validate command."""
    logger = logging.getLogger(__name__)

    books_dir = find_books_dir()
    book_dir = books_dir / args.book_id

    if not book_dir.exists():
        logger.error(f"Book not found: {args.book_id}")
        return 1

    config_path = book_dir / "book.yaml"
    if not config_path.exists():
        logger.error(f"No book.yaml found in {book_dir}")
        return 1

    try:
        config = BookConfig.from_yaml(config_path)
        print(f"✓ book.yaml is valid")
        print(f"  Title: {config.metadata.title}")
        print(f"  Chapters: {len(config.content.chapters)}")
        print(f"  Puzzle sections: {len(config.content.puzzle_sections)}")

        # Validate referenced files
        errors = config.validate_files(book_dir)
        if errors:
            print(f"\n✗ Found {len(errors)} missing file(s):")
            for error in errors:
                print(f"  - {error}")
            return 1
        else:
            print(f"✓ All referenced files exist")

        return 0

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def cmd_build(args):
    """Handle the build command."""
    logger = logging.getLogger(__name__)

    books_dir = find_books_dir()
    book_dir = books_dir / args.book_id

    if not book_dir.exists():
        logger.error(f"Book not found: {args.book_id}")
        logger.info(
            f"Available books: {[d.name for d in books_dir.iterdir() if d.is_dir()]}"
        )
        return 1

    config_path = book_dir / "book.yaml"
    if not config_path.exists():
        logger.error(f"No book.yaml found in {book_dir}")
        return 1

    # Determine output path
    output_path = None
    if args.output:
        output_path = Path(args.output)

    try:
        if args.chapters_only and args.puzzles_only:
            logger.error("Cannot use both --chapters-only and --puzzles-only")
            return 1
        elif args.chapters_only:
            logger.info(f"Building chapters only for: {args.book_id}")
            result = build_chapters_only(args.book_id, output_path)
        elif args.puzzles_only:
            logger.info(f"Building puzzles only for: {args.book_id}")
            result = build_puzzles_only(args.book_id, output_path)
        else:
            logger.info(f"Building full book: {args.book_id}")
            result = build_book(args.book_id, output_path)

        print(f"\n✓ Book built successfully: {result}")
        return 0

    except Exception as e:
        logger.error(f"Build failed: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def main():
    """Build Kakuro puzzle books from YAML configuration."""
    parser = argparse.ArgumentParser(
        prog="book_builder",
        description="Build Kakuro puzzle books from YAML configuration",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # build command
    build_parser = subparsers.add_parser("build", help="Build a book")
    build_parser.add_argument("book_id", help="Book ID (directory name in books/)")
    build_parser.add_argument(
        "--chapters-only",
        action="store_true",
        help="Build only chapters (skip puzzles)",
    )
    build_parser.add_argument(
        "--puzzles-only",
        action="store_true",
        help="Build only puzzles (skip chapters)",
    )
    build_parser.add_argument(
        "--output",
        "-o",
        help="Custom output path for the PDF",
    )

    # list command
    subparsers.add_parser("list", help="List available books")

    # validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate a book configuration"
    )
    validate_parser.add_argument("book_id", help="Book ID (directory name in books/)")

    args = parser.parse_args()
    setup_logging(args.verbose if hasattr(args, "verbose") else False)

    # Register custom fonts
    register_fonts()

    if args.command == "build":
        sys.exit(cmd_build(args))
    elif args.command == "list":
        list_books()
    elif args.command == "validate":
        sys.exit(cmd_validate(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
