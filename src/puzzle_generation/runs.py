"""
Run computation for Kakuro puzzles.

This module handles the detection and computation of horizontal and vertical
runs in a Kakuro grid.
"""

import logging
from typing import List, Tuple

from .models import Grid, Run, Direction

logger = logging.getLogger(__name__)


def compute_runs(grid: Grid) -> Tuple[List[Run], List[Run]]:
    """
    Compute all horizontal and vertical runs in a grid.

    A run is a sequence of 2 or more consecutive non-black cells.

    Args:
        grid: The puzzle grid

    Returns:
        Tuple of (horizontal_runs, vertical_runs)

    Example:
        >>> grid = Grid(height=5, width=5, cells=[[...]])
        >>> h_runs, v_runs = compute_runs(grid)
        >>> len(h_runs)
        4
    """
    horizontal_runs = compute_horizontal_runs(grid)
    vertical_runs = compute_vertical_runs(grid)

    logger.debug(
        f"Computed {len(horizontal_runs)} horizontal and "
        f"{len(vertical_runs)} vertical runs"
    )

    return horizontal_runs, vertical_runs


def compute_horizontal_runs(grid: Grid) -> List[Run]:
    """
    Compute all horizontal runs in a grid.

    Scans each row from left to right, identifying sequences of
    consecutive non-black cells of length >= 2.

    Args:
        grid: The puzzle grid

    Returns:
        List of horizontal Run objects (total=0 initially)
    """
    runs = []

    for row in range(grid.height):
        col = 0
        while col < grid.width:
            if grid.is_black(row, col):
                # Found a black cell, check if there's a run after it
                start_col = col + 1
                length = 0

                # Count consecutive non-black cells
                while start_col + length < grid.width and not grid.is_black(
                    row, start_col + length
                ):
                    length += 1

                # Only create run if length >= 2
                if length >= 2:
                    run = Run(
                        row=row,
                        col=start_col,
                        length=length,
                        total=0,  # Will be computed after solving
                        direction=Direction.HORIZONTAL,
                    )
                    runs.append(run)
                    logger.debug(f"Found horizontal run: {run}")

                # Skip past this run
                col = start_col + length
            else:
                col += 1

    return runs


def compute_vertical_runs(grid: Grid) -> List[Run]:
    """
    Compute all vertical runs in a grid.

    Scans each column from top to bottom, identifying sequences of consecutive
    non-black cells of length >= 2.

    Args:
        grid: The puzzle grid

    Returns:
        List of vertical Run objects (total=0 initially)
    """
    runs = []

    for col in range(grid.width):
        row = 0
        while row < grid.height:
            if grid.is_black(row, col):
                # Found a black cell, check if there's a run after it
                start_row = row + 1
                length = 0

                # Count consecutive non-black cells
                while start_row + length < grid.height and not grid.is_black(
                    start_row + length, col
                ):
                    length += 1

                # Only create run if length >= 2
                if length >= 2:
                    run = Run(
                        row=start_row,
                        col=col,
                        length=length,
                        total=0,  # Will be computed after solving
                        direction=Direction.VERTICAL,
                    )
                    runs.append(run)
                    logger.debug(f"Found vertical run: {run}")

                # Skip past this run
                row = start_row + length
            else:
                row += 1

    return runs


def compute_run_totals(
    grid: Grid, horizontal_runs: List[Run], vertical_runs: List[Run]
) -> None:
    """
    Compute the sum totals for all runs based on filled grid values.

    This should be called after the grid has been solved to calculate
    the clue values for each run.

    Args:
        grid: The solved puzzle grid
        horizontal_runs: List of horizontal runs (modified in place)
        vertical_runs: List of vertical runs (modified in place)
    """
    for run in horizontal_runs:
        total = sum(grid.get_cell(run.row, run.col + i) for i in range(run.length))
        run.total = total
        logger.debug(f"Horizontal run at r{run.row}c{run.col}: total={total}")

    for run in vertical_runs:
        total = sum(grid.get_cell(run.row + i, run.col) for i in range(run.length))
        run.total = total
        logger.debug(f"Vertical run at r{run.row}c{run.col}: total={total}")
