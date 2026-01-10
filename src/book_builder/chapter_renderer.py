"""
Chapter renderer - converts markdown chapters to PDF flowables.

This module parses markdown files and converts them to ReportLab
Platypus flowables for inclusion in PDF documents.
"""

import re
import logging
from pathlib import Path

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Image,
    ListFlowable,
    ListItem,
    KeepTogether,
    HRFlowable,
    Flowable,
    PageBreak,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

from .config import BookConfig

from .diagram_renderer import DiagramFlowable
from .reference_table_renderer import ReferenceTableFlowable
from .progress_tracker_renderer import ProgressTrackerFlowable
from .diagram_models import ReferenceTableDefinition
from .diagrams.chapter1 import CHAPTER1_DIAGRAMS
from .diagrams.chapter2 import CHAPTER2_DIAGRAMS
from .diagrams.chapter3 import CHAPTER3_DIAGRAMS

logger = logging.getLogger(__name__)

# Registry of all programmatic diagrams by chapter
PROGRAMMATIC_DIAGRAMS = {
    "chapter1": CHAPTER1_DIAGRAMS,
    "chapter2": CHAPTER2_DIAGRAMS,
    "chapter3": CHAPTER3_DIAGRAMS,
}


def create_styles(config: BookConfig) -> dict:
    """Create paragraph styles for chapter rendering.

    Args:
        config: Book configuration with font settings.

    Returns:
        Dictionary of style name to ParagraphStyle.
    """
    base_size = 14 if config.layout.large_print else 12
    heading_font = config.fonts.heading
    body_font = config.fonts.body

    styles = {
        "h1": ParagraphStyle(
            "ChapterTitle",
            fontName=heading_font,
            fontSize=base_size + 12,
            leading=base_size + 16,
            spaceBefore=24,
            spaceAfter=24,
            alignment=TA_CENTER,
        ),
        "h2": ParagraphStyle(
            "SectionHeading",
            fontName=heading_font,
            fontSize=base_size + 6,
            leading=base_size + 10,
            spaceBefore=18,
            spaceAfter=12,
        ),
        "h3": ParagraphStyle(
            "SubsectionHeading",
            fontName=heading_font,
            fontSize=base_size + 2,
            leading=base_size + 6,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "BodyText",
            fontName=body_font,
            fontSize=base_size,
            leading=base_size + 6,
            spaceBefore=6,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName=body_font,
            fontSize=base_size - 2,
            leading=base_size + 2,
            spaceBefore=4,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=HexColor("#555555"),
        ),
        "list_item": ParagraphStyle(
            "ListItem",
            fontName=body_font,
            fontSize=base_size,
            leading=base_size + 6,
            leftIndent=20,
            bulletIndent=10,
        ),
    }
    return styles


