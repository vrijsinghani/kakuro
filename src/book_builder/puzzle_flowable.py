"""
Puzzle flowable - wraps puzzle rendering for use in Platypus documents.

This module provides a Flowable wrapper around puzzle grid rendering,
allowing puzzles to be included in Platypus document flow.
"""

from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor

from src.puzzle_generation import Puzzle
from src.pdf_generation.renderer import render_grid
from src.pdf_generation.models import RenderConfig

# The four basic Kakuro rules
KAKURO_RULES = [
    "Fill each white cell with a digit from 1 to 9.",
    "Each horizontal or vertical run must sum to its clue number.",
    "No digit may repeat within any single run.",
    "Use logic—no guessing required!",
]


class PuzzleFlowable(Flowable):
    """A Flowable that renders a Kakuro puzzle grid with rules and header."""

    def __init__(
        self,
        puzzle: Puzzle,
        puzzle_number: int,
        difficulty: str = "Beginner",
        cell_size: float = 36,
        show_solution: bool = False,
        max_width: float = None,
        max_height: float = None,
        show_rules: bool = True,
    ):
        """Initialize puzzle flowable.

        Args:
            puzzle: Puzzle to render.
            puzzle_number: Puzzle number for labeling.
            difficulty: Difficulty level for header.
            cell_size: Cell size in points.
            show_solution: Whether to show the solution.
            max_width: Maximum width in points.
            max_height: Maximum height in points.
            show_rules: Whether to show the rules at top.
        """
        super().__init__()
        self.puzzle = puzzle
        self.puzzle_number = puzzle_number
        self.difficulty = difficulty
        self.cell_size = cell_size
        self.show_solution = show_solution
        self.max_width = max_width
        self.max_height = max_height
        self.show_rules = show_rules

        # Layout constants
        self.header_height = 30
        self.rules_height = 80 if show_rules else 0
        self.grid_top_margin = 20

    def _calculate_dimensions(self, available_width, available_height):
        """Calculate the flowable and grid dimensions."""
        grid = self.puzzle.grid

        # Calculate available space for the grid
        grid_available_height = (
            available_height
            - self.header_height
            - self.rules_height
            - self.grid_top_margin
            - 20
        )
        grid_available_width = available_width

        # Calculate cell size to maximize grid size while fitting
        cell_size_by_width = grid_available_width / grid.width
        cell_size_by_height = grid_available_height / grid.height

        # Use the smaller to ensure it fits, but cap at a reasonable maximum
        self.actual_cell_size = min(cell_size_by_width, cell_size_by_height, 50)

        # Calculate actual grid dimensions
        self.grid_width = grid.width * self.actual_cell_size
        self.grid_height = grid.height * self.actual_cell_size

        # Total flowable dimensions
        self.width = available_width
        self.height = (
            self.header_height
            + self.rules_height
            + self.grid_top_margin
            + self.grid_height
            + 20
        )

    def wrap(self, available_width, available_height):
        """Return the dimensions of the flowable."""
        self._calculate_dimensions(available_width, available_height)
        return self.width, self.height

    def draw(self):
        """Draw the puzzle page content."""
        canvas = self.canv
        y_cursor = self.height

        # Draw header: "Level - Puzzle N - Grid Size"
        y_cursor -= self.header_height
        self._draw_header(canvas, y_cursor)

        # Draw rules
        if self.show_rules:
            y_cursor -= self.rules_height
            self._draw_rules(canvas, y_cursor)

        # Draw puzzle grid (centered)
        y_cursor -= self.grid_top_margin
        grid_x = (self.width - self.grid_width) / 2

        # Create render config
        scale = self.actual_cell_size / 36.0
        config = RenderConfig(
            cell_size=self.actual_cell_size,
            line_width=1.0 * scale,
            thick_line_width=2.0 * scale,
            clue_font_size=max(7.0, 11.0 * scale),
            solution_font_size=max(10.0, 16.0 * scale),
            font_name="Helvetica",
            show_solution=self.show_solution,
        )

        # Draw the grid
        render_grid(canvas, self.puzzle, grid_x, y_cursor, config)

    def _draw_header(self, canvas, y):
        """Draw the header with level, puzzle number, and grid size."""
        canvas.saveState()

        # Header text: "Beginner - Puzzle 1 - 6×6"
        grid = self.puzzle.grid
        header = (
            f"{self.difficulty} – Puzzle {self.puzzle_number} – "
            f"{grid.width}×{grid.height}"
        )

        canvas.setFont("Helvetica-Bold", 16)
        text_width = canvas.stringWidth(header, "Helvetica-Bold", 16)
        x = (self.width - text_width) / 2
        canvas.drawString(x, y + 8, header)

        canvas.restoreState()

    def _draw_rules(self, canvas, y):
        """Draw the four basic rules as bullet points."""
        canvas.saveState()

        # Rules box styling - larger font for better readability
        rule_font_size = 12
        line_height = 18
        left_margin = 40
        bullet = "•"

        canvas.setFont("Helvetica", rule_font_size)
        canvas.setFillColor(HexColor("#333333"))

        y_pos = y + self.rules_height - 12

        for rule in KAKURO_RULES:
            canvas.drawString(left_margin, y_pos, f"{bullet}  {rule}")
            y_pos -= line_height

        canvas.restoreState()


