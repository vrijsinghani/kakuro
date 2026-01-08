"""
Grid renderer for Kakuro puzzles.

This module handles the low-level rendering of Kakuro puzzle grids
to a ReportLab PDF canvas.
"""

from typing import Optional

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, white, Color

from src.puzzle_generation import Puzzle, CellType
from .models import RenderConfig


def render_grid(
    canvas: Canvas,
    puzzle: Puzzle,
    x: float,
    y: float,
    config: Optional[RenderConfig] = None,
) -> tuple[float, float]:
    """Render a Kakuro puzzle grid to a PDF canvas.

    Args:
        canvas: ReportLab canvas to draw on.
        puzzle: Puzzle to render.
        x: X position of grid's top-left corner.
        y: Y position of grid's top-left corner (from bottom of page).
        config: Rendering configuration. Uses defaults if not provided.

    Returns:
        Tuple of (grid_width, grid_height) in points.
    """
    config = config or RenderConfig()
    grid = puzzle.grid

    grid_width = grid.width * config.cell_size
    grid_height = grid.height * config.cell_size

    # Save canvas state
    canvas.saveState()

    # Set font
    canvas.setFont(config.font_name, config.clue_font_size)

    # Draw cells from top to bottom, left to right
    for row in range(grid.height):
        for col in range(grid.width):
            cell_x = x + col * config.cell_size
            # Y is from bottom, so we invert row order
            cell_y = y - (row + 1) * config.cell_size

            cell_value = grid.get_cell(row, col)

            if cell_value == CellType.BLACK.value:
                # Black cell - check if it's a clue cell
                h_clue = _get_horizontal_clue(puzzle, row, col)
                v_clue = _get_vertical_clue(puzzle, row, col)

                if h_clue is not None or v_clue is not None:
                    # It's a clue cell with at least one clue
                    _draw_clue_cell(canvas, cell_x, cell_y, h_clue, v_clue, config)
                else:
                    # Pure black cell (no clues)
                    _draw_black_cell(canvas, cell_x, cell_y, config)
            else:
                # White cell - optionally show solution
                solution_value = (
                    cell_value if config.show_solution and cell_value > 0 else None
                )
                _draw_white_cell(canvas, cell_x, cell_y, solution_value, config)

    # Draw outer border
    canvas.setStrokeColor(black)
    canvas.setLineWidth(config.thick_line_width)
    canvas.rect(x, y - grid_height, grid_width, grid_height, stroke=1, fill=0)

    # Restore canvas state
    canvas.restoreState()

    return grid_width, grid_height


def _draw_black_cell(
    canvas: Canvas,
    x: float,
    y: float,
    config: RenderConfig,
) -> None:
    """Draw a solid black cell."""
    canvas.setFillColor(black)
    canvas.setStrokeColor(black)
    canvas.setLineWidth(config.line_width)
    canvas.rect(x, y, config.cell_size, config.cell_size, stroke=1, fill=1)


def _draw_white_cell(
    canvas: Canvas,
    x: float,
    y: float,
    value: Optional[int],
    config: RenderConfig,
) -> None:
    """Draw a white cell, optionally with a solution digit."""
    canvas.setFillColor(white)
    canvas.setStrokeColor(black)
    canvas.setLineWidth(config.line_width)
    canvas.rect(x, y, config.cell_size, config.cell_size, stroke=1, fill=1)

    if value is not None and value > 0:
        canvas.setFillColor(black)
        canvas.setFont(config.font_name, config.solution_font_size)
        # Center the digit in the cell
        text = str(value)
        text_width = canvas.stringWidth(
            text, config.font_name, config.solution_font_size
        )
        text_x = x + (config.cell_size - text_width) / 2
        text_y = y + (config.cell_size - config.solution_font_size) / 2
        canvas.drawString(text_x, text_y, text)


def _draw_clue_cell(
    canvas: Canvas,
    x: float,
    y: float,
    h_clue: Optional[int],
    v_clue: Optional[int],
    config: RenderConfig,
) -> None:
    """Draw a clue cell with diagonal split and clue numbers.

    Based on the working prototype in docs/kakurov2.py:
    - Gray background (#D0D0D0) instead of black
    - Diagonal line from TOP-LEFT to BOTTOM-RIGHT
    - 'across' (horizontal) clue at 75% right, 25% up from bottom
      (bottom-right triangle)
    - 'down' (vertical) clue at 25% right, 75% up from bottom
      (top-left triangle)

    Note: ReportLab coordinate system has Y=0 at bottom of page.
    Cell (x, y) is the BOTTOM-LEFT corner of the cell.
    """
    cell_size = config.cell_size

    # Gray background like prototype (#D0D0D0 = 208/255 ≈ 0.816)
    gray = Color(0.816, 0.816, 0.816)
    canvas.setFillColor(gray)
    canvas.setStrokeColor(black)
    canvas.setLineWidth(config.line_width)
    canvas.rect(x, y, cell_size, cell_size, stroke=1, fill=1)

    # Draw diagonal line from top-left to bottom-right (black, like prototype)
    # In ReportLab coords: top-left = (x, y + cell_size),
    # bottom-right = (x + cell_size, y)
    canvas.setStrokeColor(black)
    canvas.setLineWidth(0.8)
    canvas.line(x, y + cell_size, x + cell_size, y)

    # Draw clue numbers in black (matching prototype)
    canvas.setFillColor(black)
    canvas.setFont(config.font_name, config.clue_font_size)

    # Horizontal clue ('across') - sum for run going RIGHT
    # Position at 75% across, 75% up (upper-right area, above diagonal)
    if h_clue is not None and h_clue > 0:
        text = str(h_clue)
        text_width = canvas.stringWidth(text, config.font_name, config.clue_font_size)
        text_x = x + cell_size * 0.75 - text_width / 2
        text_y = y + cell_size * 0.75 - config.clue_font_size / 2
        canvas.drawString(text_x, text_y, text)

    # Vertical clue ('down') - sum for run going DOWN
    # Position at 25% across, 25% up (lower-left area, below diagonal)
    if v_clue is not None and v_clue > 0:
        text = str(v_clue)
        text_width = canvas.stringWidth(text, config.font_name, config.clue_font_size)
        text_x = x + cell_size * 0.25 - text_width / 2
        text_y = y + cell_size * 0.25 - config.clue_font_size / 2
        canvas.drawString(text_x, text_y, text)


def _get_horizontal_clue(puzzle: Puzzle, row: int, col: int) -> Optional[int]:
    """Get the horizontal clue value for a cell (sum for run to the right).

    Args:
        puzzle: The puzzle containing runs.
        row: Row index.
        col: Column index.

    Returns:
        The clue value if this cell starts a horizontal run, None otherwise.
    """
    for run in puzzle.horizontal_runs:
        # Check if this cell is the clue position (one before the run starts)
        # Horizontal runs: clue is at (row, col-1) for run starting at (row, col)
        if run.row == row and run.col == col + 1:
            return run.total
    return None


def _get_vertical_clue(puzzle: Puzzle, row: int, col: int) -> Optional[int]:
    """Get the vertical clue value for a cell (sum for run below).

    Args:
        puzzle: The puzzle containing runs.
        row: Row index.
        col: Column index.

    Returns:
        The clue value if this cell starts a vertical run, None otherwise.
    """
    for run in puzzle.vertical_runs:
        # Check if this cell is the clue position (one above the run starts)
        # Vertical runs: clue is at (row-1, col) for run starting at (row, col)
        if run.col == col and run.row == row + 1:
            return run.total
    return None
