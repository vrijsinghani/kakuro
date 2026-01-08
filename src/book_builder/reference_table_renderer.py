"""
Reference Table Flowable for non-grid diagrams like combination tables.

This renders nicely formatted tables with sections and cards,
suitable for reference content like "unique combinations" tables.
"""

from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor

from .diagram_models import ReferenceTableDefinition, CARD_COLORS


class ReferenceTableFlowable(Flowable):
    """A flowable that renders reference tables with combination cards."""

    # Styling constants
    TITLE_FONT_SIZE = 14
    SECTION_TITLE_FONT_SIZE = 11
    SUM_FONT_SIZE = 12
    COMBO_FONT_SIZE = 10
    CARD_WIDTH = 120
    CARD_HEIGHT = 45
    CARD_PADDING = 10
    SECTION_PADDING = 15
    BORDER_RADIUS = 8

    def __init__(self, table_def: ReferenceTableDefinition, max_width: float = 432):
        """Initialize the reference table flowable.

        Args:
            table_def: The reference table definition to render.
            max_width: Maximum width available for the table.
        """
        super().__init__()
        self.table = table_def
        self.max_width = max_width
        self._calculate_dimensions()

    def _calculate_dimensions(self):
        """Calculate total dimensions needed."""
        # Title height
        self.title_height = 35 if self.table.title else 0

        # Calculate section heights
        self.section_heights = []
        for section in self.table.sections:
            # Section title
            height = 25
            # Cards in rows
            num_rows = (len(section.cards) + section.columns - 1) // section.columns
            height += num_rows * (self.CARD_HEIGHT + self.CARD_PADDING)
            height += self.SECTION_PADDING
            self.section_heights.append(height)

        # Footer note
        self.footer_height = 25 if self.table.footer_note else 0

        # Content width - constrain to max_width with padding
        self.content_width = min(self.max_width - 40, 400)

        # Total dimensions
        self.width = self.max_width
        self.height = (
            self.title_height
            + sum(self.section_heights)
            + self.footer_height
            + 30  # Top/bottom padding
        )

    def wrap(self, available_width, available_height):
        """Return the size needed for this flowable."""
        return (self.width, self.height)

    def draw(self):
        """Draw the reference table."""
        canvas = self.canv
        y_cursor = self.height

        # Calculate centered x position
        start_x = (self.width - self.content_width) / 2

        # Draw outer border with rounded corners
        self._draw_outer_border(
            canvas, start_x, 10, self.content_width, self.height - 20
        )

        # Draw title
        if self.table.title:
            y_cursor -= 30
            self._draw_title(canvas, y_cursor)

        # Draw sections
        for section in self.table.sections:
            y_cursor = self._draw_section(canvas, section, start_x, y_cursor)

        # Draw footer note
        if self.table.footer_note:
            y_cursor -= 5
            self._draw_footer(canvas, start_x, y_cursor)

    def _draw_outer_border(self, canvas, x, y, width, height):
        """Draw the rounded border box with background."""
        bg_color = HexColor(self.table.background_color)
        border_color = HexColor(self.table.border_color)

        # Background fill
        canvas.setFillColor(bg_color)
        canvas.setStrokeColor(border_color)
        canvas.setLineWidth(2)
        canvas.roundRect(x, y, width, height, self.BORDER_RADIUS, stroke=1, fill=1)

    def _draw_title(self, canvas, y):
        """Draw the main title."""
        canvas.setFillColor(HexColor("#333333"))
        canvas.setFont("Helvetica-Bold", self.TITLE_FONT_SIZE)
        title_width = canvas.stringWidth(
            self.table.title, "Helvetica-Bold", self.TITLE_FONT_SIZE
        )
        x = (self.width - title_width) / 2
        canvas.drawString(x, y, self.table.title)

    def _draw_section(self, canvas, section, start_x, y_cursor):
        """Draw a section with title and cards."""
        # Section title
        y_cursor -= 22
        canvas.setFillColor(HexColor("#2E7D32"))  # Green
        canvas.setFont("Helvetica-Bold", self.SECTION_TITLE_FONT_SIZE)
        title_width = canvas.stringWidth(
            section.title, "Helvetica-Bold", self.SECTION_TITLE_FONT_SIZE
        )
        x = (self.width - title_width) / 2
        canvas.drawString(x, y_cursor, section.title)

        y_cursor -= 10

        # Draw cards in rows
        cards_per_row = section.columns
        card_total_width = cards_per_row * (self.CARD_WIDTH + self.CARD_PADDING)
        cards_start_x = (self.width - card_total_width) / 2

        for i, card in enumerate(section.cards):
            col = i % cards_per_row
            if i > 0 and col == 0:
                y_cursor -= self.CARD_HEIGHT + self.CARD_PADDING

            card_x = cards_start_x + col * (self.CARD_WIDTH + self.CARD_PADDING)
            self._draw_card(canvas, card, card_x, y_cursor - self.CARD_HEIGHT)

        y_cursor -= self.CARD_HEIGHT + self.SECTION_PADDING
        return y_cursor

    def _draw_card(self, canvas, card, x, y):
        """Draw a single combination card."""
        # White background for card
        canvas.setFillColor(HexColor("#FFFFFF"))
        canvas.setStrokeColor(HexColor("#E0E0E0"))
        canvas.setLineWidth(0.5)
        canvas.roundRect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT, 4, stroke=1, fill=1)

        # Get colors for this card
        colors = CARD_COLORS.get(card.color, CARD_COLORS["blue"])

        # Sum label
        sum_text = f"Sum: {card.sum_value}"
        canvas.setFillColor(HexColor(colors["sum"]))
        canvas.setFont("Helvetica-Bold", self.SUM_FONT_SIZE)
        sum_width = canvas.stringWidth(sum_text, "Helvetica-Bold", self.SUM_FONT_SIZE)
        sum_x = x + (self.CARD_WIDTH - sum_width) / 2
        canvas.drawString(sum_x, y + self.CARD_HEIGHT - 18, sum_text)

        # Combination
        canvas.setFillColor(HexColor(colors["combo"]))
        canvas.setFont("Helvetica", self.COMBO_FONT_SIZE)
        combo_width = canvas.stringWidth(
            card.combination, "Helvetica", self.COMBO_FONT_SIZE
        )
        combo_x = x + (self.CARD_WIDTH - combo_width) / 2
        canvas.drawString(combo_x, y + 10, card.combination)

    def _draw_footer(self, canvas, start_x, y):
        """Draw the footer note."""
        if not self.table.footer_note:
            return

        canvas.setFillColor(HexColor("#666666"))
        canvas.setFont("Helvetica-Oblique", 9)
        # Center the footer
        footer_width = canvas.stringWidth(
            self.table.footer_note, "Helvetica-Oblique", 9
        )
        x = (self.width - footer_width) / 2
        canvas.drawString(x, y, self.table.footer_note)
