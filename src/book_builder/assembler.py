"""
Book assembler - combines all book elements into a complete PDF.

This module handles the assembly of front matter, chapters, puzzles,
solutions, and back matter into a cohesive book document.
"""

import json
import logging
from pathlib import Path
from datetime import datetime

from reportlab.platypus import (
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER

from .config import BookConfig, PuzzleSectionConfig
from .chapter_renderer import ChapterRenderer

logger = logging.getLogger(__name__)


class BookAssembler:
    """Assembles all book components into flowables."""

    def __init__(self, config: BookConfig, book_dir: Path):
        """Initialize book assembler.

        Args:
            config: Book configuration.
            book_dir: Base directory of the book.
        """
        self.config = config
        self.book_dir = book_dir
        self.chapter_renderer = ChapterRenderer(config, book_dir)
        self.toc_entries: list[tuple[str, int]] = []  # (title, page_num)
        self._current_page = 1

    def build_title_page(self) -> list:
        """Build the title page flowables."""
        flowables = []
        meta = self.config.metadata

        title_style = ParagraphStyle(
            "BookTitle",
            fontName="Helvetica-Bold",
            fontSize=32,
            leading=38,
            alignment=TA_CENTER,
            spaceAfter=20,
        )

        subtitle_style = ParagraphStyle(
            "BookSubtitle",
            fontName="Helvetica",
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=40,
            textColor=HexColor("#444444"),
        )

        author_style = ParagraphStyle(
            "BookAuthor",
            fontName="Helvetica",
            fontSize=14,
            leading=20,
            alignment=TA_CENTER,
        )

        # Vertical centering spacer
        flowables.append(Spacer(1, 2.5 * inch))

        # Title
        flowables.append(Paragraph(meta.title, title_style))

        # Subtitle
        if meta.subtitle:
            flowables.append(Paragraph(meta.subtitle, subtitle_style))

        # Author
        if meta.author:
            flowables.append(Spacer(1, 1 * inch))
            flowables.append(Paragraph(f"by {meta.author}", author_style))

        flowables.append(PageBreak())
        self._current_page += 1

        return flowables

    def build_copyright_page(self) -> list:
        """Build the copyright page flowables."""
        flowables = []

        style = ParagraphStyle(
            "Copyright",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
        )

        year = datetime.now().year
        meta = self.config.metadata

        flowables.append(Spacer(1, 6 * inch))

        lines = [
            f"© {year} {meta.author}" if meta.author else f"© {year}",
            "",
            "All rights reserved.",
            "",
            "No part of this publication may be reproduced, distributed, "
            "or transmitted",
            "in any form or by any means without the prior written "
            "permission of the publisher.",
        ]

        for line in lines:
            if line:
                flowables.append(Paragraph(line, style))
            else:
                flowables.append(Spacer(1, 12))

        flowables.append(PageBreak())
        self._current_page += 1

        return flowables

    def build_section_header(self, title: str) -> list:
        """Build a section header page."""
        flowables = []

        style = ParagraphStyle(
            "SectionHeader",
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
        )

        flowables.append(Spacer(1, 3 * inch))
        flowables.append(Paragraph(title, style))
        flowables.append(PageBreak())
        self._current_page += 1

        return flowables

    def generate_puzzles_for_section(
        self, section: PuzzleSectionConfig, cache_dir: Path
    ) -> list:
        """Generate or load puzzles for a section.

        Args:
            section: Puzzle section configuration.
            cache_dir: Directory for caching puzzles.

        Returns:
            List of Puzzle objects.
        """
        from src.puzzle_generation import generate_puzzle, Puzzle

        cache_file = cache_dir / f"{section.difficulty}_{section.count}.json"

        # Try to load from cache
        if cache_file.exists():
            logger.info(
                f"Loading {section.count} {section.difficulty} puzzles from cache"
            )
            with open(cache_file, "r") as f:
                data = json.load(f)
            return [Puzzle.from_dict(p) for p in data]

        # Generate puzzles
        logger.info(f"Generating {section.count} {section.difficulty} puzzles...")
        puzzles = []
        grid_sizes = section.grid_sizes

        for i in range(section.count):
            # Distribute puzzles across grid sizes
            size = grid_sizes[i % len(grid_sizes)]

            # Adjust density based on difficulty
            density_map = {
                "beginner": 0.24,
                "intermediate": 0.22,
                "expert": 0.20,
            }
            density = density_map.get(section.difficulty, 0.22)

            try:
                puzzle = generate_puzzle(
                    height=size,
                    width=size,
                    black_density=density,
                    max_attempts=20,
                )
                puzzles.append(puzzle)

                if (i + 1) % 10 == 0:
                    logger.info(f"  Generated {i + 1}/{section.count} puzzles")

            except Exception as e:
                logger.warning(f"Failed to generate puzzle {i + 1}: {e}")
                continue

        # Cache the puzzles
        cache_dir.mkdir(parents=True, exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump([p.to_dict() for p in puzzles], f)

        logger.info(f"Generated and cached {len(puzzles)} puzzles")
        return puzzles
