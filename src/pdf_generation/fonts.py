"""
Font management for PDF generation.

This module handles font registration and embedding for PDF output.
It provides fallback to built-in fonts when custom fonts are unavailable.
"""

import logging
from pathlib import Path
from typing import Optional

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger(__name__)

# Default font assets directory
FONTS_DIR = Path(__file__).parent.parent.parent / "assets" / "fonts"

# Built-in ReportLab fonts (always available)
BUILTIN_FONTS = {
    "Helvetica",
    "Helvetica-Bold",
    "Helvetica-Oblique",
    "Helvetica-BoldOblique",
    "Times-Roman",
    "Times-Bold",
    "Times-Italic",
    "Times-BoldItalic",
    "Courier",
    "Courier-Bold",
    "Courier-Oblique",
    "Courier-BoldOblique",
}

# Registered custom fonts cache
_registered_fonts: set[str] = set()


def register_fonts(fonts_dir: Optional[Path] = None) -> list[str]:
    """Register custom fonts from the fonts directory.

    Args:
        fonts_dir: Path to directory containing .ttf font files.
                  Defaults to assets/fonts/

    Returns:
        List of successfully registered font names.
    """
    fonts_dir = fonts_dir or FONTS_DIR
    registered = []

    if not fonts_dir.exists():
        logger.debug(f"Fonts directory not found: {fonts_dir}")
        return registered

    for font_file in fonts_dir.glob("*.ttf"):
        font_name = font_file.stem
        if font_name in _registered_fonts:
            registered.append(font_name)
            continue

        try:
            pdfmetrics.registerFont(TTFont(font_name, str(font_file)))
            _registered_fonts.add(font_name)
            registered.append(font_name)
            logger.debug(f"Registered font: {font_name}")
        except Exception as e:
            logger.warning(f"Failed to register font {font_file}: {e}")

    return registered


def get_font_name(preferred: str = "Helvetica", fallback: str = "Helvetica") -> str:
    """Get an available font name, with fallback.

    Args:
        preferred: Preferred font name to use.
        fallback: Fallback font name if preferred is unavailable.

    Returns:
        Name of an available font.
    """
    # Check if preferred font is built-in
    if preferred in BUILTIN_FONTS:
        return preferred

    # Check if preferred font is registered
    if preferred in _registered_fonts:
        return preferred

    # Try to register fonts and check again
    register_fonts()
    if preferred in _registered_fonts:
        return preferred

    # Use fallback
    if fallback in BUILTIN_FONTS or fallback in _registered_fonts:
        logger.debug(f"Font '{preferred}' not available, using '{fallback}'")
        return fallback

    # Ultimate fallback to Helvetica
    logger.warning(f"Neither '{preferred}' nor '{fallback}' available, using Helvetica")
    return "Helvetica"


def is_font_available(font_name: str) -> bool:
    """Check if a font is available for use.

    Args:
        font_name: Name of the font to check.

    Returns:
        True if the font is available.
    """
    if font_name in BUILTIN_FONTS:
        return True
    if font_name in _registered_fonts:
        return True
    # Try registering fonts
    register_fonts()
    return font_name in _registered_fonts
