"""Verify Part 3 structure in PDF table of contents."""

import sys
from pathlib import Path
from pypdf import PdfReader


def verify_structure(pdf_path_str):
    """Check that Part 3 chapters appear in correct order in TOC."""
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        sys.exit(1)

    reader = PdfReader(pdf_path)

    try:
        # Extract TOC from page 3 and 4 (indices 2 and 3)
        toc_text = (
            reader.pages[2].extract_text() + "\n" + reader.pages[3].extract_text()
        )
    except Exception as e:
        print(f"❌ Error reading TOC pages: {e}")
        sys.exit(1)

    # Define expected sequence of headers
    expected_sequence = [
        "Part 3: Intermediate Level",
        "Chapter 7: Stepping Up",
        "Chapter 8: Intermediate Challenges",
        "Chapter 9: Advanced Intermediate",
    ]

    print("----- CHECKING SEQUENCE -----")

    # Simple substring search in order
    current_idx = -1
    last_found = ""

    for item in expected_sequence:
        # Find item in text, searching ONLY after the last found position
        found_idx = toc_text.find(item, current_idx + 1)

        if found_idx == -1:
            print(f"❌ MISSING or OUT OF ORDER: '{item}'")
            print(f"   (Last successfully found item was: '{last_found}')")
            print("\nFull TOC Text for Debugging:\n" + toc_text)
            sys.exit(1)

        print(f"✅ Found '{item}'")
        current_idx = found_idx
        last_found = item

    print("-----------------------------")
    print("✅ Part 3 Structure Verification Passed")
    sys.exit(0)


if __name__ == "__main__":
    verify_structure("books/master-kakuro/output/interior.pdf")
