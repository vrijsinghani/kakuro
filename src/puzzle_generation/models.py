"""
Data models for Kakuro puzzle generation.

This module defines the core data structures used throughout the puzzle
generation system.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any


class CellType(Enum):
    """Type of cell in a Kakuro grid."""

    BLACK = -1  # Black cell (clue cell or filler)
    EMPTY = 0  # Empty cell to be filled
    FILLED = 1  # Cell with a value (1-9)


class Direction(Enum):
    """Direction of a run in a Kakuro puzzle."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class Grid:
    """
    Represents a Kakuro puzzle grid.

    Attributes:
        height: Number of rows in the grid
        width: Number of columns in the grid
        cells: 2D list where -1=black, 0=empty, 1-9=filled

    Example:
        >>> grid = Grid(height=5, width=5, cells=[[...]])
        >>> grid.get_cell(1, 1)
        0
    """

    height: int
    width: int
    cells: List[List[int]]

    def __post_init__(self):
        """Validate grid dimensions match cells array."""
        if len(self.cells) != self.height:
            raise ValueError(
                f"Grid height {self.height} does not match cells rows {len(self.cells)}"
            )
        for i, row in enumerate(self.cells):
            if len(row) != self.width:
                raise ValueError(
                    f"Grid width {self.width} does not match row {i} length {len(row)}"
                )

    def get_cell(self, row: int, col: int) -> int:
        """Get the value of a cell at the given position."""
        return self.cells[row][col]

    def set_cell(self, row: int, col: int, value: int) -> None:
        """Set the value of a cell at the given position."""
        self.cells[row][col] = value

    def is_black(self, row: int, col: int) -> bool:
        """Check if a cell is a black cell."""
        return self.cells[row][col] == CellType.BLACK.value

    def is_empty(self, row: int, col: int) -> bool:
        """Check if a cell is empty."""
        return self.cells[row][col] == CellType.EMPTY.value

    def copy(self) -> "Grid":
        """Create a deep copy of the grid."""
        cells_copy = [row[:] for row in self.cells]
        return Grid(height=self.height, width=self.width, cells=cells_copy)


@dataclass
class Run:
    """
    Represents a horizontal or vertical run in a Kakuro puzzle.

    A run is a sequence of consecutive white cells that must be filled
    with unique digits summing to a specific total.

    Attributes:
        row: Starting row index
        col: Starting column index
        length: Number of cells in the run
        total: Sum that the run must equal (clue value)
        direction: HORIZONTAL or VERTICAL

    Example:
        >>> run = Run(row=1, col=2, length=3, total=15, direction=Direction.HORIZONTAL)
        >>> run.get_cells()
        [(1, 2), (1, 3), (1, 4)]
    """

    row: int
    col: int
    length: int
    total: int
    direction: Direction

    def get_cells(self) -> List[tuple[int, int]]:
        """
        Get (row, col) coordinates for all cells in this run.

        Returns:
            List of (row, col) tuples
        """
        if self.direction == Direction.HORIZONTAL:
            return [(self.row, self.col + i) for i in range(self.length)]
        else:  # VERTICAL
            return [(self.row + i, self.col) for i in range(self.length)]

    def __str__(self) -> str:
        """Return string representation of the run."""
        dir_str = "H" if self.direction == Direction.HORIZONTAL else "V"
        return (
            f"Run({dir_str}, r{self.row}c{self.col}, "
            f"len={self.length}, sum={self.total})"
        )


@dataclass
class Puzzle:
    """
    Represents a complete Kakuro puzzle.

    Attributes:
        grid: The puzzle grid
        horizontal_runs: List of horizontal runs
        vertical_runs: List of vertical runs

    Example:
        >>> puzzle = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)
        >>> puzzle.to_dict()
        {...}
    """

    grid: Grid
    horizontal_runs: List[Run] = field(default_factory=list)
    vertical_runs: List[Run] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize puzzle to dictionary format.

        Returns:
            Dictionary representation of the puzzle
        """
        return {
            "grid": {
                "height": self.grid.height,
                "width": self.grid.width,
                "cells": self.grid.cells,
            },
            "horizontal_runs": [
                {
                    "row": run.row,
                    "col": run.col,
                    "length": run.length,
                    "total": run.total,
                }
                for run in self.horizontal_runs
            ],
            "vertical_runs": [
                {
                    "row": run.row,
                    "col": run.col,
                    "length": run.length,
                    "total": run.total,
                }
                for run in self.vertical_runs
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Puzzle":
        """
        Deserialize puzzle from dictionary format.

        Args:
            data: Dictionary representation of the puzzle

        Returns:
            Puzzle object
        """
        grid_data = data["grid"]
        grid = Grid(
            height=grid_data["height"],
            width=grid_data["width"],
            cells=grid_data["cells"],
        )

        horizontal_runs = [
            Run(
                row=run["row"],
                col=run["col"],
                length=run["length"],
                total=run["total"],
                direction=Direction.HORIZONTAL,
            )
            for run in data["horizontal_runs"]
        ]

        vertical_runs = [
            Run(
                row=run["row"],
                col=run["col"],
                length=run["length"],
                total=run["total"],
                direction=Direction.VERTICAL,
            )
            for run in data["vertical_runs"]
        ]

        return cls(
            grid=grid, horizontal_runs=horizontal_runs, vertical_runs=vertical_runs
        )
