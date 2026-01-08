"""
Kakuro puzzle generator.

This module generates valid Kakuro puzzles with configurable dimensions
and difficulty levels.
"""

import logging
import random
from typing import Optional, Tuple

from .models import Grid, Puzzle, CellType
from .runs import compute_runs
from .solver import solve_kakuro

logger = logging.getLogger(__name__)


class PuzzleGenerationError(Exception):
    """Base exception for puzzle generation errors."""

    pass


class InvalidGridError(PuzzleGenerationError):
    """Raised when grid parameters are invalid."""

    pass


def generate_puzzle(
    height: int = 9,
    width: int = 9,
    black_density: float = 0.22,
    seed: Optional[int] = None,
    max_attempts: int = 10,
    max_run_length: int = 7,
) -> Puzzle:
    """
    Generate a valid Kakuro puzzle.

    Args:
        height: Grid height (minimum 5)
        width: Grid width (minimum 5)
        black_density: Proportion of black cells (0.15-0.30 recommended)
        seed: Random seed for reproducibility
        max_attempts: Maximum generation attempts before giving up
        max_run_length: Maximum allowed run length (default 7, prevents hard puzzles)

    Returns:
        A valid Puzzle object with unique solution

    Raises:
        InvalidGridError: If grid parameters are invalid
        PuzzleGenerationError: If generation fails after max_attempts

    Example:
        >>> puzzle = generate_puzzle(height=9, width=9, seed=42)
        >>> len(puzzle.horizontal_runs) > 0
        True
    """
    # Validate parameters
    if height < 5 or width < 5:
        raise InvalidGridError(f"Grid size must be at least 5x5, got {height}x{width}")

    if not 0.1 <= black_density <= 0.4:
        raise InvalidGridError(
            f"Black density must be between 0.1 and 0.4, got {black_density}"
        )

    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
        logger.info(f"Using random seed: {seed}")

    # Try to generate a valid puzzle
    for attempt in range(1, max_attempts + 1):
        logger.debug(f"Generation attempt {attempt}/{max_attempts}")

        try:
            grid, h_runs, v_runs = _generate_kakuro(
                height, width, black_density, max_run_length
            )

            puzzle = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)

            logger.info(
                f"Successfully generated {height}x{width} puzzle with "
                f"{len(h_runs)} horizontal and {len(v_runs)} vertical runs"
            )

            return puzzle

        except Exception as e:
            logger.debug(f"Attempt {attempt} failed: {e}")
            continue

    raise PuzzleGenerationError(
        f"Failed to generate puzzle after {max_attempts} attempts"
    )


def _generate_kakuro(
    height: int, width: int, black_density: float, max_run_length: int = 7
) -> Tuple[Grid, list, list]:
    """
    Generate a single Kakuro puzzle.

    Algorithm:
    1. Create grid with edges as black cells
    2. Randomly place black cells based on density
    3. Strategically add black cells to limit run lengths
    4. Clean up isolated cells
    5. Validate quality (no excessive consecutive black rows/columns)
    6. Compute runs and solve

    Args:
        height: Grid height
        width: Grid width
        black_density: Proportion of black cells
        max_run_length: Maximum allowed run length

    Returns:
        Tuple of (grid, horizontal_runs, vertical_runs)

    Raises:
        Exception: If puzzle generation fails or quality check fails
    """
    # Initialize grid
    cells = [[0] * width for _ in range(height)]

    # Set edges to black
    for i in range(height):
        cells[i][0] = CellType.BLACK.value
    for j in range(width):
        cells[0][j] = CellType.BLACK.value

    # Randomly place black cells
    for i in range(1, height):
        for j in range(1, width):
            if random.random() < black_density:
                cells[i][j] = CellType.BLACK.value

    grid = Grid(height=height, width=width, cells=cells)

    # Break up long runs by strategically placing additional black cells
    _limit_run_lengths(grid, max_run_length)

    # Clean up isolated cells (iterative process)
    _cleanup_grid(grid)

    # Remove any all-black rows or columns (compresses the grid)
    grid = _remove_all_black_lines(grid)

    # Compute runs
    h_runs, v_runs = compute_runs(grid)

    logger.debug(f"Found {len(h_runs)} horizontal and {len(v_runs)} vertical runs")

    # Solve the puzzle to validate and compute clues
    if not solve_kakuro(
        grid, h_runs, v_runs, randomize=True, use_csp=True, max_backtracks=500000
    ):
        raise Exception(
            "Generated grid is too difficult to solve (exceeded backtrack limit)"
        )

    return grid, h_runs, v_runs


