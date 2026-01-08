"""Pytest fixtures for PDF generation tests."""

import pytest
from pathlib import Path
import tempfile

from src.puzzle_generation import generate_puzzle, Puzzle


@pytest.fixture
def sample_puzzle() -> Puzzle:
    """Generate a simple 7x7 beginner puzzle for testing."""
    return generate_puzzle(height=7, width=7, black_density=0.30)


@pytest.fixture
def solved_puzzle() -> Puzzle:
    """Generate a solved puzzle for testing solution rendering."""
    puzzle = generate_puzzle(height=7, width=7, black_density=0.30)
    # Puzzle comes back solved from generator
    return puzzle


@pytest.fixture
def sample_puzzles() -> list[Puzzle]:
    """Generate multiple puzzles for testing multi-puzzle pages."""
    return [generate_puzzle(height=7, width=7, black_density=0.30) for _ in range(4)]


@pytest.fixture
def temp_pdf_path():
    """Create a temporary file path for PDF output."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        yield Path(f.name)
    # Cleanup happens automatically when test exits


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    output = tmp_path / "pdf_output"
    output.mkdir()
    return output
