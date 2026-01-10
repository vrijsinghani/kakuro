"""Validate table of contents for duplicate entries."""

import sys
from pathlib import Path
from pypdf import PdfReader


def validate_toc(pdf_path_str):
    """Check PDF table of contents for duplicate or malformed entries."""
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        sys.exit(1)

    reader = PdfReader(pdf_path)

    # Extract TOC page (Page 3 and 4, index 2 and 3)
    try:
        toc_text = (
            reader.pages[2].extract_text() + "\n" + reader.pages[3].extract_text()
        )
    except Exception as e:
        print(f"❌ Error reading TOC pages: {e}")
        sys.exit(1)

    lines = toc_text.split("\n")

    print("----- TOC ENTRIES -----")
    clean_entries = []
    for line in lines:
        line = line.strip()
        if not line or line == "Table of Contents":
            continue

        # Heuristic: If line ends in a number, it's likely a TOC entry
        # Note: ReportLab TOC generation might put number on newline or same line
        # This simple check looks for visual duplicates in the extracted text sequence
        clean_entries.append(line)
        print(line)

    print("-----------------------")

    # Check for adjacent duplicates
    errors = []
    for i in range(len(clean_entries) - 1):
        current = clean_entries[i]
        next_entry = clean_entries[i + 1]

        # Exact match duplication
        if current == next_entry:
            errors.append(f"Duplicate entry found: '{current}'")

        # Partial match (Title vs Title + PageNum)
        # e.g., "Part 3: Intermediate Level" vs
        # "Part 3: Intermediate Level 119"
        if current in next_entry and current != next_entry:
            # Check if it's just the label repeated
            if next_entry.startswith(current):
                errors.append(
                    f"Potential duplicate header found: '{current}' "
                    f"followed by '{next_entry}'"
                )

    if errors:
        print("\n❌ TOC VALIDATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\n✅ TOC Validation Passed: No adjacent duplicate entries found.")
        sys.exit(0)


if __name__ == "__main__":
    validate_toc("books/master-kakuro/output/interior.pdf")
