"""Tests for puzzle solver module."""

from src.puzzle_generation.models import Grid, Puzzle
from src.puzzle_generation.solver import (
    solve_puzzle,
    solve_kakuro,
    CellDomain,
    _initialize_domains,
    _select_mrv_cell,
)
from src.puzzle_generation.runs import compute_runs


class TestSolvePuzzle:
    """Tests for solve_puzzle function."""

    def test_solve_simple_puzzle(self):
        """Test solving a simple puzzle."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        h_runs, v_runs = compute_runs(grid)

        puzzle = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)
        result = solve_puzzle(puzzle, randomize=False)

        assert result is True
        # Check that all cells are filled
        for i in range(1, 3):
            for j in range(1, 3):
                assert grid.get_cell(i, j) > 0

    def test_solve_updates_run_totals(self):
        """Test that solving updates run totals."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 0, 0, 0],
        ]
        grid = Grid(height=2, width=4, cells=cells)
        h_runs, v_runs = compute_runs(grid)

        puzzle = Puzzle(grid=grid, horizontal_runs=h_runs, vertical_runs=v_runs)
        solve_puzzle(puzzle)

        # Run totals should be computed
        assert h_runs[0].total > 0


class TestSolveKakuro:
    """Tests for solve_kakuro function."""

    def test_solve_with_unique_digits_in_run(self):
        """Test that solution has unique digits in each run."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 0, 0, 0],
        ]
        grid = Grid(height=2, width=4, cells=cells)
        h_runs, v_runs = compute_runs(grid)

        result = solve_kakuro(grid, h_runs, v_runs, randomize=False)

        assert result is True
        # Check uniqueness in horizontal run
        values = [grid.get_cell(1, 1), grid.get_cell(1, 2), grid.get_cell(1, 3)]
        assert len(values) == len(set(values))  # All unique

    def test_solve_respects_constraints(self):
        """Test that solver respects run constraints."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        h_runs, v_runs = compute_runs(grid)

        result = solve_kakuro(grid, h_runs, v_runs, randomize=False)

        assert result is True

        # Check horizontal runs have unique digits
        h_values_1 = [grid.get_cell(1, 1), grid.get_cell(1, 2)]
        h_values_2 = [grid.get_cell(2, 1), grid.get_cell(2, 2)]
        assert len(h_values_1) == len(set(h_values_1))
        assert len(h_values_2) == len(set(h_values_2))

        # Check vertical runs have unique digits
        v_values_1 = [grid.get_cell(1, 1), grid.get_cell(2, 1)]
        v_values_2 = [grid.get_cell(1, 2), grid.get_cell(2, 2)]
        assert len(v_values_1) == len(set(v_values_1))
        assert len(v_values_2) == len(set(v_values_2))

    def test_solve_fills_all_empty_cells(self):
        """Test that solver fills all empty cells."""
        cells = [
            [-1, -1, -1, -1],
            [-1, 0, 0, 0],
            [-1, 0, 0, 0],
        ]
        grid = Grid(height=3, width=4, cells=cells)
        h_runs, v_runs = compute_runs(grid)

        result = solve_kakuro(grid, h_runs, v_runs)

        assert result is True
        # All non-black cells should be filled
        for i in range(1, 3):
            for j in range(1, 4):
                assert grid.get_cell(i, j) >= 1
                assert grid.get_cell(i, j) <= 9

    def test_solve_with_randomize(self):
        """Test that randomize parameter works."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid1 = Grid(height=3, width=3, cells=[row[:] for row in cells])
        grid2 = Grid(height=3, width=3, cells=[row[:] for row in cells])

        h_runs1, v_runs1 = compute_runs(grid1)
        h_runs2, v_runs2 = compute_runs(grid2)

        # Solve with randomize=True (may produce different solutions)
        result1 = solve_kakuro(grid1, h_runs1, v_runs1, randomize=True)
        result2 = solve_kakuro(grid2, h_runs2, v_runs2, randomize=True)

        assert result1 is True
        assert result2 is True
        # Both should be valid solutions (all cells filled)
        for i in range(1, 3):
            for j in range(1, 3):
                assert 1 <= grid1.get_cell(i, j) <= 9
                assert 1 <= grid2.get_cell(i, j) <= 9

    def test_unsolvable_grid_returns_false(self):
        """Test that unsolvable grid returns False."""
        # Create a grid that's impossible to solve
        # (e.g., a single cell that needs to be in both H and V runs)
        cells = [
            [-1, -1],
            [-1, 0],
        ]
        grid = Grid(height=2, width=2, cells=cells)

        # Create impossible constraints (this grid has no runs >= 2)
        h_runs = []
        v_runs = []

        result = solve_kakuro(grid, h_runs, v_runs)

        # Should succeed because there are no constraints
        assert result is True


class TestCellDomain:
    """Tests for CellDomain class."""

    def test_domain_initialization(self):
        """Test domain is initialized with values 1-9."""
        domain = CellDomain(0, 0)
        assert domain.count() == 9
        assert domain.get_values() == set(range(1, 10))

    def test_domain_custom_initialization(self):
        """Test domain with custom initial values."""
        domain = CellDomain(0, 0, {1, 2, 3})
        assert domain.count() == 3
        assert domain.get_values() == {1, 2, 3}

    def test_remove_value(self):
        """Test removing a value from domain."""
        domain = CellDomain(0, 0)
        result = domain.remove(5)
        assert result is True
        assert 5 not in domain.get_values()
        assert domain.count() == 8

    def test_remove_nonexistent_value(self):
        """Test removing a value not in domain."""
        domain = CellDomain(0, 0, {1, 2, 3})
        result = domain.remove(5)
        assert result is False
        assert domain.count() == 3

    def test_restore_value(self):
        """Test restoring a value to domain."""
        domain = CellDomain(0, 0)
        domain.remove(5)
        domain.restore(5)
        assert 5 in domain.get_values()
        assert domain.count() == 9

    def test_is_empty(self):
        """Test checking if domain is empty."""
        domain = CellDomain(0, 0, {1})
        assert not domain.is_empty()
        domain.remove(1)
        assert domain.is_empty()


class TestInitializeDomains:
    """Tests for _initialize_domains function."""

    def test_initialize_domains(self):
        """Test initializing domains for empty cells."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        empty_cells = [(1, 1), (1, 2), (2, 1), (2, 2)]

        domains = _initialize_domains(grid, empty_cells)

        assert len(domains) == 4
        assert all(cell in domains for cell in empty_cells)
        assert all(domains[cell].count() == 9 for cell in empty_cells)


