"""Inspect PDF content for debugging purposes."""

from pathlib import Path
from pypdf import PdfReader


def inspect_pdf(pdf_path_str):
    """Extract and display content from specific PDF pages."""
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return

    reader = PdfReader(pdf_path)

    # 1. Inspect TOC Page (Page 3, index 2)
    print("----- PAGE 3 (TOC) CONTENT -----")
    try:
        print(reader.pages[2].extract_text())
    except Exception as e:
        print(f"Error reading page 3: {e}")
    print("--------------------------------")

    # 2. Inspect Pages 120-130 (Part 3 Area)
    start_page = 120
    end_page = 130
    print(f"----- PAGES {start_page}-{end_page} CONTENT -----")
    for i in range(start_page, min(end_page, len(reader.pages))):
        print(f"--- PAGE {i+1} ---")
        print(reader.pages[i].extract_text())
    print("--------------------------------")


if __name__ == "__main__":
    inspect_pdf("books/master-kakuro/output/interior.pdf")
