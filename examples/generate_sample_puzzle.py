"""
Example script demonstrating puzzle generation.

This script generates a sample Kakuro puzzle and displays its properties.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.puzzle_generation import generate_puzzle


def main():
    """Generate and display a sample puzzle."""
    print("Generating a 9x9 Kakuro puzzle...")
    print()

    # Generate puzzle with fixed seed for reproducibility
    puzzle = generate_puzzle(height=9, width=9, seed=42)

    print(f"Grid size: {puzzle.grid.height}x{puzzle.grid.width}")
    print(f"Horizontal runs: {len(puzzle.horizontal_runs)}")
    print(f"Vertical runs: {len(puzzle.vertical_runs)}")
    print()

    # Display grid
    print("Grid (solved):")
    print("-" * 40)
    for i in range(puzzle.grid.height):
        row_str = ""
        for j in range(puzzle.grid.width):
            cell = puzzle.grid.get_cell(i, j)
            if cell == -1:
                row_str += " ■ "
            elif cell == 0:
                row_str += " . "
            else:
                row_str += f" {cell} "
        print(row_str)
    print("-" * 40)
    print()

    # Display some runs
    print("Sample horizontal runs:")
    for run in puzzle.horizontal_runs[:5]:
        print(f"  {run}")
    print()

    print("Sample vertical runs:")
    for run in puzzle.vertical_runs[:5]:
        print(f"  {run}")
    print()

    # Serialize to dict
    puzzle_dict = puzzle.to_dict()
    print(f"Puzzle can be serialized to dict with {len(puzzle_dict)} keys")
    print()

    print("✓ Puzzle generation successful!")


if __name__ == "__main__":
    main()
