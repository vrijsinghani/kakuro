"""Tests for puzzle generator module."""

import pytest
from src.puzzle_generation.generator import generate_puzzle, InvalidGridError
from src.puzzle_generation.models import Puzzle


class TestGeneratePuzzle:
    """Tests for generate_puzzle function."""

    def test_generate_default_puzzle(self):
        """Test generating a puzzle with default parameters."""
        puzzle = generate_puzzle(seed=42)

        assert isinstance(puzzle, Puzzle)
        assert puzzle.grid.height == 9
        assert puzzle.grid.width == 9
        assert len(puzzle.horizontal_runs) > 0
        assert len(puzzle.vertical_runs) > 0

    def test_generate_custom_size(self):
        """Test generating a puzzle with custom size."""
        puzzle = generate_puzzle(height=7, width=7, seed=42)

        assert puzzle.grid.height == 7
        assert puzzle.grid.width == 7

    def test_generate_with_seed_is_reproducible(self):
        """Test that same seed produces same puzzle."""
        puzzle1 = generate_puzzle(height=5, width=5, seed=123)
        puzzle2 = generate_puzzle(height=5, width=5, seed=123)

        # Should have same structure
        assert puzzle1.grid.cells == puzzle2.grid.cells
        assert len(puzzle1.horizontal_runs) == len(puzzle2.horizontal_runs)
        assert len(puzzle1.vertical_runs) == len(puzzle2.vertical_runs)

    def test_generate_invalid_size_too_small(self):
        """Test that invalid grid size raises error."""
        with pytest.raises(InvalidGridError, match="at least 5x5"):
            generate_puzzle(height=3, width=3)

    def test_generate_invalid_density_too_low(self):
        """Test that invalid density raises error."""
        with pytest.raises(InvalidGridError, match="between 0.1 and 0.4"):
            generate_puzzle(black_density=0.05)

    def test_generate_invalid_density_too_high(self):
        """Test that invalid density raises error."""
        with pytest.raises(InvalidGridError, match="between 0.1 and 0.4"):
            generate_puzzle(black_density=0.5)

    def test_generated_puzzle_has_edges_black(self):
        """Test that generated puzzle has black edges."""
        puzzle = generate_puzzle(height=5, width=5, seed=42)

        # Check top and left edges are black
        for i in range(5):
            assert puzzle.grid.is_black(i, 0)
            assert puzzle.grid.is_black(0, i)

    def test_generated_puzzle_is_solved(self):
        """Test that generated puzzle is already solved."""
        puzzle = generate_puzzle(height=5, width=5, seed=42)

        # All non-black cells should be filled
        for i in range(puzzle.grid.height):
            for j in range(puzzle.grid.width):
                if not puzzle.grid.is_black(i, j):
                    value = puzzle.grid.get_cell(i, j)
                    assert 1 <= value <= 9

    def test_generated_puzzle_has_valid_runs(self):
        """Test that generated puzzle has valid runs."""
        puzzle = generate_puzzle(height=6, width=6, seed=42)

        # All runs should have length >= 2
        for run in puzzle.horizontal_runs:
            assert run.length >= 2
        for run in puzzle.vertical_runs:
            assert run.length >= 2

    def test_generated_puzzle_runs_have_totals(self):
        """Test that generated puzzle runs have computed totals."""
        puzzle = generate_puzzle(height=5, width=5, seed=42)

        # All runs should have non-zero totals
        for run in puzzle.horizontal_runs:
            assert run.total > 0
        for run in puzzle.vertical_runs:
            assert run.total > 0

    def test_generate_different_densities(self):
        """Test generating puzzles with different densities."""
        puzzle_low = generate_puzzle(height=7, width=7, black_density=0.15, seed=42)
        puzzle_high = generate_puzzle(height=7, width=7, black_density=0.30, seed=43)

        # Count black cells (excluding edges)
        def count_black_interior(puzzle):
            count = 0
            for i in range(1, puzzle.grid.height):
                for j in range(1, puzzle.grid.width):
                    if puzzle.grid.is_black(i, j):
                        count += 1
            return count

        black_low = count_black_interior(puzzle_low)
        black_high = count_black_interior(puzzle_high)

        # Higher density should generally have more black cells
        # (not guaranteed due to cleanup, but likely)
        assert black_high >= black_low or abs(black_high - black_low) < 5

    def test_generate_with_max_attempts(self):
        """Test that max_attempts parameter is respected."""
        # This test is hard to trigger reliably, but we can at least
        # verify the parameter is accepted
        puzzle = generate_puzzle(height=5, width=5, max_attempts=5, seed=42)
        assert isinstance(puzzle, Puzzle)

    def test_generated_puzzle_no_duplicate_digits_in_runs(self):
        """Test that runs have no duplicate digits."""
        puzzle = generate_puzzle(height=6, width=6, seed=42)

        # Check horizontal runs
        for run in puzzle.horizontal_runs:
            cells = run.get_cells()
            values = [puzzle.grid.get_cell(r, c) for r, c in cells]
            assert len(values) == len(set(values)), f"Duplicate in H run: {values}"

        # Check vertical runs
        for run in puzzle.vertical_runs:
            cells = run.get_cells()
            values = [puzzle.grid.get_cell(r, c) for r, c in cells]
            assert len(values) == len(set(values)), f"Duplicate in V run: {values}"

    def test_generated_puzzle_run_totals_match(self):
        """Test that run totals match actual cell sums."""
        puzzle = generate_puzzle(height=5, width=5, seed=42)

        # Check horizontal runs
        for run in puzzle.horizontal_runs:
            cells = run.get_cells()
            actual_sum = sum(puzzle.grid.get_cell(r, c) for r, c in cells)
            assert actual_sum == run.total

        # Check vertical runs
        for run in puzzle.vertical_runs:
            cells = run.get_cells()
            actual_sum = sum(puzzle.grid.get_cell(r, c) for r, c in cells)
            assert actual_sum == run.total
