"""
Kakuro puzzle solver using constraint satisfaction and backtracking.

This module implements a backtracking algorithm to solve Kakuro puzzles
by filling empty cells with digits 1-9 while satisfying all constraints.
"""

import logging
import random
from typing import List, Tuple

from .models import Grid, Run, Puzzle, Direction
from .runs import compute_run_totals

logger = logging.getLogger(__name__)


class SolverError(Exception):
    """Base exception for solver errors."""

    pass


class UnsolvableError(SolverError):
    """Raised when a puzzle has no valid solution."""

    pass


class SolverTimeoutError(SolverError):
    """Raised when solver exceeds time limit."""

    pass


def solve_puzzle(puzzle: Puzzle, randomize: bool = True) -> bool:
    """
    Solve a Kakuro puzzle using backtracking.

    Args:
        puzzle: The puzzle to solve (modified in place)
        randomize: Whether to randomize digit order (for generation)

    Returns:
        True if solved successfully, False otherwise

    Raises:
        UnsolvableError: If puzzle has no valid solution
    """
    return solve_kakuro(
        puzzle.grid,
        puzzle.horizontal_runs,
        puzzle.vertical_runs,
        randomize=randomize,
    )


def solve_kakuro(
    grid: Grid,
    horizontal_runs: List[Run],
    vertical_runs: List[Run],
    randomize: bool = True,
) -> bool:
    """
    Solve a Kakuro grid using backtracking algorithm.

    This is the core solving algorithm that fills empty cells with digits 1-9
    while ensuring no duplicates within runs.

    Args:
        grid: The puzzle grid (modified in place)
        horizontal_runs: List of horizontal runs
        vertical_runs: List of vertical runs
        randomize: Whether to randomize digit order for variety

    Returns:
        True if solution found, False otherwise
    """
    # Find all empty cells
    empty_cells = [
        (i, j)
        for i in range(grid.height)
        for j in range(grid.width)
        if grid.is_empty(i, j)
    ]

    logger.debug(f"Solving puzzle with {len(empty_cells)} empty cells")

    # Solve using backtracking
    if _backtrack(grid, empty_cells, 0, horizontal_runs, vertical_runs, randomize):
        # Compute run totals after solving
        compute_run_totals(grid, horizontal_runs, vertical_runs)
        logger.info("Puzzle solved successfully")
        return True

    logger.warning("No solution found")
    return False


def _backtrack(
    grid: Grid,
    cells: List[Tuple[int, int]],
    index: int,
    h_runs: List[Run],
    v_runs: List[Run],
    randomize: bool,
) -> bool:
    """
    Recursive backtracking function.

    Args:
        grid: The puzzle grid
        cells: List of empty cell coordinates
        index: Current cell index
        h_runs: Horizontal runs
        v_runs: Vertical runs
        randomize: Whether to randomize digit order

    Returns:
        True if solution found from this state
    """
    # Base case: all cells filled
    if index == len(cells):
        return True

    row, col = cells[index]

    # Try digits 1-9 in random or sequential order
    digits = list(range(1, 10))
    if randomize:
        random.shuffle(digits)

    for digit in digits:
        if _is_valid_placement(grid, row, col, digit, h_runs, v_runs):
            # Place digit
            grid.set_cell(row, col, digit)

            # Recurse
            if _backtrack(grid, cells, index + 1, h_runs, v_runs, randomize):
                return True

            # Backtrack
            grid.set_cell(row, col, 0)

    return False


def _is_valid_placement(
    grid: Grid,
    row: int,
    col: int,
    digit: int,
    h_runs: List[Run],
    v_runs: List[Run],
) -> bool:
    """
    Check if placing a digit at (row, col) is valid.

    A placement is valid if the digit doesn't already exist in the same
    horizontal or vertical run.

    Args:
        grid: The puzzle grid
        row: Row index
        col: Column index
        digit: Digit to place (1-9)
        h_runs: Horizontal runs
        v_runs: Vertical runs

    Returns:
        True if placement is valid
    """
    # Check horizontal run
    h_cells = _get_run_cells_for_position(row, col, h_runs, Direction.HORIZONTAL)
    for r, c in h_cells:
        if (r, c) != (row, col) and grid.get_cell(r, c) == digit:
            return False

    # Check vertical run
    v_cells = _get_run_cells_for_position(row, col, v_runs, Direction.VERTICAL)
    for r, c in v_cells:
        if (r, c) != (row, col) and grid.get_cell(r, c) == digit:
            return False

    return True


def _get_run_cells_for_position(
    row: int, col: int, runs: List[Run], direction: Direction
) -> List[Tuple[int, int]]:
    """
    Get all cells in the run that contains the given position.

    Args:
        row: Row index
        col: Column index
        runs: List of runs to search
        direction: Direction of runs to check

    Returns:
        List of (row, col) tuples in the run, or empty list if not in a run
    """
    for run in runs:
        if direction == Direction.HORIZONTAL:
            if run.row == row and run.col <= col < run.col + run.length:
                return run.get_cells()
        else:  # VERTICAL
            if run.col == col and run.row <= row < run.row + run.length:
                return run.get_cells()

    return []
