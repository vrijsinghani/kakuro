"""Diagnostic script to analyze cached puzzles by chapter.

Shows grid sizes and distribution for each puzzle cache file.
"""

import json
from pathlib import Path
from collections import Counter

CACHE_DIR = Path("books/master-kakuro/output/puzzles")

# Map of cache files to chapter names based on book.yaml
CHAPTER_MAP = {
    "beginner_20_6.json": "Chapter 4: Warm-Up Puzzles (6x6)",
    "beginner_25_7.json": "Chapter 5: Building Skills (7x7)",
    "beginner_25_8.json": "Chapter 6: Beginner Mastery (8x8)",
    "intermediate_30_9.json": "Chapter 7: Stepping Up (9x9)",
    "intermediate_30_10.json": "Chapter 8: Intermediate Challenges (10x10)",
    "intermediate_30_11.json": "Chapter 9: Advanced Intermediate (11x11)",
    "expert_70_12_13_14.json": "Part 4: Expert Level (12x12, 13x13, 14x14)",
}


def analyze_cache_file(cache_file: Path) -> dict:
    """Analyze a single cache file and return grid size distribution."""
    with open(cache_file, "r") as f:
        puzzles = json.load(f)

    sizes = []
    for puzzle in puzzles:
        grid = puzzle.get("grid", {})
        height = grid.get("height", 0)
        width = grid.get("width", 0)
        sizes.append((height, width))

    return {
        "count": len(puzzles),
        "sizes": Counter(sizes),
    }


def main():
    """Analyze puzzle cache files and report grid size distribution."""
    print("=" * 70)
    print("PUZZLE CACHE ANALYSIS")
    print("=" * 70)

    if not CACHE_DIR.exists():
        print(f"ERROR: Cache directory not found: {CACHE_DIR}")
        return

    for cache_file in sorted(CACHE_DIR.glob("*.json")):
        chapter_name = CHAPTER_MAP.get(cache_file.name, f"Unknown: {cache_file.name}")

        print(f"\n{chapter_name}")
        print(f"  Cache file: {cache_file.name}")

        analysis = analyze_cache_file(cache_file)
        print(f"  Total puzzles: {analysis['count']}")
        print(f"  Grid sizes:")

        for (h, w), count in sorted(analysis["sizes"].items()):
            expected = (
                chapter_name.split("(")[-1].rstrip(")") if "(" in chapter_name else "?"
            )
            status = "✓" if f"{h}x{w}" in expected or "?" in expected else "✗ MISMATCH"
            print(f"    {h}x{w}: {count} puzzles {status}")

    print("\n" + "=" * 70)
    print("EXPECTED VS ACTUAL SUMMARY")
    print("=" * 70)

    # Check for issues
    issues = []
    for cache_file in sorted(CACHE_DIR.glob("*.json")):
        chapter_name = CHAPTER_MAP.get(cache_file.name, f"Unknown: {cache_file.name}")
        analysis = analyze_cache_file(cache_file)

        # Extract expected size from chapter name
        if "(" in chapter_name:
            expected_part = chapter_name.split("(")[-1].rstrip(")")

            for (h, w), count in analysis["sizes"].items():
                size_str = f"{h}x{w}"
                if size_str not in expected_part:
                    issues.append(
                        f"{chapter_name}: Found {count} puzzles with {size_str}"
                    )

    if issues:
        print("\n⚠️ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✓ All puzzles match expected grid sizes!")


if __name__ == "__main__":
    main()
