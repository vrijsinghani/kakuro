"""
Page builder for Kakuro puzzle PDFs.

This module handles the composition of puzzle pages, positioning
grids and adding page elements like puzzle numbers and titles.
"""

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black

from src.puzzle_generation import Puzzle
from .models import PageLayout, RenderConfig
from .renderer import render_grid


def build_puzzle_page(
    canvas: Canvas,
    puzzles: list[tuple[int, Puzzle]],
    layout: PageLayout,
) -> None:
    """Build a page with one or more puzzles.

    Args:
        canvas: ReportLab canvas to draw on.
        puzzles: List of (puzzle_number, puzzle) tuples to place on page.
        layout: Page layout configuration.
    """
    if len(puzzles) == 1:
        # Single puzzle - center on page
        puzzle_num, puzzle = puzzles[0]
        _draw_single_puzzle_page(canvas, puzzle_num, puzzle, layout)
    elif len(puzzles) == 2:
        # Two puzzles - one top, one bottom
        _draw_two_puzzle_page(canvas, puzzles[0], puzzles[1], layout)
    else:
        # For now, just draw the first two
        if puzzles:
            _draw_two_puzzle_page(
                canvas,
                puzzles[0],
                puzzles[1] if len(puzzles) > 1 else puzzles[0],
                layout,
            )


def _draw_single_puzzle_page(
    canvas: Canvas,
    puzzle_num: int,
    puzzle: Puzzle,
    layout: PageLayout,
) -> None:
    """Draw a single puzzle centered on the page."""
    config = layout.render_config
    page_width, page_height = layout.page_size

    # Calculate grid dimensions
    grid_width = puzzle.grid.width * config.cell_size

    # Center the grid
    x = (page_width - grid_width) / 2
    y = page_height - layout.margins.top - 30  # 30 points for puzzle number

    # Draw puzzle number
    _draw_puzzle_number(canvas, puzzle_num, x, y + 20, grid_width, config)

    # Draw the grid
    render_grid(canvas, puzzle, x, y, config)


def _draw_two_puzzle_page(
    canvas: Canvas,
    puzzle1: tuple[int, Puzzle],
    puzzle2: tuple[int, Puzzle],
    layout: PageLayout,
) -> None:
    """Draw two puzzles on a page, one above the other."""
    config = layout.render_config
    page_width, page_height = layout.page_size
    num1, puz1 = puzzle1
    num2, puz2 = puzzle2

    # Fixed spacing constants
    puzzle_number_height = 30  # Space for "Puzzle N" text
    gap_between_puzzles = 40  # Gap between puzzles

    # Calculate available content height
    content_height = layout.content_height

    # Calculate the maximum cell size that will fit both puzzles
    # Available height = content_height - 2 * puzzle_number_height - gap
    available_for_grids = (
        content_height - 2 * puzzle_number_height - gap_between_puzzles
    )

    # Each puzzle needs: grid_rows * cell_size
    # Total rows = puz1.grid.height + puz2.grid.height
    total_rows = puz1.grid.height + puz2.grid.height
    max_cell_size_for_height = available_for_grids / total_rows

    # Also check width constraint
    max_cols = max(puz1.grid.width, puz2.grid.width)
    max_cell_size_for_width = layout.content_width / max_cols

    # Use the smaller of the two constraints, but don't exceed original config
    cell_size = min(max_cell_size_for_height, max_cell_size_for_width, config.cell_size)

    # Create scaled config
    scale = cell_size / config.cell_size
    scaled_config = RenderConfig(
        cell_size=cell_size,
        line_width=config.line_width * scale,
        thick_line_width=config.thick_line_width * scale,
        clue_font_size=max(6.0, config.clue_font_size * scale),  # Min 6pt font
        solution_font_size=max(8.0, config.solution_font_size * scale),
        font_name=config.font_name,
        show_solution=config.show_solution,
    )

    # Calculate actual grid dimensions with scaled cell size
    grid_width1 = puz1.grid.width * cell_size
    grid_height1 = puz1.grid.height * cell_size
    grid_width2 = puz2.grid.width * cell_size

    # Position first puzzle at top
    y1 = page_height - layout.margins.top - puzzle_number_height
    x1 = (page_width - grid_width1) / 2

    # Draw first puzzle
    _draw_puzzle_number(canvas, num1, x1, y1 + 20, grid_width1, scaled_config)
    render_grid(canvas, puz1, x1, y1, scaled_config)

    # Position second puzzle below first with gap
    y2 = y1 - grid_height1 - gap_between_puzzles - puzzle_number_height
    x2 = (page_width - grid_width2) / 2

    # Draw second puzzle
    _draw_puzzle_number(canvas, num2, x2, y2 + 20, grid_width2, scaled_config)
    render_grid(canvas, puz2, x2, y2, scaled_config)


def _draw_puzzle_number(
    canvas: Canvas,
    number: int,
    x: float,
    y: float,
    grid_width: float,
    config: RenderConfig,
) -> None:
    """Draw the puzzle number above the grid."""
    canvas.saveState()
    canvas.setFillColor(black)
    canvas.setFont(config.font_name, 12)

    text = f"Puzzle {number}"
    text_width = canvas.stringWidth(text, config.font_name, 12)
    text_x = x + (grid_width - text_width) / 2

    canvas.drawString(text_x, y, text)
    canvas.restoreState()


def build_solution_page(
    canvas: Canvas,
    puzzles: list[tuple[int, Puzzle]],
    layout: PageLayout,
) -> None:
    """Build a solution page with solved puzzle grids.

    Args:
        canvas: ReportLab canvas to draw on.
        puzzles: List of (puzzle_number, puzzle) tuples.
        layout: Page layout configuration.
    """
    # Create a modified config with show_solution=True
    solution_config = RenderConfig(
        cell_size=layout.render_config.cell_size * 0.7,  # Smaller for solutions
        line_width=layout.render_config.line_width * 0.8,
        thick_line_width=layout.render_config.thick_line_width * 0.8,
        clue_font_size=layout.render_config.clue_font_size * 0.8,
        solution_font_size=layout.render_config.solution_font_size * 0.7,
        font_name=layout.render_config.font_name,
        show_solution=True,
    )

    solution_layout = PageLayout(
        page_size=layout.page_size,
        margins=layout.margins,
        puzzles_per_page=4,  # More solutions per page
        render_config=solution_config,
    )

    # For now, draw up to 4 solutions per page
    _draw_solution_grid(canvas, puzzles, solution_layout)


def _draw_solution_grid(
    canvas: Canvas,
    puzzles: list[tuple[int, Puzzle]],
    layout: PageLayout,
) -> None:
    """Draw solution grids in a 2x2 layout."""
    config = layout.render_config
    page_width, page_height = layout.page_size

    # Calculate positions for 2x2 grid of solutions
    margin = layout.margins.left

    # Grid cell positions (2 columns, 2 rows)
    positions = [
        (margin, page_height - layout.margins.top - 20),  # Top-left
        (page_width / 2 + 10, page_height - layout.margins.top - 20),  # Top-right
        (margin, page_height / 2),  # Bottom-left
        (page_width / 2 + 10, page_height / 2),  # Bottom-right
    ]

    for i, (num, puzzle) in enumerate(puzzles[:4]):
        if i >= len(positions):
            break

        x, y = positions[i]

        # Draw small puzzle number
        canvas.saveState()
        canvas.setFont(config.font_name, 10)
        canvas.drawString(x, y + 10, f"#{num}")
        canvas.restoreState()

        # Draw the solution grid
        render_grid(canvas, puzzle, x, y, config)
