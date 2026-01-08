"""
Chapter 1 diagram definitions: What is Kakuro?.

These diagrams teach the basic structure and rules of Kakuro puzzles.
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
# DIAGRAM 1: Anatomy of a Kakuro Grid
# =============================================================================

DIAGRAM_1_ANATOMY = DiagramDefinition(
    diagram_id="chapter1_diagram1",
    title="Diagram 1: Anatomy of a Kakuro Grid",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                # Row 0: black, clue(down=8), clue(down=12)
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=8),
                _make_clue_cell(0, 2, down=12),
                # Row 1: clue(across=7), white, white
                _make_clue_cell(1, 0, across=7),
                _make_white_cell(1, 1),
                _make_white_cell(1, 2),
                # Row 2: clue(across=11), white, white
                _make_clue_cell(2, 0, across=11),
                _make_white_cell(2, 1),
                _make_white_cell(2, 2),
            ],
        )
    ],
    legend=Legend(
        items={
            "#FFFFFF": "White Cell: Fill with digits 1-9",
            "#D0D0D0": "Clue Cell: Contains target sums",
        }
    ),
    annotations=[
        AnnotationBox(
            title="How to Read Clues",
            text="Upper-right = ACROSS sum (→), Lower-left = DOWN sum (↓)",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 2: Understanding Across Runs (Horizontal)
# =============================================================================

DIAGRAM_2_ACROSS = DiagramDefinition(
    diagram_id="chapter1_diagram2",
    title="Diagram 2: Understanding Across Runs (Horizontal)",
    grids=[
        DiagramGrid(
            rows=4,
            cols=4,
            cells=[
                # Row 0: all black
                _make_black_cell(0, 0),
                _make_black_cell(0, 1),
                _make_black_cell(0, 2),
                _make_black_cell(0, 3),
                # Row 1: clue(23), 3 blue cells
                _make_clue_cell(1, 0, across=23),
                _make_white_cell(1, 1, highlight=HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, highlight=HighlightStyle.PRIMARY),
                _make_white_cell(1, 3, highlight=HighlightStyle.PRIMARY),
                # Row 2: clue(15), 2 yellow, black
                _make_clue_cell(2, 0, across=15),
                _make_white_cell(2, 1, highlight=HighlightStyle.EMPHASIS),
                _make_white_cell(2, 2, highlight=HighlightStyle.EMPHASIS),
                _make_black_cell(2, 3),
                # Row 3: clue(9), 2 green, black
                _make_clue_cell(3, 0, across=9),
                _make_white_cell(3, 1, highlight=HighlightStyle.CORRECT),
                _make_white_cell(3, 2, highlight=HighlightStyle.CORRECT),
                _make_black_cell(3, 3),
            ],
        )
    ],
    legend=Legend(
        items={
            "#ADD8E6": "BLUE: 3 cells sum to 23",
            "#FFE4B5": "YELLOW: 2 cells sum to 15",
            "#90EE90": "GREEN: 2 cells sum to 9",
        }
    ),
    annotations=[
        AnnotationBox(
            text="Across runs go HORIZONTALLY, starting after the clue cell.",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 3: Understanding Down Runs (Vertical)
# =============================================================================

DIAGRAM_3_DOWN = DiagramDefinition(
    diagram_id="chapter1_diagram3",
    title="Diagram 3: Understanding Down Runs (Vertical)",
    grids=[
        DiagramGrid(
            rows=4,
            cols=4,
            cells=[
                # Row 0: black, clue(down=16), clue(down=12), clue(down=7)
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=16),
                _make_clue_cell(0, 2, down=12),
                _make_clue_cell(0, 3, down=7),
                # Rows 1-3: clue, then colored vertical runs
                _make_clue_cell(1, 0, across=10),
                _make_white_cell(1, 1, highlight=HighlightStyle.PRIMARY),
                _make_white_cell(1, 2, highlight=HighlightStyle.EMPHASIS),
                _make_white_cell(1, 3, highlight=HighlightStyle.CORRECT),
                _make_clue_cell(2, 0, across=14),
                _make_white_cell(2, 1, highlight=HighlightStyle.PRIMARY),
                _make_white_cell(2, 2, highlight=HighlightStyle.EMPHASIS),
                _make_black_cell(2, 3),
                _make_clue_cell(3, 0, across=11),
                _make_white_cell(3, 1, highlight=HighlightStyle.PRIMARY),
                _make_black_cell(3, 2),
                _make_black_cell(3, 3),
            ],
        )
    ],
    legend=Legend(
        items={
            "#ADD8E6": "BLUE: 3 cells sum to 16",
            "#FFE4B5": "YELLOW: 2 cells sum to 12",
            "#90EE90": "GREEN: 1 cell = 7",
        }
    ),
    annotations=[
        AnnotationBox(
            text="Down runs go VERTICALLY, starting below the clue cell.",
            style="info",
        )
    ],
)


# =============================================================================
# DIAGRAM 4: The No-Repetition Rule (Side-by-side comparison)
# =============================================================================

DIAGRAM_4_NO_REPETITION = DiagramDefinition(
    diagram_id="chapter1_diagram4",
    title="Diagram 4: The No-Repetition Rule",
    layout="horizontal",
    grids=[
        # CORRECT example
        DiagramGrid(
            rows=2,
            cols=3,
            title="✓ CORRECT",
            cells=[
                _make_clue_cell(0, 0, down=6),
                _make_clue_cell(0, 1, down=8),
                _make_clue_cell(0, 2, down=7),
                _make_white_cell(1, 0, "1", HighlightStyle.CORRECT),
                _make_white_cell(1, 1, "2", HighlightStyle.CORRECT),
                _make_white_cell(1, 2, "3", HighlightStyle.CORRECT),
            ],
        ),
        # INCORRECT example
        DiagramGrid(
            rows=2,
            cols=3,
            title="✗ INCORRECT",
            cells=[
                _make_clue_cell(0, 0, down=6),
                _make_clue_cell(0, 1, down=8),
                _make_clue_cell(0, 2, down=7),
                _make_white_cell(1, 0, "2", HighlightStyle.INCORRECT),
                _make_white_cell(1, 1, "2", HighlightStyle.INCORRECT),
                _make_white_cell(1, 2, "2", HighlightStyle.INCORRECT),
            ],
        ),
    ],
    legend=Legend(
        items={
            "#c6efce": "Unique digits (valid)",
            "#ffc7ce": "Repeated digit (invalid)",
        }
    ),
    caption="Each digit can only appear ONCE within a single run.",
)


# =============================================================================
# DIAGRAM 5: Same Digit Can Appear in Different Runs
# =============================================================================

DIAGRAM_5_DIFFERENT_RUNS = DiagramDefinition(
    diagram_id="chapter1_diagram5",
    title="Diagram 5: Same Digit Can Appear in Different Runs",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=17),
                _make_clue_cell(0, 2, down=16),
                _make_clue_cell(1, 0, across=17),
                _make_white_cell(1, 1, "9", HighlightStyle.EMPHASIS),
                _make_white_cell(1, 2, "8"),
                _make_clue_cell(2, 0, across=16),
                _make_white_cell(2, 1, "8"),
                _make_white_cell(2, 2, "8"),  # Different run, same digit OK
            ],
        )
    ],
    legend=Legend(
        title="Notice the digit 9:",
        items={
            "#FFE4B5": "The 9 appears in both runs but they are DIFFERENT runs",
        },
    ),
    annotations=[
        AnnotationBox(
            text="Same digit CAN appear in different runs - not twice in SAME run.",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM 6: Complete Solved Example
# =============================================================================

DIAGRAM_6_SOLVED = DiagramDefinition(
    diagram_id="chapter1_diagram6",
    title="Diagram 6: A Complete Solved Example",
    grids=[
        DiagramGrid(
            rows=3,
            cols=3,
            cells=[
                _make_black_cell(0, 0),
                _make_clue_cell(0, 1, down=4),
                _make_clue_cell(0, 2, down=6),
                _make_clue_cell(1, 0, across=3),
                _make_white_cell(1, 1, "1"),
                _make_white_cell(1, 2, "2"),
                _make_clue_cell(2, 0, across=7),
                _make_white_cell(2, 1, "3"),
                _make_white_cell(2, 2, "4"),
            ],
        )
    ],
    annotations=[
        AnnotationBox(
            title="Verify the solution:",
            text="Row 1: 1+2=3 ✓ | Row 2: 3+4=7 ✓ | Col 1: 1+3=4 ✓ | Col 2: 2+4=6 ✓",
            style="success",
        )
    ],
)


# =============================================================================
# DIAGRAM 7: Common Unique Combinations (Reference Table)
# =============================================================================

DIAGRAM_7_COMBINATIONS = ReferenceTableDefinition(
    diagram_id="chapter1_diagram7",
    title="Common Unique Combinations",
    sections=[
        CombinationSection(
            title="Two-Cell Runs with Only ONE Possible Combination",
            columns=2,
            cards=[
                CombinationCard(sum_value=3, combination="1 + 2", color="blue"),
                CombinationCard(sum_value=4, combination="1 + 3", color="blue"),
                CombinationCard(sum_value=16, combination="7 + 9", color="red"),
                CombinationCard(sum_value=17, combination="8 + 9", color="red"),
            ],
        ),
        CombinationSection(
            title="Three-Cell Runs with Only ONE Possible Combination",
            columns=2,
            cards=[
                CombinationCard(sum_value=6, combination="1 + 2 + 3", color="blue"),
                CombinationCard(sum_value=7, combination="1 + 2 + 4", color="blue"),
                CombinationCard(sum_value=23, combination="6 + 8 + 9", color="red"),
                CombinationCard(sum_value=24, combination="7 + 8 + 9", color="red"),
            ],
        ),
    ],
)


# =============================================================================
# DIAGRAM REGISTRY
# =============================================================================

CHAPTER1_DIAGRAMS = {
    "diagram_1": DIAGRAM_1_ANATOMY,
    "diagram_2": DIAGRAM_2_ACROSS,
    "diagram_3": DIAGRAM_3_DOWN,
    "diagram_4": DIAGRAM_4_NO_REPETITION,
    "diagram_5": DIAGRAM_5_DIFFERENT_RUNS,
    "diagram_6": DIAGRAM_6_SOLVED,
    "diagram_7": DIAGRAM_7_COMBINATIONS,
}


def get_chapter1_diagram(diagram_id: str):
    """Get a Chapter 1 diagram by ID.

    Args:
        diagram_id: The diagram identifier (e.g., "diagram_1")

    Returns:
        The diagram definition (DiagramDefinition or ReferenceTableDefinition).

    Raises:
        KeyError: If the diagram ID is not found.
    """
    return CHAPTER1_DIAGRAMS[diagram_id]
