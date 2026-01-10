"""
Document assembly for Kakuro puzzle books.

This module handles the creation of multi-page PDF documents,
assembling puzzle pages, solution sections, and other book elements.
"""

import logging
from pathlib import Path
from typing import Union

from reportlab.pdfgen.canvas import Canvas

from src.puzzle_generation import Puzzle
from .models import BookConfig
from .page_builder import build_puzzle_page, build_solution_page
from .compliance import apply_compliance

logger = logging.getLogger(__name__)


class PDFDocument:
    """Multi-page PDF document builder for Kakuro puzzle books."""

    def __init__(
        self,
        output_path: Union[str, Path],
        config: BookConfig = None,
        is_compliant: bool = True,
    ):
        """Initialize a new PDF document.

        Args:
            output_path: Path where the PDF will be saved.
            config: Book configuration. Uses defaults if not provided.
            is_compliant: Whether to apply PDF/X-1a compliance settings.
        """
        self.output_path = Path(output_path)
        self.config = config or BookConfig()
        self.is_compliant = is_compliant
        self.layout = self.config.layout

        # Create the canvas
        page_width, page_height = self.layout.page_size
        self.canvas = Canvas(
            str(self.output_path),
            pagesize=(page_width, page_height),
        )

        # Set document metadata
        self.canvas.setTitle(self.config.title)
        self.canvas.setAuthor(self.config.author)

        self._puzzles: list[Puzzle] = []
        self._current_page = 0

    def add_puzzle(self, puzzle: Puzzle) -> None:
        """Add a puzzle to the document.

        Args:
            puzzle: Puzzle to add.
        """
        self._puzzles.append(puzzle)

    def add_puzzles(self, puzzles: list[Puzzle]) -> None:
        """Add multiple puzzles to the document.

        Args:
            puzzles: List of puzzles to add.
        """
        self._puzzles.extend(puzzles)

    def _render_puzzle_pages(self) -> None:
        """Render all puzzle pages."""
        puzzles_per_page = self.layout.puzzles_per_page
        puzzle_num = 1

        for i in range(0, len(self._puzzles), puzzles_per_page):
            batch = []
            for j in range(puzzles_per_page):
                if i + j < len(self._puzzles):
                    batch.append((puzzle_num, self._puzzles[i + j]))
                    puzzle_num += 1

            if batch:
                build_puzzle_page(self.canvas, batch, self.layout)
                self._current_page += 1
                self.canvas.showPage()

    def _render_solution_pages(self) -> None:
        """Render solution pages."""
        # Add a section header for solutions
        self._add_section_header("Solutions")

        # Render solutions in groups of 4 per page
        puzzle_num = 1
        for i in range(0, len(self._puzzles), 4):
            batch = []
            for j in range(4):
                if i + j < len(self._puzzles):
                    batch.append((puzzle_num, self._puzzles[i + j]))
                    puzzle_num += 1

            if batch:
                build_solution_page(self.canvas, batch, self.layout)
                self._current_page += 1
                self.canvas.showPage()

    def _add_section_header(self, title: str) -> None:
        """Add a section header page."""
        page_width, page_height = self.layout.page_size

        from src.book_builder.config import DEFAULT_FONTS

        self.canvas.setFont(DEFAULT_FONTS["heading"], 24)
        text_width = self.canvas.stringWidth(title, DEFAULT_FONTS["heading"], 24)
        x = (page_width - text_width) / 2
        y = page_height / 2

        self.canvas.drawString(x, y, title)
        self._current_page += 1
        self.canvas.showPage()

    def save(self) -> Path:
        """Render all content and save the PDF.

        Returns:
            Path to the saved PDF file.
        """
        logger.info(f"Generating PDF with {len(self._puzzles)} puzzles...")

        # Render puzzle pages
        self._render_puzzle_pages()

        # Render solution pages if configured
        if self.config.include_solutions and self._puzzles:
            self._render_solution_pages()

        # Apply PDF/X compliance settings
        if self.is_compliant:
            apply_compliance(self.canvas, self.config.title, self.config.author)

        # Save the document
        self.canvas.save()
        logger.info(f"PDF saved to {self.output_path}")

        return self.output_path


def create_puzzle_book(
    puzzles: list[Puzzle],
    output_path: Union[str, Path],
    config: BookConfig = None,
) -> Path:
    """Create a complete puzzle book PDF.

    This is a convenience function that creates a PDFDocument,
    adds all puzzles, and saves the result.

    Args:
        puzzles: List of puzzles to include in the book.
        output_path: Path where the PDF will be saved.
        config: Book configuration. Uses defaults if not provided.

    Returns:
        Path to the saved PDF file.
    """
    doc = PDFDocument(output_path, config)
    doc.add_puzzles(puzzles)
    return doc.save()
