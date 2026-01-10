"""
Chapter 3 diagram definitions: First Puzzle Walkthrough.

These diagrams take the reader through a step-by-step solution of a small Kakuro grid.
"""

from ..diagram_models import (
    DiagramDefinition,
    DiagramGrid,
    DiagramCell,
    CellType,
    HighlightStyle,
    AnnotationBox,
    Legend,
    Callout,
)


def _make_black_cell(row: int, col: int) -> DiagramCell:
    """Create a solid black cell."""
    return DiagramCell(row=row, col=col, cell_type=CellType.BLACK)


def _make_clue_cell(
    row: int, col: int, across: int = None, down: int = None
) -> DiagramCell:
    """Create a clue cell with diagonal split."""
    return DiagramCell(
        row=row,
        col=col,
        cell_type=CellType.CLUE,
        clue_across=across,
        clue_down=down,
    )


def _make_white_cell(
    row: int, col: int, value: str = None, highlight: HighlightStyle = None
) -> DiagramCell:
    """Create a white cell with optional value and highlight."""
    return DiagramCell(
        row=row,
        col=col,
        cell_type=CellType.WHITE,
        value=value,
        highlight=highlight or HighlightStyle.NONE,
    )


# =============================================================================
# The Walkthrough Grid Configuration
# =============================================================================
# 4x4 Grid (actually 3x3 playable area)
#
#       C1(4) C2(14)
#     +-----+------+
# R1  |  .  |  .   | (Sum 11)
# (11) +-----+------+
# R2  |  .  |  .   | (Sum 7)
# (7) +-----+------+
#
# Solution:
# R1: 3, 8
# R2: 1, 6
# C1: 3, 1 -> Sum 4
# C2: 8, 6 -> Sum 14


# =============================================================================
# DIAGRAM 1: Step 1 - Analyzing Clues (Unique Combinations)
# =============================================================================

DIAGRAM_1_ANALYSIS = DiagramDefinition(
    diagram_id="chapter3_diagram1",
    title="Step 1: Identifying Unique Combinations",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                # Row 0: Black, C1(4), C2(14)
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=14),
                # Row 1: R1(11), ., .
                _make_clue_cell(1, 0, across=11),
                _make_white_cell(1, 1),
                _make_white_cell(1, 2),
                # Row 2: R2(7), ., .
                _make_clue_cell(2, 0, across=7),
                _make_white_cell(2, 1),
                _make_white_cell(2, 2),
            ],
        )
    ],
    callouts=[
        Callout(
            text="Only 1+3 possible here!",
            target_row=0,
            target_col=1,
            position="above",
        )
    ],
    legend=Legend(
        title="Clue Analysis:",
        items={
            "#D0D0D0": "Focus on the 4: It must be 1+3",
        },
    ),
    annotations=[
        AnnotationBox(
            title="Look for Small Sums",
            text="The vertical sum of 4 has only one combination: 1 and 3. "
            "We don't know the order yet, but we know those two digits "
            "MUST go there.",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 2: Step 2 - Elimination
# =============================================================================

DIAGRAM_2_ELIMINATION = DiagramDefinition(
    diagram_id="chapter3_diagram2",
    title="Step 2: Using Elimination",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=14),
                # Row 1: Highlight Intersection
                _make_clue_cell(1, 0, across=11),
                _make_white_cell(1, 1, value="3", highlight=HighlightStyle.CORRECT),
                _make_white_cell(1, 2),
                _make_clue_cell(2, 0, across=7),
                _make_white_cell(2, 1),  # This will be 1 later
                _make_white_cell(2, 2),
            ],
        )
    ],
    callouts=[
        Callout(
            text="Can't be 1 (1+10=11 impossible)",
            target_row=1,
            target_col=1,
            position="left",
        )
    ],
    legend=Legend(
        title="Elimination Logic:",
        items={
            "#90EE90": "Must be 3 because 1 doesn't work for the 11-sum",
        },
    ),
    annotations=[
        AnnotationBox(
            title="Checking the Intersection",
            text="The top-left cell is part of the 11-row. If we put '1' "
            "there, the other cell would need to be 10 (11-1), which is "
            "impossible (max 9). So it MUST be '3'.",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM 3: Step 3 - Solving Intersections
# =============================================================================

DIAGRAM_3_INTERSECTIONS = DiagramDefinition(
    diagram_id="chapter3_diagram3",
    title="Step 3: Completing Intersections",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=14),
                # Row 1
                _make_clue_cell(1, 0, across=11),
                _make_white_cell(1, 1, value="3"),
                _make_white_cell(1, 2, value="8", highlight=HighlightStyle.PRIMARY),
                # Row 2
                _make_clue_cell(2, 0, across=7),
                _make_white_cell(2, 1, value="1", highlight=HighlightStyle.PRIMARY),
                _make_white_cell(2, 2),
            ],
        )
    ],
    annotations=[
        AnnotationBox(
            title="Filling the Gaps",
            text="Now that we have '3':\n• Vertical: 4 - 3 = 1\n"
            "• Horizontal: 11 - 3 = 8",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 4: Complete
# =============================================================================

DIAGRAM_4_COMPLETE = DiagramDefinition(
    diagram_id="chapter3_diagram4",
    title="Step 4: The Final Cell",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=14),
                # Row 1
                _make_clue_cell(1, 0, across=11),
                _make_white_cell(1, 1, value="3"),
                _make_white_cell(1, 2, value="8"),
                # Row 2
                _make_clue_cell(2, 0, across=7),
                _make_white_cell(2, 1, value="1"),
                _make_white_cell(2, 2, value="6", highlight=HighlightStyle.CORRECT),
            ],
        )
    ],
    legend=Legend(
        title="Verification:",
        items={
            "#90EE90": "6 fits both Row (1+6=7) and Col (8+6=14)",
        },
    ),
    annotations=[
        AnnotationBox(
            title="Puzzle Solved!",
            text="The last cell is '6'. Check the math:\n"
            "Row 2: 1 + 6 = 7 ✓\nColumn 2: 8 + 6 = 14 ✓",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM REGISTRY
# =============================================================================

CHAPTER3_DIAGRAMS = {
    "diagram_1": DIAGRAM_1_ANALYSIS,
    "diagram_2": DIAGRAM_2_ELIMINATION,
    "diagram_3": DIAGRAM_3_INTERSECTIONS,
    "diagram_4": DIAGRAM_4_COMPLETE,
}
