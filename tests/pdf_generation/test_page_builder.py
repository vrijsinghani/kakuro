"""Tests for page building and layout composition."""

import pytest
from unittest.mock import MagicMock, patch

from src.pdf_generation.page_builder import (
    build_puzzle_page,
    build_solution_page,
    _draw_puzzle_number,
)
from src.pdf_generation.models import PageLayout, RenderConfig


class TestPageBuilder:
    """Tests for page building and layout composition."""

    @pytest.fixture
    def mock_canvas(self):
        """Create mock canvas for testing."""
        m = MagicMock()
        m.stringWidth.return_value = 50
        return m

    @patch("src.pdf_generation.page_builder.render_grid")
    def test_build_puzzle_page_single(self, mock_render, mock_canvas, sample_puzzle):
        """Test building a page with a single puzzle."""
        """build_puzzle_page with one puzzle should call single puzzle draw."""
        layout = PageLayout()
        build_puzzle_page(mock_canvas, [(1, sample_puzzle)], layout)

        # Should call render_grid once
        mock_render.assert_called_once()
        # Verify puzzle number was drawn
        mock_canvas.drawString.assert_called()

    @patch("src.pdf_generation.page_builder.render_grid")
    def test_build_puzzle_page_two(self, mock_render, mock_canvas, sample_puzzle):
        """build_puzzle_page with two puzzles should call two puzzle draw."""
        layout = PageLayout()
        build_puzzle_page(mock_canvas, [(1, sample_puzzle), (2, sample_puzzle)], layout)

        # Should call render_grid twice
        assert mock_render.call_count == 2

    def test_draw_puzzle_number(self, mock_canvas):
        """_draw_puzzle_number should center text above the grid."""
        config = RenderConfig()
        _draw_puzzle_number(mock_canvas, 42, 100, 500, 200, config)

        # Verify call to stringWidth to center
        mock_canvas.stringWidth.assert_called_with("Puzzle 42", config.font_name, 12)
        mock_canvas.drawString.assert_called()

    @patch("src.pdf_generation.page_builder.render_grid")
    def test_build_solution_page(self, mock_render, mock_canvas, sample_puzzle):
        """build_solution_page should render grids with show_solution=True."""
        layout = PageLayout()
        build_solution_page(mock_canvas, [(1, sample_puzzle)], layout)

        mock_render.assert_called_once()
        # Extract the config used in the call
        args, kwargs = mock_render.call_args
        config = args[4]
        assert config.show_solution is True
