"""
BookDocument - High-level document builder for complete books.

This module provides the BookDocument class that orchestrates the
assembly of all book components into a complete PDF.
"""

import logging
from pathlib import Path
from typing import Optional

from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    PageBreak,
    ActionFlowable,
    SimpleDocTemplate,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from .config import BookConfig, PuzzleSectionConfig, DEFAULT_FONTS
from .chapter_renderer import ChapterRenderer
from .assembler import BookAssembler
from .puzzle_flowable import PuzzleFlowable, SolutionFlowable

logger = logging.getLogger(__name__)


class TOCEntry:
    """Entry in the table of contents."""

    def __init__(self, title: str, level: int = 0):
        """Initialize TOC entry with title and hierarchy level."""
        self.title = title
        self.level = level
        self.page_number: Optional[int] = None


class TOCNotifyFlowable(ActionFlowable):
    """Flowable that notifies TOC of a heading."""

    def __init__(self, title: str, level: int = 0):
        """Initialize TOC notification flowable."""
        ActionFlowable.__init__(self)
        self.title = title
        self.level = level

    def apply(self, doc):
        """Notify document when flowable is placed on a page."""
        # Notify the document about this heading
        doc.notify("TOCEntry", (self.level, self.title, doc.page))


class BookDocument:
    """High-level document builder for complete books.

    Provides a clean API for building book PDFs:
        doc = BookDocument(config, book_dir)
        doc.add_title_page()
        doc.add_copyright_page()
        doc.add_toc_placeholder()
        doc.add_chapter(path, title)
        doc.add_puzzle_section(section)
        doc.add_solutions()
        doc.add_about_author(path)
        doc.finalize_toc()
        doc.save(output_path)
    """

    def __init__(self, config: BookConfig, book_dir: Path):
        """Initialize the book document.

        Args:
            config: Book configuration.
            book_dir: Base directory of the book.
        """
        self.config = config
        self.book_dir = book_dir
        self.assembler = BookAssembler(config, book_dir)
        self.chapter_renderer = ChapterRenderer(config, book_dir)

        # Flowables to build
        self.flowables: list = []

        # TOC tracking
        self.toc_entries: list[TOCEntry] = []
        self._toc_placeholder_index: Optional[int] = None
        self._has_toc = False
        self._toc: Optional[TableOfContents] = None

        # Puzzle tracking for solutions
        self.all_puzzles: list[tuple] = []  # (puzzle_num, puzzle, difficulty_label)
        self._puzzle_num = 1

        # Page dimensions
        self.page_width = config.page_width_points
        self.page_height = config.page_height_points
        self.margins = config.layout.margins

        # Calculate content area
        self.content_width = (
            self.page_width - (self.margins.left + self.margins.right) * 72
        )
        self.content_height = (
            self.page_height - (self.margins.top + self.margins.bottom) * 72
        )

    def add_title_page(self) -> "BookDocument":
        """Add the title page."""
        self.flowables.extend(self.assembler.build_title_page())
        return self

    def add_copyright_page(self) -> "BookDocument":
        """Add the copyright page."""
        self.flowables.extend(self.assembler.build_copyright_page())
        return self

    def add_toc_placeholder(self) -> "BookDocument":
        """Add the table of contents.

        Uses ReportLab's TableOfContents which auto-populates with
        page numbers during the multi-pass build process.
        """
        self._has_toc = True
        self._toc_placeholder_index = len(self.flowables)

        # Add TOC header
        toc_header_style = ParagraphStyle(
            "TOCHeader",
            fontName=DEFAULT_FONTS["heading"],
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=30,
        )
        self.flowables.append(Paragraph("Table of Contents", toc_header_style))
        self.flowables.append(Spacer(1, 0.5 * inch))

        # Create TOC with custom styles
        self._toc = TableOfContents()
        self._toc.levelStyles = [
            # Level 0 - Main sections (chapters, puzzle sections)
            ParagraphStyle(
                "TOCLevel0",
                fontName=DEFAULT_FONTS["heading"],
                fontSize=14,
                leading=20,
                leftIndent=0,
                spaceBefore=8,
                spaceAfter=4,
            ),
            # Level 1 - Subsections
            ParagraphStyle(
                "TOCLevel1",
                fontName=DEFAULT_FONTS["body"],
                fontSize=12,
                leading=16,
                leftIndent=20,
                spaceBefore=2,
                spaceAfter=2,
            ),
        ]
        self.flowables.append(self._toc)
        self.flowables.append(PageBreak())
        return self

    def add_chapter(self, chapter_path: Path, title: str) -> "BookDocument":
        """Add a chapter from a markdown file.

        Args:
            chapter_path: Path to the markdown file (relative to book_dir).
            title: Chapter title for TOC.
        """
        full_path = self.book_dir / chapter_path
        if not full_path.exists():
            logger.warning(f"Chapter not found: {full_path}")
            return self

        # Add TOC notification flowable (tracks page number)
        if self._has_toc:
            self.flowables.append(TOCNotifyFlowable(title, level=1))

        # Track for internal reference
        self.toc_entries.append(TOCEntry(title, level=1))

        logger.info(f"Rendering chapter: {title}")
        chapter_flowables = self.chapter_renderer.render_chapter(full_path, title)
        self.flowables.extend(chapter_flowables)
        self.flowables.append(PageBreak())
        return self

    def add_section_header(self, title: str) -> "BookDocument":
        """Add a section header page.

        Args:
            title: Section title.
        """
        # Add TOC notification flowable (tracks page number)
        if self._has_toc:
            self.flowables.append(TOCNotifyFlowable(title, level=0))

        # Track for internal reference
        self.toc_entries.append(TOCEntry(title, level=0))
        self.flowables.extend(self.assembler.build_section_header(title))
        return self

    def add_puzzle_section(
        self, section: PuzzleSectionConfig, cache_dir: Optional[Path] = None
    ) -> "BookDocument":
        """Add a puzzle section with generated puzzles.

        Args:
            section: Puzzle section configuration.
            cache_dir: Directory for puzzle caching.
        """
        if cache_dir is None:
            cache_dir = self.book_dir / "output" / "puzzles"

        # Section header
        if section.title:
            self.add_section_header(section.title)

        # Generate puzzles
        puzzles = self.assembler.generate_puzzles_for_section(section, cache_dir)

        # Map difficulty to display name
        difficulty_labels = {
            "beginner": "Beginner",
            "intermediate": "Intermediate",
            "expert": "Expert",
        }
        difficulty_label = difficulty_labels.get(
            section.difficulty, section.difficulty.title()
        )

        # Add puzzles as flowables
        for puzzle in puzzles:
            pf = PuzzleFlowable(
                puzzle=puzzle,
                puzzle_number=self._puzzle_num,
                difficulty=difficulty_label,
                max_width=self.content_width,
                max_height=self.content_height,
                show_rules=True,
            )
            self.flowables.append(pf)
            self.flowables.append(PageBreak())

            self.all_puzzles.append((self._puzzle_num, puzzle, difficulty_label))
            self._puzzle_num += 1

        return self

    def add_solutions(self) -> "BookDocument":
        """Add the solutions section."""
        if not self.all_puzzles:
            logger.warning("No puzzles to generate solutions for")
            return self

        self.add_section_header("Solutions")

        from reportlab.platypus import Table

        solutions_per_row = 3
        solution_col_width = self.content_width / solutions_per_row
        solution_row_height = (self.content_height - 40) / 4

        for i in range(0, len(self.all_puzzles), solutions_per_row):
            row_puzzles = self.all_puzzles[i : i + solutions_per_row]
            row_flowables = []

            for num, puzzle, _ in row_puzzles:
                sf = SolutionFlowable(
                    puzzle=puzzle,
                    puzzle_number=num,
                    max_cell_size=14,
                    max_width=solution_col_width - 10,
                    max_height=solution_row_height - 10,
                )
                row_flowables.append(sf)

            # Pad row if needed
            while len(row_flowables) < solutions_per_row:
                row_flowables.append(Spacer(1, 1))

            table = Table(
                [row_flowables], colWidths=[solution_col_width] * solutions_per_row
            )
            self.flowables.append(table)
            self.flowables.append(Spacer(1, 10))

        return self

    def add_about_author(self, markdown_path: Optional[Path] = None) -> "BookDocument":
        """Add the about author page.

        Args:
            markdown_path: Optional path to markdown file with author info.
        """
        self.flowables.append(PageBreak())

        header_style = ParagraphStyle(
            "AboutHeader",
            fontName=DEFAULT_FONTS["heading"],
            fontSize=20,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=20,
        )

        body_style = ParagraphStyle(
            "AboutBody",
            fontName=DEFAULT_FONTS["body"],
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
        )

        self.flowables.append(Spacer(1, 2 * inch))
        self.flowables.append(Paragraph("About the Author", header_style))

        if markdown_path:
            full_path = self.book_dir / markdown_path
            if full_path.exists():
                about_flowables = self.chapter_renderer.render_chapter(
                    full_path, "About the Author"
                )
                self.flowables.extend(about_flowables)
            else:
                logger.warning(f"About author file not found: {full_path}")
                self.flowables.append(
                    Paragraph("[Author biography placeholder]", body_style)
                )
        else:
            author = self.config.metadata.author or "Anonymous"
            self.flowables.append(
                Paragraph(
                    f"{author} enjoys creating puzzle books that challenge "
                    f"and entertain solvers of all skill levels.",
                    body_style,
                )
            )

        self.flowables.append(PageBreak())
        return self

    def add_notes_pages(self, count: int = 4) -> "BookDocument":
        """Add blank notes/scratch pages.

        Args:
            count: Number of notes pages to add.
        """
        header_style = ParagraphStyle(
            "NotesHeader",
            fontName=DEFAULT_FONTS["heading"],
            fontSize=16,
            leading=22,
            alignment=TA_CENTER,
        )

        for i in range(count):
            self.flowables.append(Spacer(1, 0.5 * inch))
            self.flowables.append(Paragraph("Notes", header_style))
            self.flowables.append(Spacer(1, 0.5 * inch))
            # Ruled lines would go here in a more complex implementation
            self.flowables.append(PageBreak())

        return self

    def finalize_toc(self) -> "BookDocument":
        """Finalize the table of contents with page numbers.

        ReportLab's TableOfContents handles this automatically via
        multi-pass building (multiBuild).
        """
        # TableOfContents is automatically populated during multiBuild
        return self

    def save(self, output_path: Optional[Path] = None) -> Path:
        """Build and save the PDF.

        Args:
            output_path: Output path. Defaults to books/{book_id}/output/interior.pdf

        Returns:
            Path to the saved PDF.
        """
        if output_path is None:
            output_dir = self.book_dir / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "interior.pdf"

        if self._has_toc:
            # Use BaseDocTemplate with multiBuild for TOC support
            doc = self._create_multibuild_doc(output_path)
            doc.multiBuild(self.flowables)
        else:
            # Simple build without TOC
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=(self.page_width, self.page_height),
                leftMargin=self.margins.left * inch,
                rightMargin=self.margins.right * inch,
                topMargin=self.margins.top * inch,
                bottomMargin=self.margins.bottom * inch,
                title=self.config.metadata.title,
                author=self.config.metadata.author,
            )
            doc.build(
                self.flowables,
                onFirstPage=self._add_page_number,
                onLaterPages=self._add_page_number,
            )

        logger.info(f"Book saved to: {output_path}")
        return output_path

    def _create_multibuild_doc(self, output_path: Path) -> BaseDocTemplate:
        """Create a BaseDocTemplate configured for multi-pass TOC building."""
        doc = BaseDocTemplate(
            str(output_path),
            pagesize=(self.page_width, self.page_height),
            leftMargin=self.margins.left * inch,
            rightMargin=self.margins.right * inch,
            topMargin=self.margins.top * inch,
            bottomMargin=self.margins.bottom * inch,
            title=self.config.metadata.title,
            author=self.config.metadata.author,
        )

        # Create a frame for the content area
        frame = Frame(
            self.margins.left * inch,
            self.margins.bottom * inch,
            self.content_width,
            self.content_height,
            id="normal",
        )

        # Create page template with page number callback
        template = PageTemplate(
            id="main",
            frames=[frame],
            onPage=self._add_page_number_callback,
        )
        doc.addPageTemplates([template])

        # No afterFlowable hook needed as TOCNotifyFlowable handles it directly
        # doc.afterFlowable = afterFlowable

        return doc

    def _add_page_number(self, canvas, doc):
        """Add page number to bottom center of each page (for SimpleDocTemplate)."""
        page_num = canvas.getPageNumber()
        text = str(page_num)

        canvas.saveState()
        canvas.setFont(DEFAULT_FONTS["body"], 11)
        canvas.drawCentredString(self.page_width / 2, 0.5 * inch, text)
        canvas.restoreState()

    def _add_page_number_callback(self, canvas, doc):
        """Add page number callback for PageTemplate."""
        self._add_page_number(canvas, doc)