class ChapterRenderer:
    """Renders markdown chapters to ReportLab flowables."""

    def __init__(self, config: BookConfig, book_dir: Path):
        """Initialize chapter renderer.

        Args:
            config: Book configuration.
            book_dir: Base directory of the book (for resolving relative paths).
        """
        self.config = config
        self.book_dir = book_dir
        self.styles = create_styles(config)

        # Regex patterns for markdown parsing
        self.heading_pattern = re.compile(r"^(#{1,3})\s+(.+)$")
        self.image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
        self.bold_pattern = re.compile(r"\*\*([^*]+)\*\*")
        self.italic_pattern = re.compile(r"\*([^*]+)\*")
        self.bullet_pattern = re.compile(r"^[-*]\s+(.+)$")
        self.hr_pattern = re.compile(r"^---+\s*$")
        self.pagebreak_pattern = re.compile(
            r"^<!--\s*pagebreak\s*-->\s*$", re.IGNORECASE
        )

    def render_chapter(self, chapter_path: Path, chapter_title: str) -> list:
        """Render a markdown chapter to flowables.

        Args:
            chapter_path: Path to the markdown file.
            chapter_title: Title of the chapter (for TOC).

        Returns:
            List of ReportLab flowables.
        """
        flowables = []

        # Read markdown content
        with open(chapter_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse and convert to flowables
        lines = content.split("\n")
        i = 0
        current_list_items = []

        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines (but flush any pending list)
            if not line:
                if current_list_items:
                    flowables.append(self._create_list(current_list_items))
                    current_list_items = []
                i += 1
                continue

            # Horizontal rule
            if self.hr_pattern.match(line):
                if current_list_items:
                    flowables.append(self._create_list(current_list_items))
                    current_list_items = []
                flowables.append(Spacer(1, 12))
                flowables.append(
                    HRFlowable(width="60%", thickness=1, color=HexColor("#CCCCCC"))
                )
                flowables.append(Spacer(1, 12))
                i += 1
                continue

            # Page break marker
            if self.pagebreak_pattern.match(line):
                if current_list_items:
                    flowables.append(self._create_list(current_list_items))
                    current_list_items = []
                flowables.append(PageBreak())
                i += 1
                continue

            # Heading
            heading_match = self.heading_pattern.match(line)
            if heading_match:
                if current_list_items:
                    flowables.append(self._create_list(current_list_items))
                    current_list_items = []
                level = len(heading_match.group(1))
                text = heading_match.group(2)
                style_key = f"h{level}"
                flowables.append(
                    Paragraph(self._format_text(text), self.styles[style_key])
                )
                i += 1
                continue

            # Image
            image_match = self.image_pattern.search(line)
            if image_match:
                if current_list_items:
                    flowables.append(self._create_list(current_list_items))
                    current_list_items = []
                alt_text = image_match.group(1)
                image_path = image_match.group(2)
                img_flowables = self._create_image(
                    image_path, alt_text, chapter_path.parent
                )

                # Check for caption on next line (starts with *)
                if (
                    i + 1 < len(lines)
                    and lines[i + 1].strip().startswith("*")
                    and lines[i + 1].strip().endswith("*")
                ):
                    caption_text = lines[i + 1].strip()[1:-1]  # Remove *
                    caption = Paragraph(caption_text, self.styles["caption"])
                    # Wrap image AND caption in KeepTogether for same page
                    flowables.append(Spacer(1, 16))
                    # Extract the actual image from img_flowables (skip spacers)
                    image_content = [
                        f for f in img_flowables if not isinstance(f, Spacer)
                    ]
                    flowables.append(KeepTogether(image_content + [caption]))
                    flowables.append(Spacer(1, 8))
                    i += 2
                    continue
                else:
                    # No caption - use original flowables
                    flowables.extend(img_flowables)
                i += 1
                continue

            # Bullet list
            bullet_match = self.bullet_pattern.match(line)
            if bullet_match:
                current_list_items.append(bullet_match.group(1))
                i += 1
                continue

            # Regular paragraph
            if current_list_items:
                flowables.append(self._create_list(current_list_items))
                current_list_items = []
            flowables.append(Paragraph(self._format_text(line), self.styles["body"]))
            i += 1

        # Flush any remaining list items
        if current_list_items:
            flowables.append(self._create_list(current_list_items))

        return flowables

    def _format_text(self, text: str) -> str:
        """Format text with inline markup for ReportLab.

        Args:
            text: Raw markdown text.

        Returns:
            Text with ReportLab XML markup.
        """
        # Bold: **text** -> <b>text</b>
        text = self.bold_pattern.sub(r"<b>\1</b>", text)
        # Italic: *text* -> <i>text</i>
        text = self.italic_pattern.sub(r"<i>\1</i>", text)
        return text

    def _create_list(self, items: list[str]) -> ListFlowable:
        """Create a bullet list flowable.

        Args:
            items: List of text items.

        Returns:
            ListFlowable containing all items.
        """
        list_items = [
            ListItem(Paragraph(self._format_text(item), self.styles["list_item"]))
            for item in items
        ]
        return ListFlowable(list_items, bulletType="bullet", leftIndent=20)

    def _create_image(self, image_path: str, alt_text: str, chapter_dir: Path) -> list:
        """Create an image flowable.

        Args:
            image_path: Relative path to the image.
            alt_text: Alternative text for the image.
            chapter_dir: Directory containing the chapter file.

        Returns:
            List containing image and optional spacing.
        """
        # Check for programmatic diagram first
        # Image paths like "visuals/diagrams/chapter1/diagram_1.png"
        programmatic = self._try_programmatic_diagram(image_path)
        if programmatic:
            return programmatic

        # Resolve image path relative to chapter
        full_path = chapter_dir / image_path

        # Check for SVG version first (true vector graphics)
        svg_path = full_path.with_suffix(".svg")
        if svg_path.exists():
            return self._create_svg_image(svg_path, alt_text)

        # Check for PDF version (also vector)
        pdf_path = full_path.with_suffix(".pdf")
        if pdf_path.exists():
            return self._create_pdf_image(pdf_path, alt_text)

        if not full_path.exists():
            logger.warning(f"Image not found: {full_path}")
            return [
                Paragraph(f"[Image not found: {image_path}]", self.styles["caption"])
            ]

        return self._create_raster_image(full_path, alt_text)

    def _try_programmatic_diagram(self, image_path: str) -> list | None:
        """Check if image path matches a programmatic diagram definition.

        Args:
            image_path: The image path from markdown (e.g., visuals/diagrams/...)

        Returns:
            List of flowables if programmatic diagram found, None otherwise.
        """
        # Special case for Progress Tracker
        if image_path == "programmatic:tracker":
            logger.info("Using Progress Tracker diagram")
            # Calculate max width
            max_width = (
                self.config.page_width_points
                - (self.config.layout.margins.left + self.config.layout.margins.right)
                * 72
            )
            flowable = ProgressTrackerFlowable(width=max_width)
            return [Spacer(1, 16), flowable, Spacer(1, 8)]

        # Parse path like "visuals/diagrams/chapter1/diagram_1.png"
        import re

        match = re.search(r"chapter(\d+)/diagram_(\d+)", image_path)
        if not match:
            return None

        chapter_num = match.group(1)
        diagram_num = match.group(2)
        chapter_key = f"chapter{chapter_num}"
        diagram_key = f"diagram_{diagram_num}"

        if chapter_key not in PROGRAMMATIC_DIAGRAMS:
            return None

        chapter_diagrams = PROGRAMMATIC_DIAGRAMS[chapter_key]
        if diagram_key not in chapter_diagrams:
            return None

        diagram_def = chapter_diagrams[diagram_key]
        logger.info(f"Using programmatic diagram: {chapter_key}/{diagram_key}")

        # Calculate max width
        max_width = (
            self.config.page_width_points
            - (self.config.layout.margins.left + self.config.layout.margins.right) * 72
        )

        # Choose appropriate flowable based on diagram type
        if isinstance(diagram_def, ReferenceTableDefinition):
            flowable = ReferenceTableFlowable(diagram_def, max_width=max_width)
        else:
            flowable = DiagramFlowable(diagram_def, max_width=max_width)

        # Don't wrap in KeepTogether here - caller handles grouping with caption
        return [Spacer(1, 16), flowable, Spacer(1, 8)]

    def _create_raster_image(self, full_path: Path, alt_text: str) -> list:
        """Create an image flowable from a raster image (PNG, JPG, etc.).

        Note: Raster images should only be used as a last resort when vector
        formats (SVG, PDF) are not available. Vector formats scale without
        quality loss.

        Args:
            full_path: Full path to the image file.
            alt_text: Alternative text for the image.

        Returns:
            List containing image and optional spacing.
        """
        # Calculate max dimensions
        max_width = (
            self.config.page_width_points
            - (self.config.layout.margins.left + self.config.layout.margins.right) * 72
        )
        page_height = (
            self.config.page_height_points
            - (self.config.layout.margins.top + self.config.layout.margins.bottom) * 72
        )
        max_height = page_height - 72  # Leave some room for page elements

        try:
            # Load image to get actual dimensions
            from PIL import Image as PILImage

            with PILImage.open(full_path) as pil_img:
                img_width, img_height = pil_img.size

            # Always scale to full width first
            scale = max_width / img_width
            final_width = max_width
            final_height = img_height * scale

            # If scaled height exceeds page, cap it
            if final_height > max_height:
                scale = max_height / img_height
                final_height = max_height
                final_width = img_width * scale

            logger.warning(
                f"Using raster image (consider vector format): {full_path.name}"
            )

            img = Image(str(full_path), width=final_width, height=final_height)
            return [Spacer(1, 16), KeepTogether([img]), Spacer(1, 8)]
        except Exception as e:
            logger.error(f"Failed to load image {full_path}: {e}")
            return [Paragraph(f"[Image error: {full_path}]", self.styles["caption"])]

    def _create_svg_image(self, svg_path: Path, alt_text: str) -> list:
        """Create an image flowable from an SVG file (true vector graphics).

        Args:
            svg_path: Path to the SVG file.
            alt_text: Alternative text for the image.

        Returns:
            List containing image and optional spacing.
        """
        from svglib.svglib import svg2rlg

        max_width = (
            self.config.page_width_points
            - (self.config.layout.margins.left + self.config.layout.margins.right) * 72
        )
        page_height = (
            self.config.page_height_points
            - (self.config.layout.margins.top + self.config.layout.margins.bottom) * 72
        )
        max_height = page_height - 72  # Leave room for page elements

        try:
            drawing = svg2rlg(str(svg_path))
            if drawing is None:
                logger.warning(f"Could not parse SVG: {svg_path}")
                return [
                    Paragraph(f"[SVG parse error: {svg_path}]", self.styles["caption"])
                ]

            # Get original dimensions
            orig_width = drawing.width
            orig_height = drawing.height

            # Always scale to full width - vector graphics maintain quality
            scale = max_width / orig_width
            final_width = max_width
            final_height = orig_height * scale

            # If scaled height exceeds page, cap it
            if final_height > max_height:
                scale = max_height / orig_height
                final_height = max_height
                final_width = orig_width * scale

            drawing.width = final_width
            drawing.height = final_height
            drawing.scale(scale, scale)

            logger.info(
                f"SVG: {svg_path.name} scaled to "
                f"{final_width:.0f}x{final_height:.0f}pt"
            )

            return [Spacer(1, 16), KeepTogether([drawing]), Spacer(1, 8)]

        except Exception as e:
            logger.error(f"Failed to load SVG {svg_path}: {e}")
            return [Paragraph(f"[SVG error: {svg_path}]", self.styles["caption"])]

    def _create_pdf_image(self, pdf_path: Path, alt_text: str) -> list:
        """Create an image flowable from a PDF file (vector graphics).

        Args:
            pdf_path: Path to the PDF file.
            alt_text: Alternative text for the image.

        Returns:
            List containing image and optional spacing.
        """
        from pdfrw import PdfReader
        from pdfrw.buildxobj import pagexobj

        max_width = (
            self.config.page_width_points
            - (self.config.layout.margins.left + self.config.layout.margins.right) * 72
        )
        page_height = (
            self.config.page_height_points
            - (self.config.layout.margins.top + self.config.layout.margins.bottom) * 72
        )
        max_height = page_height - 72  # Leave room for page elements

        try:
            # Use pdfrw to read the PDF and convert to a ReportLab-compatible form
            pdf = PdfReader(str(pdf_path))
            if not pdf.pages:
                logger.warning(f"PDF has no pages: {pdf_path}")
                return [Paragraph(f"[Empty PDF: {pdf_path}]", self.styles["caption"])]

            # Get the first page
            page = pdf.pages[0]
            xobj = pagexobj(page)

            # Get original dimensions
            orig_width = float(xobj.BBox[2]) - float(xobj.BBox[0])
            orig_height = float(xobj.BBox[3]) - float(xobj.BBox[1])

            # Always scale to full width - vector graphics maintain quality
            # Height will scale proportionally
            scale = max_width / orig_width
            final_width = max_width
            final_height = orig_height * scale

            # If scaled height exceeds page, cap it
            if final_height > max_height:
                scale = max_height / orig_height
                final_height = max_height
                final_width = orig_width * scale

            logger.info(
                f"PDF: {pdf_path.name} scaled to "
                f"{final_width:.0f}x{final_height:.0f}pt"
            )

            # Create a custom flowable for the PDF
            pdf_flowable = PdfImageFlowable(xobj, final_width, final_height)
            return [Spacer(1, 16), KeepTogether([pdf_flowable]), Spacer(1, 8)]

        except Exception as e:
            logger.error(f"Failed to load PDF {pdf_path}: {e}")
            return [Paragraph(f"[PDF error: {pdf_path}]", self.styles["caption"])]


class PdfImageFlowable(Flowable):
    """A flowable that renders a PDF page."""

    def __init__(self, xobj, width, height):
        """Initialize the PDF image flowable.

        Args:
            xobj: The PDF XObject to render.
            width: Target width for the image.
            height: Target height for the image.
        """
        super().__init__()
        self.xobj = xobj
        self.width = width
        self.height = height

    def wrap(self, available_width, available_height):
        """Return the size of this flowable."""
        return self.width, self.height

    def draw(self):
        """Draw the PDF page onto the canvas."""
        from pdfrw.toreportlab import makerl

        # Get original dimensions
        orig_width = float(self.xobj.BBox[2]) - float(self.xobj.BBox[0])
        orig_height = float(self.xobj.BBox[3]) - float(self.xobj.BBox[1])

        # Calculate scale
        scale_x = self.width / orig_width
        scale_y = self.height / orig_height

        self.canv.saveState()
        self.canv.scale(scale_x, scale_y)

        # Render the PDF page
        rl_obj = makerl(self.canv, self.xobj)
        self.canv.doForm(rl_obj)

        self.canv.restoreState()
