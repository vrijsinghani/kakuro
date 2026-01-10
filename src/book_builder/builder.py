"""
Book builder - main orchestration for building complete books.

This module provides the main entry points for building PDF books
from YAML configuration files.
"""

import logging
import subprocess
import shutil
from pathlib import Path
from typing import Optional

from .config import BookConfig, PartHeaderConfig, ChapterConfig, PuzzleSectionConfig
from .document import BookDocument

logger = logging.getLogger(__name__)

# Base directory for all books
BOOKS_DIR = Path(__file__).parent.parent.parent / "books"


def embed_fonts(input_pdf: Path) -> Path:
    """Post-process PDF to embed all fonts using Ghostscript.

    Args:
        input_pdf: Path to the input PDF file.

    Returns:
        Path to the processed PDF (same file, modified in place).

    Raises:
        RuntimeError: If Ghostscript is not available or fails.
    """
    # Check if Ghostscript is available
    gs_path = shutil.which("gs")
    if not gs_path:
        raise RuntimeError(
            "Ghostscript (gs) not found. Install it with: sudo apt install ghostscript"
        )

    # Create temp output file
    output_pdf = input_pdf.with_suffix(".embedded.pdf")

    cmd = [
        gs_path,
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        "-dEmbedAllFonts=true",
        "-dSubsetFonts=true",
        "-dPDFSETTINGS=/prepress",
        f"-sOutputFile={output_pdf}",
        str(input_pdf),
    ]

    logger.info("Embedding fonts with Ghostscript...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Ghostscript failed: {result.stderr}")

    # Replace original with embedded version
    output_pdf.replace(input_pdf)
    logger.info("Fonts embedded successfully")

    return input_pdf


def get_book_dir(book_id: str) -> Path:
    """Get the directory for a book.

    Args:
        book_id: Book identifier (directory name).

    Returns:
        Path to the book directory.
    """
    return BOOKS_DIR / book_id


def build_book(book_id: str, output_path: Optional[Path] = None) -> Path:
    """Build a complete book from configuration.

    Args:
        book_id: Book identifier (directory name under books/).
        output_path: Optional output path.
            Defaults to books/{book_id}/output/interior.pdf

    Returns:
        Path to the generated PDF.
    """
    book_dir = get_book_dir(book_id)
    config_path = book_dir / "book.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Book configuration not found: {config_path}")

    config = BookConfig.from_yaml(config_path)
    cache_dir = book_dir / "output" / "puzzles"

    logger.info(f"Building book: {config.metadata.title}")

    # Create document using new BookDocument class
    doc = BookDocument(config, book_dir)

    # Front matter
    doc.add_title_page()
    doc.add_copyright_page()

    # TOC placeholder (if configured)
    for item in config.content.front_matter:
        if item.type == "toc":
            doc.add_toc_placeholder()
            break

    # Process body content
    for item in config.content.body:
        if isinstance(item, PartHeaderConfig):
            doc.add_section_header(item.title)
        elif isinstance(item, ChapterConfig):
            doc.add_chapter(Path(item.path), item.title)
        elif isinstance(item, PuzzleSectionConfig):
            doc.add_puzzle_section(item, cache_dir)

    # Back matter
    for item in config.content.back_matter:
        if item.type == "solutions":
            doc.add_solutions()
        elif item.type == "about_author":
            about_path = Path(item.path) if item.path else None
            doc.add_about_author(about_path)
        elif item.type == "notes":
            doc.add_notes_pages()

    # Finalize TOC and save
    doc.finalize_toc()
    pdf_path = doc.save(output_path)

    # Post-process to embed all fonts for KDP compliance
    return embed_fonts(pdf_path)


def build_chapters_only(book_id: str, output_path: Optional[Path] = None) -> Path:
    """Build only the chapter content (no puzzles).

    Args:
        book_id: Book identifier.
        output_path: Optional output path.

    Returns:
        Path to the generated PDF.
    """
    book_dir = get_book_dir(book_id)
    config_path = book_dir / "book.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Book configuration not found: {config_path}")

    config = BookConfig.from_yaml(config_path)

    if output_path is None:
        output_dir = book_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "chapters_only.pdf"

    logger.info(f"Building chapters for: {config.metadata.title}")

    # Create document using BookDocument class (chapters only)
    doc = BookDocument(config, book_dir)

    # Add chapters directly (no front matter or section headers)
    for item in config.content.body:
        if isinstance(item, ChapterConfig):
            doc.add_chapter(Path(item.path), item.title)

    return doc.save(output_path)


def build_puzzles_only(book_id: str, output_path: Optional[Path] = None) -> Path:
    """Build only the puzzle sections (no chapters).

    Args:
        book_id: Book identifier.
        output_path: Optional output path.

    Returns:
        Path to the generated PDF.
    """
    book_dir = get_book_dir(book_id)
    config_path = book_dir / "book.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Book configuration not found: {config_path}")

    config = BookConfig.from_yaml(config_path)
    cache_dir = book_dir / "output" / "puzzles"

    if output_path is None:
        output_dir = book_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "puzzles_only.pdf"

    logger.info(f"Building puzzles for: {config.metadata.title}")

    # Create document using BookDocument class (puzzles only)
    doc = BookDocument(config, book_dir)

    # Add puzzle sections
    for item in config.content.body:
        if isinstance(item, PuzzleSectionConfig):
            doc.add_puzzle_section(item, cache_dir)

    # Add solutions
    doc.add_solutions()

    return doc.save(output_path)
