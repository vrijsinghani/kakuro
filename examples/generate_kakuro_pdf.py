"""Example script demonstrating how to generate a Kakuro puzzle book PDF."""

from pathlib import Path
from src.puzzle_generation import generate_puzzle
from src.pdf_generation import (
    PDFDocument,
    BookConfig,
    PageLayout,
    LETTER,
)


def main():
    """Generate example Kakuro puzzle book PDF."""
    # 1. Setup output path
    output_path = Path("output/example_book.pdf")
    output_path.parent.mkdir(exist_ok=True)

    print(f"Generating puzzles...")
    # 2. Generate some sample puzzles
    # Using small sizes for speed in this example
    puzzles = [generate_puzzle(height=7, width=7, black_density=0.3) for _ in range(4)]

    # 3. Configure the book
    config = BookConfig(
        title="My First Kakuro Book",
        author="Kakuro Builder",
        include_solutions=True,
        layout=PageLayout(page_size=LETTER, puzzles_per_page=2),  # Standard layout
    )

    # 4. Create and save the document
    print(f"Creating PDF at {output_path}...")
    doc = PDFDocument(output_path, config)

    # Add puzzles as a batch
    doc.add_puzzles(puzzles)

    # Save (this also appends the solutions section if config.include_solutions is True)
    final_path = doc.save()

    print(f"✓ PDF successfully generated: {final_path}")


if __name__ == "__main__":
    main()
