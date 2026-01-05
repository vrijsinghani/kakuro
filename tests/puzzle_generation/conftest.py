"""Pytest configuration and fixtures for puzzle generation tests."""

import pytest
from typing import List


@pytest.fixture
def sample_grid_5x5() -> List[List[int]]:
    """Create a simple 5x5 grid for testing."""
    return [
        [-1, -1, -1, -1, -1],
        [-1, 0, 0, -1, 0],
        [-1, 0, 0, -1, 0],
        [-1, -1, -1, -1, 0],
        [-1, 0, 0, 0, 0],
    ]


@pytest.fixture
def sample_grid_9x9() -> List[List[int]]:
    """Create a 9x9 grid similar to the original kakurov2.py."""
    return [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, -1, 0, 0, 0, -1, 0],
        [-1, 0, 0, -1, 0, 0, 0, -1, 0],
        [-1, -1, -1, -1, -1, -1, 0, -1, 0],
        [-1, 0, 0, 0, -1, 0, 0, -1, 0],
        [-1, 0, 0, 0, -1, 0, 0, -1, 0],
        [-1, 0, 0, 0, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, 0, 0, 0],
        [-1, 0, 0, 0, -1, 0, 0, 0, 0],
    ]


@pytest.fixture
def solved_grid_simple() -> List[List[int]]:
    """Create a simple solved grid for validation testing."""
    return [
        [-1, -1, -1],
        [-1, 1, 2],
        [-1, 3, 4],
    ]