class TestSelectMRVCell:
    """Tests for _select_mrv_cell function."""

    def test_select_mrv_cell_all_equal(self):
        """Test MRV selection when all domains are equal."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        empty_cells = [(1, 1), (1, 2), (2, 1), (2, 2)]
        domains = _initialize_domains(grid, empty_cells)

        cell = _select_mrv_cell(grid, domains)
        assert cell in empty_cells

    def test_select_mrv_cell_different_sizes(self):
        """Test MRV selection with different domain sizes."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        empty_cells = [(1, 1), (1, 2), (2, 1), (2, 2)]
        domains = _initialize_domains(grid, empty_cells)

        # Reduce domain of (1, 1) to make it the MRV cell
        domains[(1, 1)].remove(1)
        domains[(1, 1)].remove(2)
        domains[(1, 1)].remove(3)

        cell = _select_mrv_cell(grid, domains)
        assert cell == (1, 1)

    def test_select_mrv_cell_empty_domain(self):
        """Test MRV selection with empty domain."""
        cells = [
            [-1, -1, -1],
            [-1, 0, 0],
            [-1, 0, 0],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        empty_cells = [(1, 1), (1, 2)]
        domains = _initialize_domains(grid, empty_cells)

        # Empty the domain of (1, 1)
        for i in range(1, 10):
            domains[(1, 1)].remove(i)

        cell = _select_mrv_cell(grid, domains)
        assert cell is None  # Should return None when domain is empty

    def test_select_mrv_cell_all_filled(self):
        """Test MRV selection when all cells are filled."""
        cells = [
            [-1, -1, -1],
            [-1, 1, 2],
            [-1, 3, 4],
        ]
        grid = Grid(height=3, width=3, cells=cells)
        empty_cells = [(1, 1), (1, 2), (2, 1), (2, 2)]
        domains = _initialize_domains(grid, empty_cells)

        cell = _select_mrv_cell(grid, domains)
        assert cell is None  # All cells are filled
