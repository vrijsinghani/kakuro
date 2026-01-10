"""Tests for grid rendering components."""

import pytest
from unittest.mock import MagicMock

from reportlab.lib.colors import black, white
from src.pdf_generation.renderer import (
    render_grid,
    _draw_black_cell,
    _draw_white_cell,
    _draw_clue_cell,
    _get_horizontal_clue,
    _get_vertical_clue,
)
from src.pdf_generation.models import RenderConfig
from src.puzzle_generation import Puzzle, Grid, Run, Direction


class TestRenderer:
    """Tests for grid rendering components."""

    @pytest.fixture
    def mock_canvas(self):
        """Create mock canvas for testing."""
        return MagicMock()

    @pytest.fixture
    def simple_puzzle(self):
        """Create simple 2x2 test puzzle."""
        # 2x2 grid: (0,0) black, (0,1) clue, (1,0) white, (1,1) white
        cells = [[-1, -1], [0, 0]]
        grid = Grid(height=2, width=2, cells=cells)
        # Horizontal run starting at (1,1)
        h_run = Run(row=1, col=1, length=1, total=5, direction=Direction.HORIZONTAL)
        # Vertical run starting at (1,1)
        v_run = Run(row=1, col=1, length=1, total=3, direction=Direction.VERTICAL)
        return Puzzle(grid=grid, horizontal_runs=[h_run], vertical_runs=[v_run])

    def test_render_grid_dimensions(self, mock_canvas, simple_puzzle):
        """render_grid should return correct total dimensions."""
        config = RenderConfig(cell_size=20)
        width, height = render_grid(mock_canvas, simple_puzzle, 100, 500, config)
        assert width == 40  # 2 * 20
        assert height == 40  # 2 * 20
        assert mock_canvas.rect.called

    def test_draw_black_cell(self, mock_canvas):
        """_draw_black_cell should draw a filled black rectangle."""
        config = RenderConfig(cell_size=20)
        _draw_black_cell(mock_canvas, 10, 10, config)
        mock_canvas.rect.assert_called_with(10, 10, 20, 20, stroke=1, fill=1)
        mock_canvas.setFillColor.assert_called_with(black)

    def test_draw_white_cell_empty(self, mock_canvas):
        """_draw_white_cell should draw a filled white rectangle."""
        config = RenderConfig(cell_size=20)
        _draw_white_cell(mock_canvas, 10, 10, None, config)
        mock_canvas.rect.assert_called_with(10, 10, 20, 20, stroke=1, fill=1)
        mock_canvas.setFillColor.assert_any_call(white)

    def test_draw_white_cell_with_value(self, mock_canvas):
        """_draw_white_cell should draw a value if provided."""
        config = RenderConfig(cell_size=20, show_solution=True)
        _draw_white_cell(mock_canvas, 10, 10, 5, config)
        mock_canvas.drawString.assert_called()
        # Verify black color set for text
        mock_canvas.setFillColor.assert_any_call(black)

    def test_draw_clue_cell(self, mock_canvas):
        """_draw_clue_cell should draw a diagonal line and clue numbers."""
        config = RenderConfig(cell_size=20)
        _draw_clue_cell(mock_canvas, 10, 10, 5, 3, config)
        # Diagonal line
        mock_canvas.line.assert_called_with(10, 10 + 20, 10 + 20, 10)
        # Two clues
        assert mock_canvas.drawString.call_count == 2

    def test_get_horizontal_clue(self, simple_puzzle):
        """_get_horizontal_clue should find clue for cell to the left of a run."""
        # Run starts at (1,1). Clue should be at (1,0)
        clue = _get_horizontal_clue(simple_puzzle, 1, 0)
        assert clue == 5
        assert _get_horizontal_clue(simple_puzzle, 0, 0) is None

    def test_get_vertical_clue(self, simple_puzzle):
        """_get_vertical_clue should find clue for cell above a run."""
        # Run starts at (1,1). Clue should be at (0,1)
        clue = _get_vertical_clue(simple_puzzle, 0, 1)
        assert clue == 3
        assert _get_vertical_clue(simple_puzzle, 0, 0) is None
