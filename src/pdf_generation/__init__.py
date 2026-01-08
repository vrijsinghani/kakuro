"""
Kakuro PDF Generation Module.

This module provides functionality for generating print-ready PDF files
from Kakuro puzzles for Amazon KDP publishing.

Main exports:
    - create_puzzle_book: Generate a complete puzzle book PDF
    - PDFDocument: Multi-page document builder
    - PageLayout: Page configuration (dimensions, margins)
    - RenderConfig: Rendering configuration (fonts, line widths)
    - BookConfig: Complete book configuration
"""

from .models import (
    PageLayout,
    Margins,
    RenderConfig,
    BookConfig,
    PageSize,
    LETTER,
    A4,
    POINTS_PER_INCH,
)
from .fonts import register_fonts, get_font_name, is_font_available
from .renderer import render_grid
from .page_builder import build_puzzle_page, build_solution_page
from .document import PDFDocument, create_puzzle_book

__all__ = [
    # Constants
    "POINTS_PER_INCH",
    # Models
    "PageLayout",
    "Margins",
    "RenderConfig",
    "BookConfig",
    "PageSize",
    "LETTER",
    "A4",
    # Fonts
    "register_fonts",
    "get_font_name",
    "is_font_available",
    # Rendering
    "render_grid",
    # Page building
    "build_puzzle_page",
    "build_solution_page",
    # Document
    "PDFDocument",
    "create_puzzle_book",
]

__version__ = "0.1.0"
