"""
Validate PDF/X Compliance.

This script generates a dummy PDF using the PDFDocument class and inspects
its metadata to verify that PDF/X compliance flags are set correctly.
"""

import sys
from pathlib import Path

from src.pdf_generation.document import PDFDocument
from src.puzzle_generation import Puzzle
from src.puzzle_generation.models import Grid


def create_dummy_puzzle():
    """Create a simple dummy puzzle for testing."""
    grid = Grid(10, 10, [[0] * 10 for _ in range(10)])
    puzzle = Puzzle(grid=grid, horizontal_runs=[], vertical_runs=[])
    return puzzle


def check_metadata(pdf_path):
    """Check if the PDF has the correct metadata."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        metadata = reader.metadata

        print(f"Metadata: {metadata}")

        required_keys = {
            "/Title": "Kakuro Puzzle Book",
            "/Producer": "ReportLab PDF Library",
            "/Creator": "Kakuro Book Builder",
            "/Trapped": "/False",
        }

        missing = []
        for key, value in required_keys.items():
            if key not in metadata or metadata[key] != value:
                missing.append(f"{key}: expected '{value}', got '{metadata.get(key)}'")

        if missing:
            print("❌ Validation Failed:")
            for m in missing:
                print(f"  - {m}")
            return False

        print("✅ Validation Successful: All PDF/X metadata present.")
        return True

    except ImportError:
        print(
            "⚠ pypdf not installed. Please install it to verify "
            "metadata programmatically."
        )
        print("Run: pip install pypdf")
        return False
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return False


def main():
    """Generate test PDF and validate PDF/X compliance."""
    output_path = Path("output/compliance_test.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating test PDF at {output_path}...")
    doc = PDFDocument(output_path, is_compliant=True)
    doc.add_puzzle(create_dummy_puzzle())
    doc.save()

    print("Verifying metadata...")
    if check_metadata(output_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
