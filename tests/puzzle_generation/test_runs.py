"""Tests for run computation module."""

from src.puzzle_generation.models import Grid, Direction
from src.puzzle_generation.runs import (
    compute_runs,
    compute_horizontal_runs,
    compute_vertical_runs,
    compute_run_totals,
)


class TestComputeHorizontalRuns:
    """Tests for horizontal run computation."""

    def test_simple_horizontal_run(self):
        """Test detecting a simple horizontal run."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 0, 0, 0],
        ]
        grid = Grid(height=2, width=4, cells=cells)
        runs = compute_horizontal_runs(grid)

        assert len(runs) == 1
        assert runs[0].row == 1
        assert runs[0].col == 1
        assert runs[0].length == 3
        assert runs[0].direction == Direction.HORIZONTAL

    def test_multiple_horizontal_runs(self):
        """Test detecting multiple horizontal runs in same row."""
        cells = [
            [-1, -1, -1, -1, -1, -1],
            [-1, 0, 0, -1, 0, 0],
        ]
        grid = Grid(height=2, width=6, cells=cells)
        runs = compute_horizontal_runs(grid)

        assert len(runs) == 2
        assert runs[0].col == 1
        assert runs[0].length == 2
        assert runs[1].col == 4
        assert runs[1].length == 2

    def test_ignore_single_cell(self):
        """Test that single cells are not counted as runs."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 0, -1, 0],
        ]
        grid = Grid(height=2, width=4, cells=cells)
        runs = compute_horizontal_runs(grid)

        assert len(runs) == 0

    def test_no_horizontal_runs(self):
        """Test grid with no horizontal runs."""
        cells = [
            [-1, -1, -1],
            [-1, -1, -1],
        ]
        grid = Grid(height=2, width=3, cells=cells)
        runs = compute_horizontal_runs(grid)

        assert len(runs) == 0


class TestComputeVerticalRuns:
    """Tests for vertical run computation."""

    def test_simple_vertical_run(self):
        """Test detecting a simple vertical run."""
        cells = [
            [-1, -1],
            [-1, 0],
            [-1, 0],
            [-1, 0],
        ]
        grid = Grid(height=4, width=2, cells=cells)
        runs = compute_vertical_runs(grid)

        assert len(runs) == 1
        assert runs[0].row == 1
        assert runs[0].col == 1
        assert runs[0].length == 3
        assert runs[0].direction == Direction.VERTICAL

    def test_multiple_vertical_runs(self):
        """Test detecting multiple vertical runs in same column."""
        cells = [
            [-1, -1],
            [-1, 0],
            [-1, 0],
            [-1, -1],
            [-1, 0],
            [-1, 0],
        ]
        grid = Grid(height=6, width=2, cells=cells)
        runs = compute_vertical_runs(grid)

        assert len(runs) == 2
        assert runs[0].row == 1
        assert runs[0].length == 2
        assert runs[1].row == 4
        assert runs[1].length == 2

    def test_ignore_single_cell_vertical(self):
        """Test that single cells are not counted as runs."""
        cells = [
            [-1, -1],
            [-1, 0],
            [-1, -1],
            [-1, 0],
        ]
        grid = Grid(height=4, width=2, cells=cells)
        runs = compute_vertical_runs(grid)

        assert len(runs) == 0


class TestComputeRuns:
    """Tests for combined run computation."""

    def test_compute_both_runs(self, sample_grid_5x5):
        """Test computing both horizontal and vertical runs."""
        grid = Grid(height=5, width=5, cells=sample_grid_5x5)
        h_runs, v_runs = compute_runs(grid)

        assert len(h_runs) > 0
        assert len(v_runs) > 0

    def test_runs_have_zero_total_initially(self, sample_grid_5x5):
        """Test that runs start with total=0."""
        grid = Grid(height=5, width=5, cells=sample_grid_5x5)
        h_runs, v_runs = compute_runs(grid)

        for run in h_runs:
            assert run.total == 0
        for run in v_runs:
            assert run.total == 0


class TestComputeRunTotals:
    """Tests for computing run totals."""

    def test_compute_horizontal_total(self):
        """Test computing total for horizontal run."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 1, 2, 3],
        ]
        grid = Grid(height=2, width=4, cells=cells)
        h_runs = compute_horizontal_runs(grid)

        compute_run_totals(grid, h_runs, [])

        assert h_runs[0].total == 6  # 1 + 2 + 3

    def test_compute_vertical_total(self):
        """Test computing total for vertical run."""
        cells = [
            [-1, -1],
            [-1, 2],
            [-1, 4],
            [-1, 6],
        ]
        grid = Grid(height=4, width=2, cells=cells)
        v_runs = compute_vertical_runs(grid)

        compute_run_totals(grid, [], v_runs)

        assert v_runs[0].total == 12  # 2 + 4 + 6

    def test_compute_multiple_totals(self):
        """Test computing totals for multiple runs."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 1, 2, 3],
            [-1, 4, 5, 6],
        ]
        grid = Grid(height=3, width=4, cells=cells)
        h_runs = compute_horizontal_runs(grid)

        compute_run_totals(grid, h_runs, [])

        assert len(h_runs) == 2
        assert h_runs[0].total == 6  # 1 + 2 + 3
        assert h_runs[1].total == 15  # 4 + 5 + 6
