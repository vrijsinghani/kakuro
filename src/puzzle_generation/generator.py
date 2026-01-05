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
) -> Puzzle:
    """
    Generate a valid Kakuro puzzle.

    Args:
        height: Grid height (minimum 5)
        width: Grid width (minimum 5)
        black_density: Proportion of black cells (0.15-0.30 recommended)
        seed: Random seed for reproducibility
        max_attempts: Maximum generation attempts before giving up

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
            grid, h_runs, v_runs = _generate_kakuro(height, width, black_density)

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
    height: int, width: int, black_density: float
) -> Tuple[Grid, list, list]:
    """
    Generate a single Kakuro puzzle.

    This follows the algorithm from the original kakurov2.py:
    1. Create grid with edges as black cells
    2. Randomly place black cells based on density
    3. Clean up isolated cells
    4. Compute runs
    5. Solve the puzzle

    Args:
        height: Grid height
        width: Grid width
        black_density: Proportion of black cells

    Returns:
        Tuple of (grid, horizontal_runs, vertical_runs)

    Raises:
        Exception: If puzzle generation fails
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

    # Clean up isolated cells (iterative process)
    _cleanup_grid(grid)

    # Compute runs
    h_runs, v_runs = compute_runs(grid)

    logger.debug(f"Found {len(h_runs)} horizontal and {len(v_runs)} vertical runs")

    # Solve the puzzle to validate and compute clues
    if not solve_kakuro(grid, h_runs, v_runs, randomize=True):
        raise Exception("Generated grid is unsolvable")

    return grid, h_runs, v_runs


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
