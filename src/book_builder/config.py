"""
Configuration models for book building.

This module defines Pydantic models for parsing and validating
book.yaml configuration files.
"""

from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field
import yaml


class MetadataConfig(BaseModel):
    """Book metadata configuration."""

    title: str
    subtitle: Optional[str] = None
    author: str = ""
    isbn: Optional[str] = None


class ChapterConfig(BaseModel):
    """Chapter configuration."""

    path: str
    title: str


class PuzzleSectionConfig(BaseModel):
    """Puzzle section configuration."""

    title: str
    difficulty: Literal["beginner", "intermediate", "expert"]
    count: int
    grid_sizes: list[int] = Field(default_factory=lambda: [9, 10, 11])


class FrontMatterItem(BaseModel):
    """Front matter item configuration."""

    type: Literal["title_page", "copyright", "toc"]


class BackMatterItem(BaseModel):
    """Back matter item configuration."""

    type: Literal["solutions", "about_author", "notes"]
    path: Optional[str] = None


class ContentConfig(BaseModel):
    """Content structure configuration."""

    front_matter: list[FrontMatterItem] = Field(default_factory=list)
    chapters: list[ChapterConfig] = Field(default_factory=list)
    puzzle_sections: list[PuzzleSectionConfig] = Field(default_factory=list)
    back_matter: list[BackMatterItem] = Field(default_factory=list)


class MarginsConfig(BaseModel):
    """Page margins in inches."""

    top: float = 0.75
    bottom: float = 0.75
    left: float = 0.75
    right: float = 0.75


class LayoutConfig(BaseModel):
    """Page layout configuration."""

    page_size: Literal["letter", "a4"] | tuple[float, float] = "letter"
    margins: MarginsConfig = Field(default_factory=MarginsConfig)
    large_print: bool = False
    puzzles_per_page: int = 1
    solutions_per_page: int = 6


class FontsConfig(BaseModel):
    """Font configuration."""

    body: str = "Helvetica"
    heading: str = "Helvetica-Bold"
    puzzle: str = "Helvetica"


class BookConfig(BaseModel):
    """Complete book configuration."""

    metadata: MetadataConfig
    content: ContentConfig = Field(default_factory=ContentConfig)
    layout: LayoutConfig = Field(default_factory=LayoutConfig)
    fonts: FontsConfig = Field(default_factory=FontsConfig)

    @classmethod
    def from_yaml(cls, path: Path) -> "BookConfig":
        """Load configuration from a YAML file.

        Args:
            path: Path to the book.yaml file.

        Returns:
            Parsed BookConfig instance.
        """
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @property
    def page_width_points(self) -> float:
        """Get page width in points."""
        if self.layout.page_size == "letter":
            return 8.5 * 72
        elif self.layout.page_size == "a4":
            return 595.27
        else:
            return self.layout.page_size[0] * 72

    @property
    def page_height_points(self) -> float:
        """Get page height in points."""
        if self.layout.page_size == "letter":
            return 11 * 72
        elif self.layout.page_size == "a4":
            return 841.89
        else:
            return self.layout.page_size[1] * 72
