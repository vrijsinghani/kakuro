"""
Diagram renderer - generates instructional diagrams using ReportLab.

This module renders diagram definitions directly to ReportLab Flowables,
eliminating the need for HTML→browser→screenshot conversion.
"""

import logging
from reportlab.platypus import Flowable
from reportlab.lib.colors import black, white, HexColor, Color
from reportlab.lib.units import inch

from .diagram_models import (
    DiagramDefinition,
    DiagramGrid,
    DiagramCell,
    CellType,
    HighlightStyle,
    AnnotationBox,
    HIGHLIGHT_COLORS,
    ANNOTATION_STYLES,
)

logger = logging.getLogger(__name__)


class DiagramFlowable(Flowable):
    """A Flowable that renders a complete instructional diagram."""

    # Default styling
    DEFAULT_CELL_SIZE = 36  # points
    DEFAULT_FONT = "Helvetica"
    DEFAULT_LINE_WIDTH = 1.0
    DEFAULT_THICK_LINE_WIDTH = 2.0
    NAVY_BLUE = HexColor("#1a365d")  # Navy blue for black cells

    # Spacing constants
    TITLE_BOTTOM_PADDING = 15  # Space below main title
    GRID_TITLE_HEIGHT = 20  # Space for grid titles like "✓ CORRECT"
    GRID_BOTTOM_PADDING = 15  # Space below grids
    CAPTION_TOP_PADDING = 10  # Space above caption

    def __init__(
        self,
        diagram: DiagramDefinition,
        max_width: float = 6.0 * inch,
        cell_size: float = None,
    ):
        """Initialize diagram flowable.

        Args:
            diagram: The diagram definition to render.
            max_width: Maximum width in points.
            cell_size: Cell size in points (auto-calculated if None).
        """
        super().__init__()
        self.diagram = diagram
        self.max_width = max_width
        self.cell_size = cell_size or self.DEFAULT_CELL_SIZE

        # Calculate dimensions
        self._calculate_dimensions()

    def _calculate_dimensions(self):
        """Calculate the total dimensions needed for the diagram."""
        # Title height (main diagram title)
        self.title_height = 30 + self.TITLE_BOTTOM_PADDING if self.diagram.title else 0

        # Calculate grid dimensions (including per-grid title heights)
        self.grid_heights = []
        self.grid_widths = []

        for grid in self.diagram.grids:
            # Auto-scale cell size if grid is too wide
            grid_width = grid.cols * self.cell_size
            if grid_width > self.max_width:
                scale = self.max_width / grid_width
                self.cell_size = self.cell_size * scale

            self.grid_widths.append(grid.cols * self.cell_size)
            # Include title height (20pt) in each grid's height if it has a title
            grid_height = grid.rows * self.cell_size
            if grid.title:
                grid_height += 20  # Space for grid title
            self.grid_heights.append(grid_height)

        # Layout grids
        if self.diagram.layout == "horizontal" and len(self.diagram.grids) > 1:
            grid_spacing = 20
            total_grid_width = sum(self.grid_widths) + grid_spacing * (
                len(self.diagram.grids) - 1
            )
            # Scale down if too wide
            if total_grid_width > self.max_width:
                scale = self.max_width / total_grid_width
                self.cell_size *= scale
                self.grid_widths = [w * scale for w in self.grid_widths]
                self.grid_heights = [h * scale for h in self.grid_heights]
            self.total_grid_width = sum(self.grid_widths) + grid_spacing * (
                len(self.diagram.grids) - 1
            )
            self.total_grid_height = max(self.grid_heights) if self.grid_heights else 0
        else:
            self.total_grid_width = max(self.grid_widths) if self.grid_widths else 0
            self.total_grid_height = sum(self.grid_heights) if self.grid_heights else 0

        # Annotations height
        self.annotations_height = len(self.diagram.annotations) * 50

        # Legend dimensions
        self.legend_position = getattr(self.diagram, "legend_position", "right")
        if self.diagram.legend:
            num_items = len(self.diagram.legend.items)
            has_title = 1 if self.diagram.legend.title else 0
            self.legend_height = (num_items + has_title) * 20 + 10
            # Calculate legend width for right positioning
            max_label_len = max(
                len(label) for label in self.diagram.legend.items.values()
            )
            self.legend_width = max(150, max_label_len * 6 + 30)
        else:
            self.legend_height = 0
            self.legend_width = 0

        # Caption height
        self.caption_height = (
            self.CAPTION_TOP_PADDING + 20 if self.diagram.caption else 0
        )

        # Total dimensions - always use max_width for proper centering
        self.width = self.max_width
        if self.legend_position == "right" and self.diagram.legend:
            # Grid + legend side by side - calculate content width for centering
            self.content_width = self.total_grid_width + self.legend_width + 30
            legend_contributes_height = 0
        else:
            self.content_width = self.total_grid_width
            legend_contributes_height = self.legend_height

        # Grid title heights are now included in grid_heights, so no separate addition
        self.height = (
            self.title_height
            + max(
                self.total_grid_height,
                self.legend_height if self.legend_position == "right" else 0,
            )
            + self.GRID_BOTTOM_PADDING
            + self.annotations_height
            + legend_contributes_height
            + self.caption_height
            + 10  # Bottom padding
        )

    def wrap(self, available_width, available_height):
        """Return the size needed for this flowable."""
        return (self.width, self.height)

    def draw(self):
        """Draw the complete diagram."""
        canvas = self.canv
        y_cursor = self.height

        # Draw title
        if self.diagram.title:
            y_cursor -= 30  # Title text height
            self._draw_title(canvas, y_cursor)
            y_cursor -= self.TITLE_BOTTOM_PADDING

        # Draw grids (and legend to the right if positioned there)
        # Note: grid titles are drawn within _draw_grid, which adjusts y internally
        grid_y = y_cursor

        if self.legend_position == "right" and self.diagram.legend:
            # Calculate combined width and center everything
            gap = 30  # Gap between grid and legend
            combined_width = self.total_grid_width + gap + self.legend_width
            start_x = (self.width - combined_width) / 2

            # Draw grids starting from centered position
            if self.diagram.layout == "horizontal":
                self._draw_grids_horizontal(canvas, y_cursor, start_x=start_x)
            else:
                self._draw_grids_vertical(canvas, y_cursor, start_x=start_x)

            # Draw legend to the right of grids, vertically centered with grid cells
            legend_x = start_x + self.total_grid_width + gap
            legend_center_y = grid_y - (self.total_grid_height - self.legend_height) / 2
            self._draw_legend_at(canvas, legend_x, legend_center_y)
        else:
            # Center grids
            if self.diagram.layout == "horizontal":
                self._draw_grids_horizontal(canvas, y_cursor)
            else:
                self._draw_grids_vertical(canvas, y_cursor)

        y_cursor -= self.total_grid_height + self.GRID_BOTTOM_PADDING

        # Draw legend below if not positioned right
        if self.diagram.legend and self.legend_position != "right":
            self._draw_legend(canvas, y_cursor)
            y_cursor -= self.legend_height

        # Draw annotations
        for annotation in self.diagram.annotations:
            self._draw_annotation_box(canvas, annotation, y_cursor)
            y_cursor -= 50

        # Draw caption
        if self.diagram.caption:
            self._draw_caption(canvas, 10)

    def _draw_grids_horizontal(self, canvas, y, start_x: float = None):
        """Draw multiple grids side by side."""
        grid_spacing = 20
        if start_x is not None:
            x_cursor = start_x
        else:
            x_cursor = (self.width - self.total_grid_width) / 2

        for i, grid in enumerate(self.diagram.grids):
            # Align grids at top
            self._draw_grid(canvas, grid, x_cursor, y)
            x_cursor += self.grid_widths[i] + grid_spacing

    def _draw_grids_vertical(self, canvas, y, start_x: float = None):
        """Draw grids stacked vertically."""
        y_cursor = y

        for i, grid in enumerate(self.diagram.grids):
            if start_x is not None:
                x = start_x
            else:
                x = (self.width - self.grid_widths[i]) / 2
            self._draw_grid(canvas, grid, x, y_cursor)
            y_cursor -= self.grid_heights[i] + 10

    def _draw_grid(self, canvas, grid: DiagramGrid, x: float, y: float):
        """Draw a single grid at the specified position."""
        canvas.saveState()

        # Draw grid title if present (20pt reserved in height calculation)
        if grid.title:
            canvas.setFont("Helvetica-Bold", 11)
            title_width = canvas.stringWidth(grid.title, "Helvetica-Bold", 11)
            title_x = x + (grid.cols * self.cell_size - title_width) / 2
            canvas.drawString(title_x, y - 5, grid.title)
            y -= 20

        # Draw cells
        for row in range(grid.rows):
            for col in range(grid.cols):
                cell_x = x + col * self.cell_size
                cell_y = y - (row + 1) * self.cell_size

                cell = grid.get_cell(row, col)
                if cell:
                    self._draw_cell(canvas, cell, cell_x, cell_y)
                else:
                    # Default white cell
                    self._draw_white_cell(canvas, cell_x, cell_y, None, None)

        # Draw outer border
        canvas.setStrokeColor(black)
        canvas.setLineWidth(self.DEFAULT_THICK_LINE_WIDTH)
        grid_width = grid.cols * self.cell_size
        grid_height = grid.rows * self.cell_size
        canvas.rect(x, y - grid_height, grid_width, grid_height, stroke=1, fill=0)

        # Draw grid caption if present
        if grid.caption:
            canvas.setFont("Helvetica-Oblique", 10)
            caption_width = canvas.stringWidth(grid.caption, "Helvetica-Oblique", 10)
            caption_x = x + (grid_width - caption_width) / 2
            canvas.drawString(caption_x, y - grid_height - 15, grid.caption)

        canvas.restoreState()

    def _draw_cell(self, canvas, cell: DiagramCell, x: float, y: float):
        """Draw a single cell based on its type."""
        if cell.cell_type == CellType.BLACK:
            self._draw_black_cell(canvas, x, y)
        elif cell.cell_type == CellType.CLUE:
            self._draw_clue_cell(
                canvas, x, y, cell.clue_across, cell.clue_down, cell.highlight
            )
        else:  # WHITE
            self._draw_white_cell(canvas, x, y, cell.value, cell.highlight)

    def _draw_black_cell(self, canvas, x: float, y: float):
        """Draw a solid navy blue cell."""
        canvas.setFillColor(self.NAVY_BLUE)
        canvas.setStrokeColor(self.NAVY_BLUE)
        canvas.setLineWidth(self.DEFAULT_LINE_WIDTH)
        canvas.rect(x, y, self.cell_size, self.cell_size, stroke=1, fill=1)

    def _draw_white_cell(
        self, canvas, x: float, y: float, value: str, highlight: HighlightStyle
    ):
        """Draw a white cell with optional value and highlight."""
        # Background color
        if highlight and highlight != HighlightStyle.NONE:
            bg_color = HexColor(HIGHLIGHT_COLORS[highlight])
        else:
            bg_color = white

        canvas.setFillColor(bg_color)
        canvas.setStrokeColor(black)
        canvas.setLineWidth(self.DEFAULT_LINE_WIDTH)
        canvas.rect(x, y, self.cell_size, self.cell_size, stroke=1, fill=1)

        # Draw value if present
        if value:
            canvas.setFillColor(black)
            font_size = self.cell_size * 0.5
            canvas.setFont(self.DEFAULT_FONT, font_size)
            text_width = canvas.stringWidth(value, self.DEFAULT_FONT, font_size)
            text_x = x + (self.cell_size - text_width) / 2
            text_y = y + (self.cell_size - font_size) / 2
            canvas.drawString(text_x, text_y, value)

    def _draw_clue_cell(
        self,
        canvas,
        x: float,
        y: float,
        h_clue: int,
        v_clue: int,
        highlight: HighlightStyle,
    ):
        """Draw a clue cell with diagonal split."""
        # Gray background
        gray = Color(0.816, 0.816, 0.816)
        canvas.setFillColor(gray)
        canvas.setStrokeColor(black)
        canvas.setLineWidth(self.DEFAULT_LINE_WIDTH)
        canvas.rect(x, y, self.cell_size, self.cell_size, stroke=1, fill=1)

        # Diagonal line
        canvas.setLineWidth(0.8)
        canvas.line(x, y + self.cell_size, x + self.cell_size, y)

        # Clue numbers
        canvas.setFillColor(black)
        clue_font_size = self.cell_size * 0.3
        canvas.setFont(self.DEFAULT_FONT, clue_font_size)

        if h_clue:
            text = str(h_clue)
            tw = canvas.stringWidth(text, self.DEFAULT_FONT, clue_font_size)
            tx = x + self.cell_size * 0.75 - tw / 2
            ty = y + self.cell_size * 0.75 - clue_font_size / 2
            canvas.drawString(tx, ty, text)

        if v_clue:
            text = str(v_clue)
            tw = canvas.stringWidth(text, self.DEFAULT_FONT, clue_font_size)
            tx = x + self.cell_size * 0.25 - tw / 2
            ty = y + self.cell_size * 0.25 - clue_font_size / 2
            canvas.drawString(tx, ty, text)

    def _draw_title(self, canvas, y):
        """Draw the diagram title centered at the top."""
        if not self.diagram.title:
            return

        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(black)

        text_width = canvas.stringWidth(self.diagram.title, "Helvetica-Bold", 14)
        x = (self.width - text_width) / 2
        canvas.drawString(x, y + 8, self.diagram.title)
        canvas.restoreState()

    def _draw_legend(self, canvas, y):
        """Draw the legend showing color meanings (stacked vertically)."""
        if not self.diagram.legend:
            return

        canvas.saveState()
        x = 20
        y_cursor = y
        line_height = 20  # Vertical spacing between items

        # Legend title
        if self.diagram.legend.title:
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x, y_cursor, self.diagram.legend.title)
            y_cursor -= line_height

        # Legend items - stacked vertically
        canvas.setFont("Helvetica", 9)
        for color_key, label in self.diagram.legend.items.items():
            # Draw color swatch
            try:
                color = HexColor(color_key)
            except ValueError:
                color = HexColor(HIGHLIGHT_COLORS.get(color_key, "#CCCCCC"))

            canvas.setFillColor(color)
            canvas.setStrokeColor(black)
            canvas.rect(x, y_cursor - 2, 15, 15, stroke=1, fill=1)

            # Draw label
            canvas.setFillColor(black)
            canvas.drawString(x + 22, y_cursor + 2, label)

            y_cursor -= line_height

        canvas.restoreState()

    def _draw_legend_at(self, canvas, x: float, y: float):
        """Draw the legend at a specific position (for right-side placement)."""
        if not self.diagram.legend:
            return

        canvas.saveState()
        y_cursor = y
        line_height = 20

        # Legend title
        if self.diagram.legend.title:
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x, y_cursor, self.diagram.legend.title)
            y_cursor -= line_height

        # Legend items
        canvas.setFont("Helvetica", 9)
        for color_key, label in self.diagram.legend.items.items():
            try:
                color = HexColor(color_key)
            except ValueError:
                color = HexColor(HIGHLIGHT_COLORS.get(color_key, "#CCCCCC"))

            canvas.setFillColor(color)
            canvas.setStrokeColor(black)
            canvas.rect(x, y_cursor - 2, 15, 15, stroke=1, fill=1)

            canvas.setFillColor(black)
            canvas.drawString(x + 22, y_cursor + 2, label)

            y_cursor -= line_height

        canvas.restoreState()

    def _draw_annotation_box(self, canvas, annotation: AnnotationBox, y):
        """Draw an annotation box with styled background."""
        canvas.saveState()

        style = ANNOTATION_STYLES.get(annotation.style, ANNOTATION_STYLES["info"])
        box_width = self.width - 40
        box_height = 40
        x = 20

        # Draw background
        canvas.setFillColor(HexColor(style["bg"]))
        canvas.setStrokeColor(HexColor(style["border"]))
        canvas.setLineWidth(1.5)
        canvas.roundRect(x, y - box_height, box_width, box_height, 5, stroke=1, fill=1)

        # Draw title if present
        text_y = y - 15
        if annotation.title:
            canvas.setFont("Helvetica-Bold", 10)
            canvas.setFillColor(HexColor(style["text"]))
            canvas.drawString(x + 10, text_y, annotation.title)
            text_y -= 15

        # Draw text
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(HexColor(style["text"]))
        canvas.drawString(x + 10, text_y, annotation.text)

        canvas.restoreState()

    def _draw_caption(self, canvas, y):
        """Draw the diagram caption at the bottom."""
        if not self.diagram.caption:
            return

        canvas.saveState()
        canvas.setFont("Helvetica-Oblique", 10)
        canvas.setFillColor(black)

        text_width = canvas.stringWidth(self.diagram.caption, "Helvetica-Oblique", 10)
        x = (self.width - text_width) / 2
        canvas.drawString(x, y, self.diagram.caption)
        canvas.restoreState()


def render_diagram(diagram: DiagramDefinition, max_width: float = 6.0 * inch) -> list:
    """Render a diagram definition to a list of flowables.

    Args:
        diagram: The diagram definition to render.
        max_width: Maximum width in points.

    Returns:
        List of flowables including the diagram and spacing.
    """
    from reportlab.platypus import Spacer, KeepTogether

    flowable = DiagramFlowable(diagram, max_width=max_width)
    return [Spacer(1, 16), KeepTogether([flowable]), Spacer(1, 8)]
