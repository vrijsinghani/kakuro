"""
Diagram definitions for instructional chapters.

This package contains programmatic diagram definitions that are
rendered directly using ReportLab, avoiding the HTML conversion pipeline.
"""

from .chapter1 import CHAPTER1_DIAGRAMS, get_chapter1_diagram

__all__ = ["CHAPTER1_DIAGRAMS", "get_chapter1_diagram"]
