"""
Kakuro puzzle solver using constraint satisfaction and backtracking.

This module implements a backtracking algorithm to solve Kakuro puzzles
by filling empty cells with digits 1-9 while satisfying all constraints.
"""

import logging
import random
from typing import List, Tuple, Set, Dict, Optional

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


class CellDomain:
    """
    Tracks the valid domain (possible values) for a cell in the puzzle.

    This class is used for constraint satisfaction problem (CSP) solving
    with forward checking and constraint propagation.
    """

    def __init__(self, row: int, col: int, initial_values: Set[int] = None):
        """
        Initialize a cell domain.

        Args:
            row: Row index of the cell
            col: Column index of the cell
            initial_values: Initial set of valid values (default: {1-9})
        """
        self.row = row
        self.col = col
        self.values: Set[int] = (
            initial_values if initial_values is not None else set(range(1, 10))
        )

    def remove(self, value: int) -> bool:
        """
        Remove a value from the domain.

        Args:
            value: Value to remove

        Returns:
            True if value was removed, False if not in domain
        """
        if value in self.values:
            self.values.remove(value)
            return True
        return False

    def restore(self, value: int) -> None:
        """
        Restore a value to the domain.

        Args:
            value: Value to restore
        """
        self.values.add(value)

    def get_values(self) -> Set[int]:
        """
        Get the set of valid values.

        Returns:
            Set of valid values
        """
        return self.values.copy()

    def count(self) -> int:
        """
        Count the number of remaining valid values.

        Returns:
            Number of valid values in domain
        """
        return len(self.values)

    def is_empty(self) -> bool:
        """
        Check if domain is empty (no valid values).

        Returns:
            True if domain is empty
        """
        return len(self.values) == 0

    def __repr__(self) -> str:
        """Return string representation of domain."""
        return f"CellDomain({self.row}, {self.col}, {sorted(self.values)})"


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
    use_csp: bool = True,
) -> bool:
    """
    Solve a Kakuro grid using backtracking algorithm with CSP heuristics.

    This is the core solving algorithm that fills empty cells with digits 1-9
    while ensuring no duplicates within runs. Uses MRV, forward checking,
    and constraint propagation for improved performance.

    Args:
        grid: The puzzle grid (modified in place)
        horizontal_runs: List of horizontal runs
        vertical_runs: List of vertical runs
        randomize: Whether to randomize digit order for variety
        use_csp: Whether to use CSP heuristics (MRV, forward checking)

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

    if use_csp:
        # Initialize domains for CSP solving
        domains = _initialize_domains(grid, empty_cells)
        logger.debug("Using CSP heuristics (MRV + forward checking)")

        # Solve using CSP-enhanced backtracking
        if _backtrack_csp(grid, domains, horizontal_runs, vertical_runs, randomize):
            compute_run_totals(grid, horizontal_runs, vertical_runs)
            logger.info("Puzzle solved successfully with CSP")
            return True
    else:
        # Solve using basic backtracking (legacy)
        if _backtrack(grid, empty_cells, 0, horizontal_runs, vertical_runs, randomize):
            compute_run_totals(grid, horizontal_runs, vertical_runs)
            logger.info("Puzzle solved successfully")
            return True

    logger.warning("No solution found")
    return False


def _initialize_domains(
    grid: Grid, empty_cells: List[Tuple[int, int]]
) -> Dict[Tuple[int, int], CellDomain]:
    """
    Initialize domains for all empty cells.

    Args:
        grid: The puzzle grid
        empty_cells: List of empty cell coordinates

    Returns:
        Dictionary mapping (row, col) to CellDomain
    """
    domains = {}
    for row, col in empty_cells:
        domains[(row, col)] = CellDomain(row, col)
    return domains


def _select_mrv_cell(
    grid: Grid, domains: Dict[Tuple[int, int], CellDomain]
) -> Optional[Tuple[int, int]]:
    """
    Select the cell with Minimum Remaining Values (MRV heuristic).

    This heuristic chooses the empty cell with the fewest valid values,
    which tends to fail faster and reduce the search space.

    Args:
        grid: The puzzle grid
        domains: Dictionary of cell domains

    Returns:
        (row, col) of cell with minimum remaining values, or None if all filled
    """
    min_count = float("inf")
    best_cell = None

    for (row, col), domain in domains.items():
        if grid.is_empty(row, col):
            count = domain.count()
            if count == 0:
                # Domain is empty - this path is unsolvable
                return None
            if count < min_count:
                min_count = count
                best_cell = (row, col)

    return best_cell


def _backtrack_csp(
    grid: Grid,
    domains: Dict[Tuple[int, int], CellDomain],
    h_runs: List[Run],
    v_runs: List[Run],
    randomize: bool,
) -> bool:
    """
    CSP-enhanced backtracking with MRV and forward checking.

    Args:
        grid: The puzzle grid
        domains: Dictionary of cell domains
        h_runs: Horizontal runs
        v_runs: Vertical runs
        randomize: Whether to randomize digit order

    Returns:
        True if solution found from this state
    """
    # Select cell using MRV heuristic
    cell = _select_mrv_cell(grid, domains)

    # Base case: all cells filled
    if cell is None:
        # Check if all cells are actually filled
        all_filled = all(not grid.is_empty(row, col) for (row, col) in domains.keys())
        return all_filled

    row, col = cell
    domain = domains[(row, col)]

    # Try each value in the domain
    values = list(domain.get_values())
    if randomize:
        random.shuffle(values)

    for digit in values:
        if _is_valid_placement(grid, row, col, digit, h_runs, v_runs):
            # Place digit
            grid.set_cell(row, col, digit)

            # Forward checking: update domains of affected cells
            removed_values = _forward_check(
                grid, row, col, digit, domains, h_runs, v_runs
            )

            # Check if forward checking created empty domains
            if removed_values is not None:
                # Recurse
                if _backtrack_csp(grid, domains, h_runs, v_runs, randomize):
                    return True

                # Backtrack: restore domains
                _restore_domains(domains, removed_values)

            # Backtrack: remove digit
            grid.set_cell(row, col, 0)

    return False


def _forward_check(
    grid: Grid,
    row: int,
    col: int,
    digit: int,
    domains: Dict[Tuple[int, int], CellDomain],
    h_runs: List[Run],
    v_runs: List[Run],
) -> Optional[List[Tuple[Tuple[int, int], int]]]:
    """
    Perform forward checking after placing a digit.

    Removes the placed digit from domains of all cells in the same runs.
    Returns the list of removed values for backtracking, or None if any
    domain becomes empty.

    Args:
        grid: The puzzle grid
        row: Row of placed digit
        col: Column of placed digit
        digit: The digit that was placed
        domains: Dictionary of cell domains
        h_runs: Horizontal runs
        v_runs: Vertical runs

    Returns:
        List of ((row, col), value) tuples that were removed, or None if
        forward checking fails (empty domain created)
    """
    removed = []

    # Get cells in same horizontal run
    h_cells = _get_run_cells_for_position(row, col, h_runs, Direction.HORIZONTAL)
    for r, c in h_cells:
        if (r, c) != (row, col) and (r, c) in domains and grid.is_empty(r, c):
            if domains[(r, c)].remove(digit):
                removed.append(((r, c), digit))
                # Check if domain became empty
                if domains[(r, c)].is_empty():
                    # Restore what we removed and return None
                    _restore_domains(domains, removed)
                    return None

    # Get cells in same vertical run
    v_cells = _get_run_cells_for_position(row, col, v_runs, Direction.VERTICAL)
    for r, c in v_cells:
        if (r, c) != (row, col) and (r, c) in domains and grid.is_empty(r, c):
            if domains[(r, c)].remove(digit):
                removed.append(((r, c), digit))
                # Check if domain became empty
                if domains[(r, c)].is_empty():
                    # Restore what we removed and return None
                    _restore_domains(domains, removed)
                    return None

    return removed


def _restore_domains(
    domains: Dict[Tuple[int, int], CellDomain],
    removed_values: List[Tuple[Tuple[int, int], int]],
) -> None:
    """
    Restore domain values that were removed during forward checking.

    Args:
        domains: Dictionary of cell domains
        removed_values: List of ((row, col), value) tuples to restore
    """
    for (row, col), value in removed_values:
        if (row, col) in domains:
            domains[(row, col)].restore(value)


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
