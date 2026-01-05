"""Tests for puzzle generation data models."""

import pytest
from src.puzzle_generation.models import Grid, Run, Puzzle, Direction


class TestGrid:
    """Tests for Grid class."""

    def test_grid_creation(self):
        """Test creating a valid grid."""
        cells = [[0, 0], [0, 0]]
        grid = Grid(height=2, width=2, cells=cells)
        assert grid.height == 2
        assert grid.width == 2
        assert len(grid.cells) == 2

    def test_grid_validation_height_mismatch(self):
        """Test grid validation catches height mismatch."""
        cells = [[0, 0], [0, 0]]
        with pytest.raises(ValueError, match="height.*does not match"):
            Grid(height=3, width=2, cells=cells)

    def test_grid_validation_width_mismatch(self):
        """Test grid validation catches width mismatch."""
        cells = [[0, 0, 0], [0, 0]]
        with pytest.raises(ValueError, match="width.*does not match"):
            Grid(height=2, width=2, cells=cells)

    def test_get_cell(self):
        """Test getting cell values."""
        cells = [[1, 2], [3, 4]]
        grid = Grid(height=2, width=2, cells=cells)
        assert grid.get_cell(0, 0) == 1
        assert grid.get_cell(1, 1) == 4

    def test_set_cell(self):
        """Test setting cell values."""
        cells = [[0, 0], [0, 0]]
        grid = Grid(height=2, width=2, cells=cells)
        grid.set_cell(0, 1, 5)
        assert grid.get_cell(0, 1) == 5

    def test_is_black(self):
        """Test checking if cell is black."""
        cells = [[-1, 0], [0, -1]]
        grid = Grid(height=2, width=2, cells=cells)
        assert grid.is_black(0, 0) is True
        assert grid.is_black(0, 1) is False

    def test_is_empty(self):
        """Test checking if cell is empty."""
        cells = [[0, -1], [5, 0]]
        grid = Grid(height=2, width=2, cells=cells)
        assert grid.is_empty(0, 0) is True
        assert grid.is_empty(0, 1) is False
        assert grid.is_empty(1, 0) is False

    def test_grid_copy(self):
        """Test creating a deep copy of grid."""
        cells = [[1, 2], [3, 4]]
        grid = Grid(height=2, width=2, cells=cells)
        grid_copy = grid.copy()

        # Modify original
        grid.set_cell(0, 0, 99)

        # Copy should be unchanged
        assert grid_copy.get_cell(0, 0) == 1
        assert grid.get_cell(0, 0) == 99


class TestRun:
    """Tests for Run class."""

    def test_run_creation(self):
        """Test creating a run."""
        run = Run(row=1, col=2, length=3, total=15, direction=Direction.HORIZONTAL)
        assert run.row == 1
        assert run.col == 2
        assert run.length == 3
        assert run.total == 15
        assert run.direction == Direction.HORIZONTAL

    def test_get_cells_horizontal(self):
        """Test getting cells for horizontal run."""
        run = Run(row=2, col=3, length=4, total=20, direction=Direction.HORIZONTAL)
        cells = run.get_cells()
        assert cells == [(2, 3), (2, 4), (2, 5), (2, 6)]

    def test_get_cells_vertical(self):
        """Test getting cells for vertical run."""
        run = Run(row=1, col=5, length=3, total=12, direction=Direction.VERTICAL)
        cells = run.get_cells()
        assert cells == [(1, 5), (2, 5), (3, 5)]

    def test_run_str(self):
        """Test string representation of run."""
        run = Run(row=1, col=2, length=3, total=15, direction=Direction.HORIZONTAL)
        s = str(run)
        assert "H" in s
        assert "r1c2" in s
        assert "len=3" in s
        assert "sum=15" in s


class TestPuzzle:
    """Tests for Puzzle class."""

    def test_puzzle_creation(self):
        """Test creating a puzzle."""
        cells = [[-1, -1], [-1, 0]]
        grid = Grid(height=2, width=2, cells=cells)
        h_runs = [Run(1, 1, 1, 5, Direction.HORIZONTAL)]
        v_runs = []

        puzzle = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)
        assert puzzle.grid == grid
        assert len(puzzle.horizontal_runs) == 1
        assert len(puzzle.vertical_runs) == 0

    def test_puzzle_to_dict(self):
        """Test serializing puzzle to dictionary."""
        cells = [[-1, -1], [-1, 0]]
        grid = Grid(height=2, width=2, cells=cells)
        h_runs = [Run(1, 1, 1, 5, Direction.HORIZONTAL)]
        v_runs = [Run(0, 1, 1, 3, Direction.VERTICAL)]

        puzzle = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)
        data = puzzle.to_dict()

        assert data["grid"]["height"] == 2
        assert data["grid"]["width"] == 2
        assert len(data["horizontal_runs"]) == 1
        assert len(data["vertical_runs"]) == 1
        assert data["horizontal_runs"][0]["total"] == 5

    def test_puzzle_from_dict(self):
        """Test deserializing puzzle from dictionary."""
        data = {
            "grid": {"height": 2, "width": 2, "cells": [[-1, -1], [-1, 0]]},
            "horizontal_runs": [{"row": 1, "col": 1, "length": 1, "total": 5}],
            "vertical_runs": [{"row": 0, "col": 1, "length": 1, "total": 3}],
        }

        puzzle = Puzzle.from_dict(data)
        assert puzzle.grid.height == 2
        assert puzzle.grid.width == 2
        assert len(puzzle.horizontal_runs) == 1
        assert len(puzzle.vertical_runs) == 1
        assert puzzle.horizontal_runs[0].total == 5
        assert puzzle.horizontal_runs[0].direction == Direction.HORIZONTAL
        assert puzzle.vertical_runs[0].direction == Direction.VERTICAL

    def test_puzzle_round_trip(self):
        """Test serialization and deserialization round trip."""
        cells = [[-1, -1, -1], [-1, 1, 2], [-1, 3, 4]]
        grid = Grid(height=3, width=3, cells=cells)
        h_runs = [Run(1, 1, 2, 3, Direction.HORIZONTAL)]
        v_runs = [Run(1, 1, 2, 4, Direction.VERTICAL)]

        original = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)
        data = original.to_dict()
        restored = Puzzle.from_dict(data)

        assert restored.grid.height == original.grid.height
        assert restored.grid.cells == original.grid.cells
        assert len(restored.horizontal_runs) == len(original.horizontal_runs)
        assert restored.horizontal_runs[0].total == original.horizontal_runs[0].total
