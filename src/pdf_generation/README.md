# PDF Generation Module

This module provides high-level and low-level tools for generating professional Kakuro puzzle book PDFs. It is designed to produce files ready for automated printing services like **Amazon KDP**.

## Features

- **Multi-Layout Support**: Standard (2 puzzles per page) and Large Print (1 puzzle per page) layouts.
- **Automated Book Assembly**: Handle puzzle numbering, page sequencing, and solution sections.
- **KDP-Ready Compliance**: Automatic font embedding, correct page dimensions, and essential metadata injection.
- **Customizable Rendering**: Configurable fonts, cell sizes, line weights, and clue positioning.

## Architecture

- [`models.py`](models.py): Data models for `PageLayout`, `RenderConfig`, and `BookConfig`.
- [`renderer.py`](renderer.py): Low-level drawing logic for Kakuro grids and cells.
- [`page_builder.py`](page_builder.py): Layout logic for positioning grids and adding page elements.
- [`document.py`](document.py): High-level class (`PDFDocument`) for assembling a multi-page PDF.
- [`fonts.py`](fonts.py): Font registration and fallback management.
- [`compliance.py`](compliance.py): Logic for KDP-specific metadata and standards.

## Usage

See `examples/generate_kakuro_pdf.py` for a complete demonstration.

```python
from src.pdf_generation import PDFDocument, BookConfig

doc = PDFDocument("output.pdf", BookConfig(title="My Puzzles"))
doc.add_puzzles(puzzles)
doc.save()
```

## Amazon KDP Compliance Guide

To ensure your generated PDFs are accepted by KDP and look great in print:

1.  **Page Size**: Use standard sizes like `LETTER` (8.5" x 11") or `A4`. Our `models.py` includes these constants.
2.  **Margins**: KDP requires minimum margins (typically 0.25" to 0.5" depending on page count). `PageLayout` defaults set safe margins for interior content.
3.  **Fonts**: KDP requires all fonts to be embedded. This module uses ReportLab's `TTFont` registration, which forces embedding by default.
4.  **Metadata**: Professional books should have Title and Author metadata. The `compliance.py` module automatically injects these from your `BookConfig`.
5.  **Colors**: For black and white interiors, use grayscale. Our renderer uses `reportlab.lib.colors.black` and `white`.
6.  **No Encryption**: PDFs must be unsecured. This module does not apply any security or encryption.

### Validation
Before uploading, it is recommended to:
- Run the built-in validation script: `python scripts/quality_control/validate_compliance.py`
- Open the PDF in a professional viewer (like Adobe Acrobat) to verify font embedding.
- Use the KDP Print Previewer tool after uploading to check for bleed and margin issues.
