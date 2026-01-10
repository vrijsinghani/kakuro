"""
Book Builder Module.

This module provides functionality for building complete Kakuro puzzle books
from YAML configuration files. It assembles chapters, puzzles, and solutions
into print-ready PDF documents.

Main exports:
    - BookDocument: High-level document builder for complete books
    - build_book: Build a complete book from configuration
    - BookConfig: Book configuration model
    - ChapterRenderer: Markdown to PDF renderer
"""

from .config import BookConfig, ChapterConfig, PuzzleSectionConfig, LayoutConfig
from .chapter_renderer import ChapterRenderer
from .builder import build_book, build_chapters_only, build_puzzles_only
from .assembler import BookAssembler
from .document import BookDocument, TOCEntry
from .puzzle_flowable import PuzzleFlowable, SolutionFlowable

__all__ = [
    "BookConfig",
    "ChapterConfig",
    "PuzzleSectionConfig",
    "LayoutConfig",
    "ChapterRenderer",
    "BookAssembler",
    "BookDocument",
    "TOCEntry",
    "PuzzleFlowable",
    "SolutionFlowable",
    "build_book",
    "build_chapters_only",
    "build_puzzles_only",
]

__version__ = "0.1.0"
