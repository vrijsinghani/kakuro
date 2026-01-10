"""Book builder configuration models and defaults."""

from pathlib import Path
from typing import Optional, Literal, Union
import yaml
from pydantic import BaseModel, Field


# Default embeddable fonts
DEFAULT_FONTS = {
    "body": "NotoSans-Regular",
    "heading": "NotoSans-Bold",
    "puzzle": "NotoSans-Regular",
    "caption": "NotoSans-Regular",  # Replaces Helvetica-Oblique
    # Symbol is usually built-in but we should use a unicode font ideally
    "symbol": "Symbol",
}


class MetadataConfig(BaseModel):
    """Book metadata configuration."""

    title: str
    subtitle: Optional[str] = None
    author: str = ""
    isbn: Optional[str] = None


class PartHeaderConfig(BaseModel):
    """Part header configuration."""

    type: Literal["part_header"] = "part_header"
    title: str


class ChapterConfig(BaseModel):
    """Chapter configuration."""

    type: Literal["chapter"] = "chapter"
    path: str
    title: str


class PuzzleSectionConfig(BaseModel):
    """Puzzle section configuration."""

    type: Literal["puzzle_section"] = "puzzle_section"
    title: Optional[str] = None
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
    body: list[Union[PartHeaderConfig, ChapterConfig, PuzzleSectionConfig]] = Field(
        default_factory=list
    )
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

    body: str = DEFAULT_FONTS["body"]
    heading: str = DEFAULT_FONTS["heading"]
    puzzle: str = DEFAULT_FONTS["puzzle"]


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

    def validate_files(self, book_dir: Path) -> list[str]:
        """Validate that all referenced files exist.

        Args:
            book_dir: Base directory of the book.

        Returns:
            List of error messages for missing files.
        """
        errors = []

        # Validate body files (chapters only)
        for item in self.content.body:
            if isinstance(item, ChapterConfig):
                chapter_path = book_dir / item.path
                if not chapter_path.exists():
                    errors.append(f"Chapter file not found: {item.path}")

        # Validate back matter files
        for item in self.content.back_matter:
            if item.path:
                item_path = book_dir / item.path
                if not item_path.exists():
                    errors.append(f"Back matter file not found: {item.path}")

        return errors
