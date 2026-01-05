"""
Kakuro Puzzle Generation Module.

This module provides functionality for generating valid Kakuro puzzles with
configurable dimensions and difficulty levels.

Main exports:
    - generate_puzzle: Generate a complete Kakuro puzzle
    - solve_puzzle: Solve a given Kakuro puzzle
    - Grid: Grid data structure
    - Run: Run data structure
    - Puzzle: Complete puzzle data structure
"""

from .models import Grid, Run, Puzzle, Direction, CellType
from .generator import generate_puzzle, PuzzleGenerationError, InvalidGridError
from .solver import solve_puzzle, SolverError, UnsolvableError, SolverTimeoutError
from .config import PuzzleConfig, get_config

__all__ = [
    "generate_puzzle",
    "solve_puzzle",
    "Grid",
    "Run",
    "Puzzle",
    "Direction",
    "CellType",
    "PuzzleConfig",
    "get_config",
    "PuzzleGenerationError",
    "InvalidGridError",
    "SolverError",
    "UnsolvableError",
    "SolverTimeoutError",
]

__version__ = "0.1.0"
