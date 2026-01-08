"""
Chapter 2 diagram definitions: Essential Solving Techniques.

These diagrams teach elimination, cascade effects, starting strategies,
and troubleshooting for Kakuro puzzles.
"""

from ..diagram_models import (
    DiagramDefinition,
    DiagramGrid,
    DiagramCell,
    CellType,
    HighlightStyle,
    AnnotationBox,
    Legend,
    ReferenceTableDefinition,
    CombinationSection,
    CombinationCard,
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
# DIAGRAM 1: Unique Combinations Reference Table
# =============================================================================

DIAGRAM_1_COMBINATIONS = ReferenceTableDefinition(
    diagram_id="chapter2_diagram1",
    title="Unique Combinations Reference",
    sections=[
        CombinationSection(
            title="Two-Cell Unique Combinations",
            columns=2,
            cards=[
                CombinationCard(sum_value=3, combination="1 + 2", color="blue"),
                CombinationCard(sum_value=4, combination="1 + 3", color="blue"),
                CombinationCard(sum_value=16, combination="7 + 9", color="red"),
                CombinationCard(sum_value=17, combination="8 + 9", color="red"),
            ],
        ),
        CombinationSection(
            title="Three-Cell Unique Combinations",
            columns=2,
            cards=[
                CombinationCard(sum_value=6, combination="1 + 2 + 3", color="blue"),
                CombinationCard(sum_value=7, combination="1 + 2 + 4", color="blue"),
                CombinationCard(sum_value=23, combination="6 + 8 + 9", color="red"),
                CombinationCard(sum_value=24, combination="7 + 8 + 9", color="red"),
            ],
        ),
    ],
    footer_note="Green = memorize these. They give instant answers!",
)


# =============================================================================
# DIAGRAM 2a: Elimination Method - Setup & ACROSS Analysis
# Shows initial puzzle state and ACROSS possibilities
# =============================================================================

DIAGRAM_2A_ELIMINATION_SETUP = DiagramDefinition(
    diagram_id="chapter2_diagram2",
    title="Diagram 2a: Elimination Method — Setup",
    layout="horizontal",
    grids=[
        # Grid 1: Initial Puzzle State
        DiagramGrid(
            rows=4,
            cols=4,
            title="Initial State",
            cells=[
                _make_black_cell(0, 0),
                _make_black_cell(0, 1),
                _make_clue_cell(0, 2, down=9),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=15),
                _make_white_cell(1, 1, "?", HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, "?", HighlightStyle.PRIMARY),
                _make_white_cell(1, 3, "?", HighlightStyle.PRIMARY),
                _make_black_cell(2, 0),
                _make_black_cell(2, 1),
                _make_white_cell(2, 2, "?"),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_black_cell(3, 1),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
    ],
    legend=Legend(
        items={
            "#ADD8E6": "ACROSS run: 3 cells sum to 15",
        }
    ),
    annotations=[
        AnnotationBox(
            title="ACROSS 15 Possibilities",
            text="1+5+9, 1+6+8, 2+4+9, 2+5+8, 2+6+7, 3+4+8, 3+5+7, 4+5+6",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 2b: Elimination Method - DOWN Analysis & Solution
# =============================================================================

DIAGRAM_2B_ELIMINATION_SOLUTION = DiagramDefinition(
    diagram_id="chapter2_diagram3",
    title="Diagram 2b: Elimination Method — Solution",
    layout="horizontal",
    grids=[
        # Grid showing intersection analysis
        DiagramGrid(
            rows=4,
            cols=4,
            title="The Intersection",
            cells=[
                _make_black_cell(0, 0),
                _make_black_cell(0, 1),
                _make_clue_cell(0, 2, down=9),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=15),
                _make_white_cell(1, 1, "?", HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, "?", HighlightStyle.INCORRECT),  # Key cell
                _make_white_cell(1, 3, "?", HighlightStyle.PRIMARY),
                _make_black_cell(2, 0),
                _make_black_cell(2, 1),
                _make_white_cell(2, 2, "?", HighlightStyle.EMPHASIS),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_black_cell(3, 1),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
        # Grid showing the solution
        DiagramGrid(
            rows=4,
            cols=4,
            title="Solution",
            cells=[
                _make_black_cell(0, 0),
                _make_black_cell(0, 1),
                _make_clue_cell(0, 2, down=9),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=15),
                _make_white_cell(1, 1, "2", HighlightStyle.CORRECT),
                _make_white_cell(1, 2, "4", HighlightStyle.CORRECT),
                _make_white_cell(1, 3, "9", HighlightStyle.CORRECT),
                _make_black_cell(2, 0),
                _make_black_cell(2, 1),
                _make_white_cell(2, 2, "5", HighlightStyle.CORRECT),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_black_cell(3, 1),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
    ],
    legend=Legend(
        items={
            "#FFB6C1": "Key intersection cell",
            "#FFE4B5": "DOWN run: 2 cells sum to 9",
        }
    ),
    annotations=[
        AnnotationBox(
            title="Intersection = 4",
            text="ACROSS middle: 4,5,6 | DOWN top: 1,2,3,4 → Only 4 in both!",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM 3: The Cascade Effect
# =============================================================================

DIAGRAM_3_CASCADE = DiagramDefinition(
    diagram_id="chapter2_diagram4",
    title="Diagram 3: The Cascade Effect",
    layout="horizontal",
    grids=[
        # Before: One cell solved
        DiagramGrid(
            rows=4,
            cols=4,
            title="BEFORE: One Cell Solved",
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=17),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=7),
                _make_white_cell(1, 1),
                _make_white_cell(1, 2),
                _make_black_cell(1, 3),
                _make_clue_cell(2, 0, across=11),
                _make_white_cell(2, 1, "3", HighlightStyle.CORRECT),
                _make_white_cell(2, 2),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_black_cell(3, 1),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
        # After: Cascade unlocks more
        DiagramGrid(
            rows=4,
            cols=4,
            title="AFTER: Cascade Unlocks 3 More!",
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=17),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=7),
                _make_white_cell(1, 1, "1", HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, "6", HighlightStyle.PRIMARY),
                _make_black_cell(1, 3),
                _make_clue_cell(2, 0, across=11),
                _make_white_cell(2, 1, "3", HighlightStyle.CORRECT),
                _make_white_cell(2, 2, "8", HighlightStyle.PRIMARY),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_black_cell(3, 1),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
    ],
    legend=Legend(
        items={
            "#90EE90": "Starting digit (known)",
            "#ADD8E6": "Unlocked by cascade",
        }
    ),
    annotations=[
        AnnotationBox(
            text="The 3 forces: DOWN 4→1, ACROSS 7→1+6, ACROSS 11→3+8",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM 4: Identifying Good Starting Points
# =============================================================================

DIAGRAM_4_STARTING_POINTS = DiagramDefinition(
    diagram_id="chapter2_diagram5",
    title="Diagram 4: Identifying Good Starting Points",
    grids=[
        DiagramGrid(
            rows=4,
            cols=5,
            cells=[
                # Row 0
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=17),
                _make_clue_cell(0, 2, down=6),
                _make_black_cell(0, 3),
                _make_black_cell(0, 4),
                # Row 1
                _make_clue_cell(1, 0, across=12),
                _make_white_cell(1, 1, highlight=HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, highlight=HighlightStyle.CORRECT),
                _make_black_cell(1, 3),
                _make_black_cell(1, 4),
                # Row 2: with constrained intersections
                _make_clue_cell(2, 0, across=4),
                _make_white_cell(2, 1, highlight=HighlightStyle.PRIMARY),
                _make_white_cell(2, 2, highlight=HighlightStyle.CORRECT),
                _make_black_cell(2, 3),
                _make_black_cell(2, 4),
                # Row 3
                _make_black_cell(3, 0),
                _make_black_cell(3, 1),
                _make_clue_cell(3, 2, across=16),
                _make_white_cell(3, 3, highlight=HighlightStyle.EMPHASIS),
                _make_white_cell(3, 4, highlight=HighlightStyle.EMPHASIS),
            ],
        )
    ],
    legend=Legend(
        items={
            "#90EE90": "Unique combo (sum 6 = 1+2+3)",
            "#FFE4B5": "Unique combo (sum 16 = 7+9)",
            "#ADD8E6": "Short runs (easy to solve)",
        }
    ),
    annotations=[
        AnnotationBox(
            title="Solving Order",
            text="1. Unique combos 2. Short runs (blue) 3. Build outward",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 5a: Complex Intersection Analysis - Setting Up
# =============================================================================

DIAGRAM_5A_INTERSECTION_SETUP = DiagramDefinition(
    diagram_id="chapter2_diagram6",
    title="Diagram 5a: Analyzing Multiple Intersections — Setup",
    grids=[
        DiagramGrid(
            rows=3,
            cols=5,
            title="Write Pencil Marks",
            cells=[
                # Row 0: clue row
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=10),
                _make_clue_cell(0, 2, down=7),
                _make_clue_cell(0, 3, down=12),
                _make_black_cell(0, 4),
                # Row 1: ACROSS 15
                _make_clue_cell(1, 0, across=15),
                _make_white_cell(1, 1, "?", HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, "?", HighlightStyle.EMPHASIS),
                _make_white_cell(1, 3, "?", HighlightStyle.CORRECT),
                _make_black_cell(1, 4),
                # Row 2: ACROSS 14
                _make_clue_cell(2, 0, across=14),
                _make_white_cell(2, 1, "?", HighlightStyle.PRIMARY),
                _make_white_cell(2, 2, "?", HighlightStyle.EMPHASIS),
                _make_white_cell(2, 3, "?", HighlightStyle.CORRECT),
                _make_black_cell(2, 4),
            ],
        )
    ],
    legend=Legend(
        items={
            "#ADD8E6": "DOWN 10: 1+9, 2+8, 3+7, 4+6",
            "#FFE4B5": "DOWN 7: 1+6, 2+5, 3+4",
            "#90EE90": "DOWN 12: 3+9, 4+8, 5+7",
        }
    ),
    annotations=[
        AnnotationBox(
            text="Each cell must satisfy BOTH its across and down run constraints.",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 5b: Complex Intersection Analysis - The Solution
# =============================================================================

DIAGRAM_5B_INTERSECTION_SOLUTION = DiagramDefinition(
    diagram_id="chapter2_diagram7",
    title="Diagram 5b: Analyzing Multiple Intersections — Solution",
    grids=[
        DiagramGrid(
            rows=3,
            cols=5,
            title="The Solution",
            cells=[
                # Row 0: clue row
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=10),
                _make_clue_cell(0, 2, down=7),
                _make_clue_cell(0, 3, down=12),
                _make_black_cell(0, 4),
                # Row 1: ACROSS 15 = 4+2+9
                _make_clue_cell(1, 0, across=15),
                _make_white_cell(1, 1, "4", HighlightStyle.CORRECT),
                _make_white_cell(1, 2, "2", HighlightStyle.CORRECT),
                _make_white_cell(1, 3, "9", HighlightStyle.CORRECT),
                _make_black_cell(1, 4),
                # Row 2: ACROSS 14 = 6+5+3
                _make_clue_cell(2, 0, across=14),
                _make_white_cell(2, 1, "6", HighlightStyle.CORRECT),
                _make_white_cell(2, 2, "5", HighlightStyle.CORRECT),
                _make_white_cell(2, 3, "3", HighlightStyle.CORRECT),
                _make_black_cell(2, 4),
            ],
        )
    ],
    annotations=[
        AnnotationBox(
            title="Verification",
            text="ACROSS: 4+2+9=15✓, 6+5+3=14✓ | DOWN: 4+6=10✓, 2+5=7✓, 9+3=12✓",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM 6a: Troubleshooting - Repeated Digits
# =============================================================================

DIAGRAM_6A_REPEATED_DIGITS = DiagramDefinition(
    diagram_id="chapter2_diagram8",
    title="Diagram 6a: Troubleshooting — Repeated Digits",
    layout="horizontal",
    grids=[
        # With Error
        DiagramGrid(
            rows=4,
            cols=4,
            title="❌ WITH ERROR",
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=13),
                _make_clue_cell(0, 2, down=12),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=10),
                _make_white_cell(1, 1, "3", HighlightStyle.INCORRECT),
                _make_white_cell(1, 2, "3", HighlightStyle.INCORRECT),
                _make_black_cell(1, 3),
                _make_black_cell(2, 0),
                _make_white_cell(2, 1, "9"),
                _make_white_cell(2, 2, "8"),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_white_cell(3, 1, "1"),
                _make_white_cell(3, 2, "1"),
                _make_black_cell(3, 3),
            ],
        ),
        # Corrected
        DiagramGrid(
            rows=4,
            cols=4,
            title="✓ CORRECTED",
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=13),
                _make_clue_cell(0, 2, down=12),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=10),
                _make_white_cell(1, 1, "3", HighlightStyle.CORRECT),
                _make_white_cell(1, 2, "7", HighlightStyle.CORRECT),
                _make_black_cell(1, 3),
                _make_black_cell(2, 0),
                _make_white_cell(2, 1, "9"),
                _make_white_cell(2, 2, "4"),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_white_cell(3, 1, "1"),
                _make_white_cell(3, 2, "1"),
                _make_black_cell(3, 3),
            ],
        ),
    ],
    legend=Legend(
        items={
            "#FFB6C1": "Error: same digit twice in run",
            "#90EE90": "Fixed: all unique digits",
        }
    ),
    annotations=[
        AnnotationBox(
            text="Problem: 3+3=6≠10. Fix: Change to 3+7=10. DOWN 12: 7+4+1=12✓",
            style="error",
        )
    ],
)


# =============================================================================
# DIAGRAM 6b: Troubleshooting - Wrong Sums
# =============================================================================

DIAGRAM_6B_WRONG_SUMS = DiagramDefinition(
    diagram_id="chapter2_diagram9",
    title="Diagram 6b: Troubleshooting — Wrong Sums",
    layout="horizontal",
    grids=[
        # With Error
        DiagramGrid(
            rows=4,
            cols=4,
            title="❌ WITH ERROR",
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=12),
                _make_clue_cell(0, 2, down=11),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=7),
                _make_white_cell(1, 1, "2", HighlightStyle.INCORRECT),
                _make_white_cell(1, 2, "6", HighlightStyle.INCORRECT),
                _make_black_cell(1, 3),
                _make_black_cell(2, 0),
                _make_white_cell(2, 1, "8"),
                _make_white_cell(2, 2, "5"),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_white_cell(3, 1, "2"),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
        # Corrected
        DiagramGrid(
            rows=4,
            cols=4,
            title="✓ CORRECTED",
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=11),
                _make_clue_cell(0, 2, down=11),
                _make_black_cell(0, 3),
                _make_clue_cell(1, 0, across=7),
                _make_white_cell(1, 1, "1", HighlightStyle.CORRECT),
                _make_white_cell(1, 2, "6", HighlightStyle.CORRECT),
                _make_black_cell(1, 3),
                _make_black_cell(2, 0),
                _make_white_cell(2, 1, "8"),
                _make_white_cell(2, 2, "5"),
                _make_black_cell(2, 3),
                _make_black_cell(3, 0),
                _make_white_cell(3, 1, "2"),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        ),
    ],
    legend=Legend(
        items={
            "#FFB6C1": "Error: sum doesn't match",
            "#90EE90": "Fixed: 1+6=7✓",
        }
    ),
    annotations=[
        AnnotationBox(
            text="Problem: 2+6=8≠7. Fix: Change 2 to 1. ACROSS 7: 1+6=7✓",
            style="error",
        )
    ],
)


# =============================================================================
# DIAGRAM REGISTRY
# =============================================================================

CHAPTER2_DIAGRAMS = {
    "diagram_1": DIAGRAM_1_COMBINATIONS,
    "diagram_2": DIAGRAM_2A_ELIMINATION_SETUP,
    "diagram_3": DIAGRAM_2B_ELIMINATION_SOLUTION,
    "diagram_4": DIAGRAM_3_CASCADE,
    "diagram_5": DIAGRAM_4_STARTING_POINTS,
    "diagram_6": DIAGRAM_5A_INTERSECTION_SETUP,
    "diagram_7": DIAGRAM_5B_INTERSECTION_SOLUTION,
    "diagram_8": DIAGRAM_6A_REPEATED_DIGITS,
    "diagram_9": DIAGRAM_6B_WRONG_SUMS,
}


def get_chapter2_diagram(diagram_id: str):
    """Get a Chapter 2 diagram by ID.

    Args:
        diagram_id: The diagram identifier (e.g., "diagram_1")

    Returns:
        The diagram definition (DiagramDefinition or ReferenceTableDefinition).

    Raises:
        KeyError: If the diagram ID is not found.
    """
    return CHAPTER2_DIAGRAMS[diagram_id]
