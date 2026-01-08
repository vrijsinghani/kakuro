"""
Data models for PDF generation.

This module defines the configuration dataclasses used throughout
the PDF generation process.
"""

from dataclasses import dataclass, field
from typing import Optional, NamedTuple

# Points per inch (ReportLab's native unit)
POINTS_PER_INCH = 72


class PageSize(NamedTuple):
    """Page dimensions in points."""

    width: float
    height: float


# Standard page sizes in points
LETTER = PageSize(8.5 * POINTS_PER_INCH, 11 * POINTS_PER_INCH)
A4 = PageSize(595.27, 841.89)  # Standard A4 in points
LARGE_FORMAT = PageSize(8.5 * POINTS_PER_INCH, 11 * POINTS_PER_INCH)
STANDARD = PageSize(8.0 * POINTS_PER_INCH, 10.0 * POINTS_PER_INCH)
COMPACT = PageSize(7.0 * POINTS_PER_INCH, 10.0 * POINTS_PER_INCH)


@dataclass(frozen=True)
class Margins:
    """Page margins in points.

    Attributes:
        top: Top margin
        bottom: Bottom margin
        left: Left margin
        right: Right margin
        gutter: Extra binding margin (added to left on odd pages, right on even)
    """

    top: float = 36.0  # 0.5 inch
    bottom: float = 36.0
    left: float = 36.0
    right: float = 36.0
    gutter: float = 9.0  # 0.125 inch

    @classmethod
    def from_inches(
        cls,
        top: float = 0.5,
        bottom: float = 0.5,
        left: float = 0.5,
        right: float = 0.5,
        gutter: float = 0.125,
    ) -> "Margins":
        """Create margins from inch measurements."""
        return cls(
            top=top * POINTS_PER_INCH,
            bottom=bottom * POINTS_PER_INCH,
            left=left * POINTS_PER_INCH,
            right=right * POINTS_PER_INCH,
            gutter=gutter * POINTS_PER_INCH,
        )


@dataclass(frozen=True)
class RenderConfig:
    """Configuration for rendering puzzle grids.

    Attributes:
        cell_size: Size of each grid cell in points
        line_width: Width of grid lines in points
        thick_line_width: Width of outer border in points
        clue_font_size: Font size for clue numbers
        solution_font_size: Font size for solution digits
        font_name: Name of font to use
        show_solution: Whether to display solution digits
    """

    cell_size: float = 43.2  # 0.6 inch in points
    line_width: float = 1.0
    thick_line_width: float = 2.0
    clue_font_size: float = 8.0
    solution_font_size: float = 14.0
    font_name: str = "Helvetica"
    show_solution: bool = False

    @classmethod
    def large_print(cls) -> "RenderConfig":
        """Create a large-print configuration."""
        return cls(
            cell_size=64.8,  # 0.9 inch
            line_width=1.5,
            thick_line_width=3.0,
            clue_font_size=12.0,
            solution_font_size=20.0,
        )


@dataclass
class PageLayout:
    """Page layout configuration.

    Attributes:
        page_size: Page dimensions (width, height) in points
        margins: Page margins
        puzzles_per_page: Number of puzzles per page (1 or 2)
        render_config: Grid rendering configuration
    """

    page_size: PageSize = field(default_factory=lambda: LETTER)
    margins: Margins = field(default_factory=Margins)
    puzzles_per_page: int = 2
    render_config: RenderConfig = field(default_factory=RenderConfig)

    @property
    def content_width(self) -> float:
        """Available width for content after margins."""
        return self.page_size.width - self.margins.left - self.margins.right

    @property
    def content_height(self) -> float:
        """Available height for content after margins."""
        return self.page_size.height - self.margins.top - self.margins.bottom

    @classmethod
    def standard(cls) -> "PageLayout":
        """Create standard layout (2 puzzles per page)."""
        return cls(puzzles_per_page=2)

    @classmethod
    def large_print(cls) -> "PageLayout":
        """Create large-print layout (1 puzzle per page, larger cells)."""
        return cls(
            puzzles_per_page=1,
            render_config=RenderConfig.large_print(),
        )


@dataclass
class BookConfig:
    """Configuration for generating a complete puzzle book.

    Attributes:
        title: Book title
        subtitle: Optional subtitle
        author: Author name
        layout: Page layout configuration
        include_instructions: Whether to include instruction pages
        include_solutions: Whether to include solution section
        puzzles_start_page: Page number for first puzzle
    """

    title: str = "Kakuro Puzzle Book"
    subtitle: Optional[str] = None
    author: str = ""
    layout: PageLayout = field(default_factory=PageLayout)
    include_instructions: bool = True
    include_solutions: bool = True
    puzzles_start_page: int = 1
