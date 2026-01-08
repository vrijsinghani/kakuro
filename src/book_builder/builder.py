"""
Book builder - main orchestration for building complete books.

This module provides the main entry points for building PDF books
from YAML configuration files.
"""

import logging
from pathlib import Path
from typing import Optional

from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    PageBreak,
)
from reportlab.lib.units import inch

from .config import BookConfig
from .chapter_renderer import ChapterRenderer

logger = logging.getLogger(__name__)

# Base directory for all books
BOOKS_DIR = Path(__file__).parent.parent.parent / "books"


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
    from .assembler import BookAssembler
    from .puzzle_flowable import PuzzleFlowable, SolutionFlowable

    book_dir = get_book_dir(book_id)
    config_path = book_dir / "book.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Book configuration not found: {config_path}")

    config = BookConfig.from_yaml(config_path)

    if output_path is None:
        output_dir = book_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "interior.pdf"

    cache_dir = book_dir / "output" / "puzzles"

    logger.info(f"Building book: {config.metadata.title}")

    # Initialize assembler
    assembler = BookAssembler(config, book_dir)

    # Build document
    doc = _create_document(output_path, config)
    flowables = []
    all_puzzles = []  # (puzzle_num, puzzle) for solutions

    # Front matter
    flowables.extend(assembler.build_title_page())
    flowables.extend(assembler.build_copyright_page())

    # Chapters (Part 1)
    flowables.extend(assembler.build_section_header("Part 1: How to Play"))

    renderer = ChapterRenderer(config, book_dir)
    for chapter_config in config.content.chapters:
        chapter_path = book_dir / chapter_config.path
        if not chapter_path.exists():
            logger.warning(f"Chapter not found: {chapter_path}")
            continue

        logger.info(f"Rendering chapter: {chapter_config.title}")
        chapter_flowables = renderer.render_chapter(chapter_path, chapter_config.title)
        flowables.extend(chapter_flowables)
        flowables.append(PageBreak())

    # Puzzle sections
    puzzle_num = 1
    max_puzzle_width = (
        config.page_width_points
        - (config.layout.margins.left + config.layout.margins.right) * 72
    )
    max_puzzle_height = (
        config.page_height_points
        - (config.layout.margins.top + config.layout.margins.bottom) * 72
    )

    # Map difficulty to display name
    difficulty_labels = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "expert": "Expert",
    }

    for section in config.content.puzzle_sections:
        # Section header
        flowables.extend(assembler.build_section_header(section.title))

        # Generate puzzles
        puzzles = assembler.generate_puzzles_for_section(section, cache_dir)

        difficulty_label = difficulty_labels.get(
            section.difficulty, section.difficulty.title()
        )

        # Add puzzles as flowables
        for puzzle in puzzles:
            pf = PuzzleFlowable(
                puzzle=puzzle,
                puzzle_number=puzzle_num,
                difficulty=difficulty_label,
                max_width=max_puzzle_width,
                max_height=max_puzzle_height,
                show_rules=True,
            )
            flowables.append(pf)
            flowables.append(PageBreak())

            all_puzzles.append((puzzle_num, puzzle, difficulty_label))
            puzzle_num += 1

    # Solutions section
    if all_puzzles:
        flowables.extend(assembler.build_section_header("Solutions"))

        # Add solutions in rows (multiple per page)
        from reportlab.platypus import Table

        solutions_per_row = 3
        solution_col_width = max_puzzle_width / solutions_per_row
        # Allow some height per row (page height / ~4 rows per page)
        solution_row_height = (max_puzzle_height - 40) / 4

        for i in range(0, len(all_puzzles), solutions_per_row):
            row_puzzles = all_puzzles[i : i + solutions_per_row]
            row_flowables = []

            for num, puzzle, _ in row_puzzles:  # Unpack with difficulty ignored
                sf = SolutionFlowable(
                    puzzle=puzzle,
                    puzzle_number=num,
                    max_cell_size=14,
                    max_width=solution_col_width - 10,  # Padding
                    max_height=solution_row_height - 10,
                )
                row_flowables.append(sf)

            # Pad row if needed
            while len(row_flowables) < solutions_per_row:
                row_flowables.append(Spacer(1, 1))

            # Create table for row
            table = Table(
                [row_flowables], colWidths=[solution_col_width] * solutions_per_row
            )
            flowables.append(table)
            flowables.append(Spacer(1, 10))

    # Build the PDF
    doc.build(flowables, onFirstPage=_add_page_number, onLaterPages=_add_page_number)
    logger.info(f"Book saved to: {output_path}")

    return output_path


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

    # Build document
    doc = _create_document(output_path, config)
    flowables = []

    # Add chapters
    renderer = ChapterRenderer(config, book_dir)
    for chapter_config in config.content.chapters:
        chapter_path = book_dir / chapter_config.path
        if not chapter_path.exists():
            logger.warning(f"Chapter not found: {chapter_path}")
            continue

        logger.info(f"Rendering chapter: {chapter_config.title}")
        chapter_flowables = renderer.render_chapter(chapter_path, chapter_config.title)
        flowables.extend(chapter_flowables)
        flowables.append(PageBreak())

    # Build the PDF with page numbers
    doc.build(flowables, onFirstPage=_add_page_number, onLaterPages=_add_page_number)
    logger.info(f"Chapters saved to: {output_path}")

    return output_path


def _create_document(output_path: Path, config: BookConfig) -> SimpleDocTemplate:
    """Create a ReportLab document with proper page settings.

    Args:
        output_path: Path for the output PDF.
        config: Book configuration.

    Returns:
        Configured SimpleDocTemplate.
    """
    page_width = config.page_width_points
    page_height = config.page_height_points
    margins = config.layout.margins

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=(page_width, page_height),
        leftMargin=margins.left * inch,
        rightMargin=margins.right * inch,
        topMargin=margins.top * inch,
        bottomMargin=margins.bottom * inch,
        title=config.metadata.title,
        author=config.metadata.author,
    )

    return doc


def _add_page_number(canvas, doc):
    """Add page number to bottom center of each page.

    Args:
        canvas: ReportLab canvas.
        doc: Document being built.
    """
    page_num = canvas.getPageNumber()
    text = str(page_num)

    canvas.saveState()
    canvas.setFont("Helvetica", 11)

    # Bottom center
    page_width = doc.pagesize[0]
    canvas.drawCentredString(page_width / 2, 0.5 * inch, text)

    canvas.restoreState()
