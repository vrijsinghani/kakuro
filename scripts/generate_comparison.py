"""Generate comparison PDFs with and without compression.

This demonstrates the difference in grid appearance and size accuracy.
"""

import json
from pathlib import Path
import logging
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.puzzle_generation import generate_puzzle

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("books/master-kakuro/output/comparison")


def generate_comparison_set():
    """Generate puzzles with and without compression for comparison."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sizes = [(6, 6), (7, 7), (8, 8), (9, 9)]

    for height, width in sizes:
        logger.info(f"\n{'='*50}")
        logger.info(f"Generating {height}x{width} puzzles")
        logger.info(f"{'='*50}")

        # With compression (default behavior, strict enforcement)
        logger.info(f"\nWith compression (strict {height}x{width}+):")
        try:
            puzzle_compressed = generate_puzzle(
                height=height,
                width=width,
                black_density=0.22,
                max_attempts=50,  # More attempts for strict enforcement
                min_size=(height, width),  # Enforce exact minimum
                compress_grid=True,
            )
            logger.info(
                f"  Result: {puzzle_compressed.grid.height}x"
                f"{puzzle_compressed.grid.width}"
            )

            # Save to JSON
            with open(
                OUTPUT_DIR / f"puzzle_{height}x{width}_compressed.json", "w"
            ) as f:
                json.dump(puzzle_compressed.to_dict(), f, indent=2)

        except Exception as e:
            logger.error(f"  Failed: {e}")

        # Without compression (exact dimensions)
        logger.info(f"\nWithout compression (exact {height}x{width}):")
        try:
            puzzle_uncompressed = generate_puzzle(
                height=height,
                width=width,
                black_density=0.22,
                max_attempts=50,
                compress_grid=False,  # No compression
            )
            logger.info(
                f"  Result: {puzzle_uncompressed.grid.height}x"
                f"{puzzle_uncompressed.grid.width}"
            )

            # Save to JSON
            with open(
                OUTPUT_DIR / f"puzzle_{height}x{width}_uncompressed.json", "w"
            ) as f:
                json.dump(puzzle_uncompressed.to_dict(), f, indent=2)

        except Exception as e:
            logger.error(f"  Failed: {e}")

    logger.info(f"\nComparison puzzles saved to: {OUTPUT_DIR}")


def analyze_comparison():
    """Analyze and display the generated puzzles."""
    logger.info("\n" + "=" * 60)
    logger.info("COMPARISON ANALYSIS")
    logger.info("=" * 60)

    for json_file in sorted(OUTPUT_DIR.glob("*.json")):
        with open(json_file, "r") as f:
            data = json.load(f)

        grid = data["grid"]
        height = grid["height"]
        width = grid["width"]

        is_compressed = "compressed" in json_file.name
        expected = json_file.name.split("_")[1]  # e.g., "6x6"

        mode = "COMPRESSED" if is_compressed else "UNCOMPRESSED"
        logger.info(f"\n{json_file.name}:")
        logger.info(f"  Mode: {mode}")
        logger.info(f"  Expected: {expected}")
        logger.info(f"  Actual: {height}x{width}")
        logger.info(f"  Match: {'✓' if f'{height}x{width}' == expected else '✗'}")


if __name__ == "__main__":
    generate_comparison_set()
    analyze_comparison()
