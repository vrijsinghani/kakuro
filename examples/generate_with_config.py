"""
Example script demonstrating puzzle generation with configuration.

This script shows how to use the PuzzleConfig to generate puzzles
with different difficulty levels.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.puzzle_generation import generate_puzzle, get_config


def main():
    """Generate puzzles using configuration."""
    # Load configuration
    config = get_config()

    print("Kakuro Puzzle Generator - Configuration Demo")
    print("=" * 50)
    print()

    # Show default configuration
    print("Default Configuration:")
    print(f"  Grid size: {config.default_width}x{config.default_height}")
    print(f"  Black density: {config.default_black_density}")
    print(f"  Max attempts: {config.max_generation_attempts}")
    print()

    # Generate puzzles for each difficulty level
    difficulties = ["beginner", "intermediate", "expert", "master"]

    for difficulty in difficulties:
        print(f"\n{difficulty.upper()} Difficulty:")
        print("-" * 50)

        # Get difficulty configuration
        diff_config = config.get_difficulty_config(difficulty)
        width = diff_config["grid_size"]["width"]
        height = diff_config["grid_size"]["height"]
        density = diff_config["black_density"]

        print(f"  Grid: {width}x{height}")
        print(f"  Black density: {density}")
        print(f"  Description: {diff_config['description']}")

        # Generate puzzle with these settings
        print(f"  Generating puzzle...")
        puzzle = generate_puzzle(
            height=height, width=width, black_density=density, seed=42
        )

        print(f"  ✓ Generated successfully!")
        print(f"    - Horizontal runs: {len(puzzle.horizontal_runs)}")
        print(f"    - Vertical runs: {len(puzzle.vertical_runs)}")
        total_runs = len(puzzle.horizontal_runs) + len(puzzle.vertical_runs)
        print(f"    - Total runs: {total_runs}")

    print()
    print("=" * 50)
    print("✓ All difficulty levels generated successfully!")


if __name__ == "__main__":
    main()
