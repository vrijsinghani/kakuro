#!/usr/bin/env python3
"""
Convert HTML diagrams to SVG files using Playwright.

This script extracts individual diagram containers from HTML files
and saves them as scalable SVG images for use in PDF generation.
"""

import asyncio
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright


async def extract_diagrams_to_svg(html_path: Path, output_dir: Path, chapter_num: int):
    """Extract each diagram from HTML and save as SVG (vector graphics).

    Args:
        html_path: Path to the HTML file with diagrams.
        output_dir: Directory to save files.
        chapter_num: Chapter number for naming.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        await page.goto(f"file://{html_path.absolute()}")
        await page.wait_for_load_state("networkidle")

        # Find all diagram containers
        diagrams = await page.query_selector_all(".diagram-container")
        print(f"Found {len(diagrams)} diagrams in {html_path.name}")

        for i, diagram in enumerate(diagrams, 1):
            # Get the bounding box
            box = await diagram.bounding_box()
            if not box:
                continue

            pdf_path = output_dir / f"diagram_{i}.pdf"
            svg_path = output_dir / f"diagram_{i}.svg"

            # Isolate this diagram for PDF export
            await page.evaluate(
                """(index) => {
                const containers = document.querySelectorAll('.diagram-container');
                containers.forEach((c, i) => {
                    c.style.display = i === index ? 'block' : 'none';
                    if (i === index) {
                        c.style.pageBreakAfter = 'avoid';
                        c.style.margin = '0';
                        c.style.padding = '20px';
                    }
                });
                document.body.style.background = 'white';
                document.body.style.margin = '0';
                document.body.style.padding = '0';
            }""",
                i - 1,
            )

            # Get diagram title for naming
            title_elem = await diagram.query_selector("h2")
            title = await title_elem.inner_text() if title_elem else f"Diagram {i}"

            # Save as PDF first (vector)
            await page.pdf(
                path=str(pdf_path),
                width=f"{int(box['width'] + 40)}px",
                height=f"{int(box['height'] + 40)}px",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )

            # Convert PDF to SVG using pdf2svg
            subprocess.run(["pdf2svg", str(pdf_path), str(svg_path)], check=True)

            print(f"  Saved diagram {i}: {title[:50]}...")

            # Reset display for next iteration
            await page.evaluate(
                """() => {
                document.querySelectorAll('.diagram-container').forEach(c => {
                    c.style.display = 'block';
                });
            }"""
            )

        await browser.close()


async def main():
    """Process all chapter HTML files."""
    base_dir = Path(__file__).parent.parent

    chapters = [
        (
            base_dir / "kdp/book_content/chapters/visuals/kakuro_chapter1_visuals.html",
            base_dir
            / "books/beginner-to-expert-250/chapters/visuals/diagrams/chapter1",
            1,
        ),
        (
            base_dir / "kdp/book_content/chapters/visuals/kakuro_chapter2_visuals.html",
            base_dir
            / "books/beginner-to-expert-250/chapters/visuals/diagrams/chapter2",
            2,
        ),
    ]

    for html_path, output_dir, chapter_num in chapters:
        if html_path.exists():
            print(f"\nProcessing Chapter {chapter_num}...")
            await extract_diagrams_to_svg(html_path, output_dir, chapter_num)
        else:
            print(f"Warning: {html_path} not found")

    print("\nDone! Diagrams saved as PDF (vector) and PNG (raster).")


if __name__ == "__main__":
    asyncio.run(main())