def _remove_all_black_lines(grid: Grid) -> Grid:
    """
    Remove any interior rows or columns that are completely black.

    This compresses the grid but produces cleaner looking puzzles.
    The first row and first column (edges) are always kept.

    Args:
        grid: The grid to clean up

    Returns:
        A new Grid with all-black lines removed
    """
    # Find rows to keep (row 0 always kept, plus any row with at least one white cell)
    rows_to_keep = [0]  # Always keep edge
    for row in range(1, grid.height):
        has_white = any(not grid.is_black(row, col) for col in range(1, grid.width))
        if has_white:
            rows_to_keep.append(row)

    # Find columns to keep (col 0 always kept, plus any col with at least
    # one white cell)
    cols_to_keep = [0]  # Always keep edge
    for col in range(1, grid.width):
        has_white = any(not grid.is_black(row, col) for row in range(1, grid.height))
        if has_white:
            cols_to_keep.append(col)

    # If nothing was removed, return original grid
    if len(rows_to_keep) == grid.height and len(cols_to_keep) == grid.width:
        return grid

    # Build new compressed grid
    new_height = len(rows_to_keep)
    new_width = len(cols_to_keep)

    new_cells = []
    for new_row, old_row in enumerate(rows_to_keep):
        row_cells = []
        for new_col, old_col in enumerate(cols_to_keep):
            row_cells.append(grid.get_cell(old_row, old_col))
        new_cells.append(row_cells)

    logger.debug(
        f"Compressed grid from {grid.height}x{grid.width} to {new_height}x{new_width}"
    )

    return Grid(height=new_height, width=new_width, cells=new_cells)


def _limit_run_lengths(grid: Grid, max_run_length: int) -> None:
    """
    Break up runs that exceed the maximum length by placing black cells.

    This is crucial for making large grids solvable. Long runs create exponentially
    hard search spaces. For example, a 9-cell run has 9! = 362,880 possible digit
    arrangements before considering constraints.

    Args:
        grid: The grid to modify (modified in place)
        max_run_length: Maximum allowed run length (typically 6-7)
    """
    changed = True
    iterations = 0
    max_iterations = 20  # Prevent infinite loops

    while changed and iterations < max_iterations:
        changed = False
        iterations += 1

        # Check horizontal runs
        for row in range(1, grid.height):
            run_start = None
            run_length = 0

            for col in range(1, grid.width):
                if grid.is_black(row, col):
                    run_start = None
                    run_length = 0
                else:
                    if run_start is None:
                        run_start = col
                    run_length += 1

                    # If run exceeds max length, place a black cell to break it
                    if run_length > max_run_length:
                        # Place black cell at optimal position (middle-ish of run)
                        # This creates two shorter runs instead of one long one
                        break_col = run_start + max_run_length // 2
                        grid.set_cell(row, break_col, CellType.BLACK.value)
                        logger.debug(
                            f"Breaking long horizontal run at ({row}, {break_col})"
                        )
                        changed = True
                        run_start = None
                        run_length = 0

        # Check vertical runs
        for col in range(1, grid.width):
            run_start = None
            run_length = 0

            for row in range(1, grid.height):
                if grid.is_black(row, col):
                    run_start = None
                    run_length = 0
                else:
                    if run_start is None:
                        run_start = row
                    run_length += 1

                    # If run exceeds max length, place a black cell to break it
                    if run_length > max_run_length:
                        # Place black cell at optimal position
                        break_row = run_start + max_run_length // 2
                        grid.set_cell(break_row, col, CellType.BLACK.value)
                        logger.debug(
                            f"Breaking long vertical run at ({break_row}, {col})"
                        )
                        changed = True
                        run_start = None
                        run_length = 0

    if iterations >= max_iterations:
        logger.warning(f"_limit_run_lengths hit max iterations ({max_iterations})")
    else:
        logger.debug(f"Run lengths limited after {iterations} iteration(s)")


def _cleanup_grid(grid: Grid, max_iterations: int = 50) -> None:
    """
    Clean up the grid by removing isolated cells.

    A cell is isolated if it's not part of both a horizontal and vertical run.
    This iteratively converts such cells to black until the grid stabilizes.

    Args:
        grid: The grid to clean up (modified in place)
        max_iterations: Maximum cleanup iterations
    """
    for iteration in range(max_iterations):
        changed = False
        h_runs, v_runs = compute_runs(grid)

        for i in range(1, grid.height):
            for j in range(1, grid.width):
                if not grid.is_black(i, j):
                    # Check if cell is in both horizontal and vertical runs
                    in_h_run = _is_in_run(i, j, h_runs, horizontal=True)
                    in_v_run = _is_in_run(i, j, v_runs, horizontal=False)

                    if not (in_h_run and in_v_run):
                        grid.set_cell(i, j, CellType.BLACK.value)
                        changed = True

        if not changed:
            logger.debug(f"Grid stabilized after {iteration + 1} iterations")
            break


def _is_in_run(row: int, col: int, runs: list, horizontal: bool) -> bool:
    """
    Check if a cell is part of any run in the list.

    Args:
        row: Cell row
        col: Cell column
        runs: List of runs to check
        horizontal: True for horizontal runs, False for vertical

    Returns:
        True if cell is in a run
    """
    for run in runs:
        if horizontal:
            if run.row == row and run.col <= col < run.col + run.length:
                return True
        else:  # vertical
            if run.col == col and run.row <= row < run.row + run.length:
                return True

    return False
