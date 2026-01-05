"""Logging configuration for puzzle generation module."""

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """
    Configure logging for the puzzle generation module.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logger = logging.getLogger("puzzle_generation")
    logger.setLevel(numeric_level)
