# Design: PDF Generation Module

## Context

The Kakuro project needs to generate print-ready PDF books for Amazon KDP publishing. ReportLab is the chosen library due to its professional-grade PDF generation capabilities, font embedding, and precise layout control.

## Goals / Non-Goals

### Goals
- Create a modular PDF generation system matching the puzzle generation architecture
- Render Kakuro grids with precise clue placement
- Support multiple page layouts and trim sizes
- Generate KDP-compliant PDF/X-1a output
- Enable batch book generation

### Non-Goals
- Cover generation (separate module later)
- EPUB/digital formats (future enhancement)
- Full book automation (Phase 2)

## Architecture

```
src/pdf_generation/
├── __init__.py          # Public API exports
├── models.py            # Data models (PageLayout, BookConfig, etc.)
├── renderer.py          # Grid rendering to PDF canvas
├── page_builder.py      # Page composition (puzzles, solutions)
├── document.py          # Multi-page document assembly
├── fonts.py             # Font loading and embedding
└── compliance.py        # PDF/X-1a compliance utilities
```

## Key Decisions

### Decision 1: ReportLab Canvas API (Low-Level)
- **What**: Use `reportlab.pdfgen.canvas` directly for grid rendering
- **Why**: Maximum control over positioning, line weights, and clue placement
- **Alternatives**: Platypus Flowables - rejected due to grid complexity

### Decision 2: Platypus for Document Assembly
- **What**: Use `reportlab.platypus` for multi-page documents
- **Why**: Built-in pagination, headers/footers, page templates
- **Trade-off**: Mixed approach requires careful integration

### Decision 3: Points as Internal Units
- **What**: Use points (1/72 inch) internally, inches for configuration
- **Why**: ReportLab native unit, precise positioning
- **Conversion**: `inches * 72 = points`

### Decision 4: Modular Rendering
- **What**: Separate grid rendering from page layout from document assembly
- **Why**: Testability, reusability, single responsibility
- **Pattern**: Similar to puzzle_generation module structure

## Data Models

```python
@dataclass
class PageLayout:
    width: float           # Page width in points
    height: float          # Page height in points
    margins: Margins       # Top, bottom, left, right, gutter
    cell_size: float       # Grid cell size in points
    puzzles_per_page: int  # 1 or 2

@dataclass  
class RenderConfig:
    line_width: float      # Grid line thickness
    clue_font_size: float  # Font size for clue numbers
    solution_font_size: float
    show_solution: bool    # True for solution pages

@dataclass
class BookConfig:
    title: str
    puzzles: list[Puzzle]
    layout: PageLayout
    render_config: RenderConfig
    include_instructions: bool
    include_solutions: bool
```

## Rendering Algorithm

### Grid Rendering
1. Calculate grid bounds from puzzle dimensions and cell_size
2. Draw outer border (thicker line)
3. Draw black cells as filled rectangles
4. Draw white cells with thin borders
5. For each clue cell, render diagonal split and clue numbers
6. For solution pages, render digit in each white cell

### Clue Cell Layout
```
+-------+
|\   B  |   A = horizontal clue (down-right)
|  \    |   B = vertical clue (up-right)
| A  \  |   Diagonal line from top-left to bottom-right
+-------+
```

## Risks / Trade-offs

### Risk: Font Embedding Complexity
- **Mitigation**: Use Liberation Sans (open-source, widely compatible)
- **Fallback**: Helvetica (built into ReportLab)

### Risk: PDF/X-1a Compliance
- **Mitigation**: Test with KDP Previewer early and often
- **Approach**: Start simple, add compliance features incrementally

### Risk: Large Book Performance
- **Mitigation**: Stream pages to disk, don't hold all in memory
- **Target**: Generate 500-puzzle book in <60 seconds

## Open Questions

1. Should instruction pages use a template or be generated dynamically?
2. What fonts should be bundled vs. expected to be installed?
3. Should we support CMYK color mode in initial version?