class SolutionFlowable(Flowable):
    """A smaller flowable for solution grids with dynamic sizing."""

    def __init__(
        self,
        puzzle: Puzzle,
        puzzle_number: int,
        max_cell_size: float = 14,
        max_width: float = None,
        max_height: float = None,
    ):
        """Initialize solution flowable.

        Args:
            puzzle: Puzzle to render.
            puzzle_number: Puzzle number for labeling.
            max_cell_size: Maximum cell size in points.
            max_width: Maximum width for this solution grid.
            max_height: Maximum height for this solution grid.
        """
        super().__init__()
        self.puzzle = puzzle
        self.puzzle_number = puzzle_number
        self.max_cell_size = max_cell_size
        self.max_width = max_width
        self.max_height = max_height
        self.label_height = 16

        # Will be calculated in wrap()
        self.actual_cell_size = max_cell_size
        self.width = 0
        self.height = 0

    def wrap(self, available_width, available_height):
        """Calculate dimensions based on available space."""
        grid = self.puzzle.grid

        # Use provided max or available space
        max_w = self.max_width or available_width
        max_h = self.max_height or available_height

        # Calculate cell size to fit within constraints
        cell_by_width = max_w / grid.width
        cell_by_height = (max_h - self.label_height) / grid.height

        # Use smallest constraint, capped at max_cell_size
        self.actual_cell_size = min(cell_by_width, cell_by_height, self.max_cell_size)

        # Calculate actual dimensions
        self.width = grid.width * self.actual_cell_size
        self.height = grid.height * self.actual_cell_size + self.label_height

        return self.width, self.height

    def draw(self):
        """Draw the solution on the canvas."""
        canvas = self.canv

        # Scale line widths and fonts based on cell size
        scale = self.actual_cell_size / 14.0

        config = RenderConfig(
            cell_size=self.actual_cell_size,
            line_width=max(0.3, 0.5 * scale),
            thick_line_width=max(0.5, 1.0 * scale),
            clue_font_size=max(4.0, 6.0 * scale),
            solution_font_size=max(5.0, 8.0 * scale),
            font_name="Helvetica",
            show_solution=True,
        )

        # Draw puzzle number
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(0, self.height - 12, f"#{self.puzzle_number}")
        canvas.restoreState()

        # Draw the grid
        grid_height = self.puzzle.grid.height * self.actual_cell_size
        render_grid(canvas, self.puzzle, 0, grid_height, config)
