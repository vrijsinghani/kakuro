"""Verify PDF content and structure."""

import sys
from pathlib import Path

# Try to import pypdf
try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not found. Trying to find another way...")
    sys.exit(1)


def verify_pdf(pdf_path_str):
    """Check PDF for expected chapter content and TOC structure."""
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return

    reader = PdfReader(pdf_path)
    print(f"PDF Page Count: {len(reader.pages)}")

    # 1. Check for Chapter 3 Title in entire text
    found_chapter_3 = False
    chapter_3_title = "Chapter 3: Your First Puzzle Walkthrough"

    # 2. Check for Unique Text
    unique_text = "The sum of 4 in two cells can ONLY be 1 + 3"
    found_unique_text = False

    # 3. Check for specific string in Table of Contents (usually first few pages)
    toc_pages = []

    # Scan all pages
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if chapter_3_title in text:
            print(f"✅ Found Chapter 3 Title on page {i+1}")
            found_chapter_3 = True
            # Assuming TOC is in first 10 pages
            if i < 10:
                toc_pages.append(i)

        if unique_text in text:
            print(f"✅ Found Unique Text on page {i+1}")
            found_unique_text = True

    if not found_chapter_3:
        print("❌ Chapter 3 Title NOT found in text.")
    if not found_unique_text:
        print("❌ Unique Text from Chapter 3 NOT found.")

    # 4. Check TOC Structure (heuristic)
    # If we found the title on multiple early pages, it might be double
    # TOC entry
    if len(toc_pages) > 1:
        print(
            f"⚠️ Warning: Chapter 3 title found on multiple early pages: "
            f"{toc_pages}. Possible duplicate TOC entry?"
        )
    elif len(toc_pages) == 1:
        print(
            f"ℹ️ Chapter 3 title found on page {toc_pages[0]+1} "
            f"(likely TOC or start of chapter)."
        )


if __name__ == "__main__":
    verify_pdf("books/master-kakuro/output/interior.pdf")
