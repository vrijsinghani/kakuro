"""
Diagram data models for programmatic diagram generation.

These dataclasses define the structure for instructional diagrams
that are rendered directly using ReportLab drawing primitives.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class CellType(Enum):
    """Type of cell in a diagram grid."""

    WHITE = "white"  # Empty white cell (can have a value)
    BLACK = "black"  # Solid black cell
    CLUE = "clue"  # Clue cell with diagonal split


class HighlightStyle(Enum):
    """Highlight style for cells."""

    NONE = "none"
    CORRECT = "correct"  # Green highlight
    INCORRECT = "incorrect"  # Red highlight
    EMPHASIS = "emphasis"  # Yellow/gold highlight
    PRIMARY = "primary"  # Blue highlight
    SECONDARY = "secondary"  # Purple highlight


@dataclass
class DiagramCell:
    """A single cell in a diagram grid."""

    row: int
    col: int
    cell_type: CellType = CellType.WHITE
    value: Optional[str] = None  # Digit or text to display
    clue_across: Optional[int] = None  # Horizontal clue value
    clue_down: Optional[int] = None  # Vertical clue value
    highlight: HighlightStyle = HighlightStyle.NONE
    label: Optional[str] = None  # Small label (e.g., "A", "B")


@dataclass
class DiagramGrid:
    """A Kakuro-style grid for diagrams."""

    rows: int
    cols: int
    cells: list[DiagramCell] = field(default_factory=list)
    title: Optional[str] = None  # Title above grid
    caption: Optional[str] = None  # Caption below grid

    def get_cell(self, row: int, col: int) -> Optional[DiagramCell]:
        """Get cell at position, or None if not defined."""
        for cell in self.cells:
            if cell.row == row and cell.col == col:
                return cell
        return None


@dataclass
class Callout:
    """An annotation callout pointing to part of a diagram."""

    text: str
    target_row: int  # Grid row the callout points to
    target_col: int  # Grid col the callout points to
    position: str = "right"  # 'left', 'right', 'above', 'below'


@dataclass
class AnnotationBox:
    """A text box with optional styling for annotations."""

    text: str
    style: str = "info"  # 'info', 'warning', 'success', 'error'
    title: Optional[str] = None


@dataclass
class Legend:
    """A legend showing color/symbol meanings."""

    items: dict[str, str]  # color/symbol -> label mapping
    title: Optional[str] = None


@dataclass
class DiagramDefinition:
    """Complete definition of an instructional diagram."""

    diagram_id: str  # e.g., "chapter1_diagram1"
    title: str
    grids: list[DiagramGrid] = field(default_factory=list)
    callouts: list[Callout] = field(default_factory=list)
    annotations: list[AnnotationBox] = field(default_factory=list)
    legend: Optional[Legend] = None
    layout: str = "single"  # 'single', 'horizontal', 'vertical'
    caption: Optional[str] = None  # Overall caption for the diagram
    legend_position: str = "right"  # 'right', 'below'


# =============================================================================
# Reference Table Models (for non-puzzle diagrams like combination tables)
# =============================================================================


@dataclass
class CombinationCard:
    """A single combination card showing sum and digits."""

    sum_value: int
    combination: str  # e.g., "1 + 2"
    color: str = "blue"  # "blue" or "red"


@dataclass
class CombinationSection:
    """A section of combination cards with a header."""

    title: str
    cards: list[CombinationCard] = field(default_factory=list)
    columns: int = 2  # Number of cards per row


@dataclass
class ReferenceTableDefinition:
    """A reference table showing combinations or other non-grid content."""

    diagram_id: str
    title: str
    sections: list[CombinationSection] = field(default_factory=list)
    footer_note: Optional[str] = None
    border_color: str = "#4CAF50"  # Green border
    background_color: str = "#E8F5E9"  # Light green background


# =============================================================================
# Color Palettes and Styles
# =============================================================================

# Color palette for highlights
HIGHLIGHT_COLORS = {
    HighlightStyle.NONE: None,
    HighlightStyle.CORRECT: "#90EE90",  # Light green
    HighlightStyle.INCORRECT: "#FFB6C1",  # Light red/pink
    HighlightStyle.EMPHASIS: "#FFE4B5",  # Moccasin/light gold
    HighlightStyle.PRIMARY: "#ADD8E6",  # Light blue
    HighlightStyle.SECONDARY: "#DDA0DD",  # Plum/light purple
}

# Style colors for annotation boxes
ANNOTATION_STYLES = {
    "info": {"bg": "#E3F2FD", "border": "#2196F3", "text": "#1565C0"},
    "warning": {"bg": "#FFF3E0", "border": "#FF9800", "text": "#E65100"},
    "success": {"bg": "#E8F5E9", "border": "#4CAF50", "text": "#2E7D32"},
    "error": {"bg": "#FFEBEE", "border": "#F44336", "text": "#C62828"},
}

# Colors for combination cards
CARD_COLORS = {
    "blue": {"sum": "#1565C0", "combo": "#333333"},
    "red": {"sum": "#C62828", "combo": "#333333"},
    "green": {"sum": "#2E7D32", "combo": "#333333"},
}
