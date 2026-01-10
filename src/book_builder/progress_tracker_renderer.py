"""
Progress Tracker Flowable for the Kakuro book.

This renders a specific progress tracking table for the user to fill out.
"""

from reportlab.platypus import Flowable
from reportlab.lib.colors import black, HexColor
from .config import DEFAULT_FONTS


class ProgressTrackerFlowable(Flowable):
    """A flowable that renders the Kakuro Progress Tracker table."""

    # Constants
    ROW_HEIGHT = 20
    HEADER_HEIGHT = 25
    TABLE_WIDTH = 450
    COL_WIDTHS = [60, 80, 80, 80, 150]  # Puzzle #, Date, Time, Difficulty, Notes
    HEADERS = ["Puzzle #", "Date", "Time", "Difficulty", "Notes"]

    # Rows to track (milestones)
    MILESTONES = [1, 5, 10, 20, 25, 30, 40, 50, 60, 70]

    def __init__(self, width=450):
        """Initialize progress tracker with specified width."""
        super().__init__()
        self.width = width
        self.height = self._calculate_height()

    def _calculate_height(self):
        """Calculate total height needed."""
        table_height = self.HEADER_HEIGHT + (len(self.MILESTONES) * self.ROW_HEIGHT)
        padding = 40
        personal_best_height = 80
        return table_height + padding + personal_best_height

    def wrap(self, available_width, available_height):
        """Return required dimensions for this flowable."""
        return (self.width, self.height)

    def draw(self):
        """Render the progress tracker table on the canvas."""
        canvas = self.canv
        # Center the table
        x = (self.width - sum(self.COL_WIDTHS)) / 2
        y = self.height

        # Draw Table Header
        y -= self.HEADER_HEIGHT
        self._draw_row(canvas, x, y, self.HEADERS, is_header=True)

        # Draw Table Rows
        for milestone in self.MILESTONES:
            y -= self.ROW_HEIGHT
            row_data = [str(milestone), "", "", "", ""]
            self._draw_row(canvas, x, y, row_data)

        # Draw Personal Best Section
        y -= 40  # Padding
        self._draw_personal_best(canvas, x, y)

    def _draw_row(self, canvas, start_x, y, data, is_header=False):
        """Draw a single row of the table."""
        current_x = start_x

        # Background for header
        if is_header:
            canvas.setFillColor(HexColor("#E0E0E0"))
            canvas.rect(
                start_x, y, sum(self.COL_WIDTHS), self.HEADER_HEIGHT, fill=1, stroke=0
            )
            canvas.setFillColor(black)
            canvas.setFont(DEFAULT_FONTS["heading"], 10)
        else:
            canvas.setFillColor(black)
            canvas.setFont(DEFAULT_FONTS["body"], 10)

        for i, text in enumerate(data):
            width = self.COL_WIDTHS[i]

            # Draw cell border
            canvas.setStrokeColor(black)
            canvas.setLineWidth(0.5)
            canvas.rect(
                current_x,
                y,
                width,
                self.ROW_HEIGHT if not is_header else self.HEADER_HEIGHT,
                fill=0,
                stroke=1,
            )

            # Draw text (centered)
            if text:
                text_width = canvas.stringWidth(
                    text,
                    DEFAULT_FONTS["heading"] if is_header else DEFAULT_FONTS["body"],
                    10,
                )
                text_x = current_x + (width - text_width) / 2
                text_y = y + 6 if not is_header else y + 8
                canvas.drawString(text_x, text_y, text)

            current_x += width

    def _draw_personal_best(self, canvas, x, y):
        """Draw the Personal Best section."""
        canvas.setFont(DEFAULT_FONTS["heading"], 12)
        canvas.drawString(x, y, "Personal Best:")

        y -= 20
        canvas.setFont(DEFAULT_FONTS["body"], 10)

        grids = ["6x6 Grid", "7x7 Grid", "8x8 Grid"]
        for grid in grids:
            canvas.drawString(x + 20, y, f"{grid}:")
            # Draw underline for user entry
            canvas.line(x + 100, y, x + 250, y)
            y -= 20
