# Diagram Renderer Specification

## ADDED Requirements

### Requirement: Programmatic Diagram Generation

The system SHALL generate instructional diagrams directly using ReportLab drawing primitives, eliminating the HTML→browser→screenshot→conversion pipeline.

#### Scenario: Kakuro grid diagram renders correctly
- **GIVEN** a diagram definition specifying a Kakuro grid with cells, clues, and highlights
- **WHEN** the diagram is rendered to PDF
- **THEN** the output is true vector graphics (not rasterized)
- **AND** text remains crisp at any zoom level
- **AND** the diagram scales to full page width

#### Scenario: Diagram with annotations renders correctly
- **GIVEN** a diagram definition with annotation boxes, legends, and callouts
- **WHEN** the diagram is rendered to PDF
- **THEN** all text is readable at print size (minimum 10pt effective)
- **AND** annotation boxes are properly positioned relative to the grid

#### Scenario: Side-by-side comparison diagram renders correctly
- **GIVEN** a diagram definition with two grids (e.g., CORRECT vs INCORRECT examples)
- **WHEN** the diagram is rendered to PDF
- **THEN** both grids appear side-by-side with proper spacing
- **AND** each grid has its own caption/annotation

---

### Requirement: Diagram Definition Format

The system SHALL support diagram definitions as Python data structures or YAML files, specifying:
- Grid dimensions and cell contents
- Cell styling (colors, highlights)
- Clue values and positions
- Annotations, legends, and callouts
- Layout options (side-by-side, stacked)

#### Scenario: Diagram defined in Python
- **GIVEN** a Python dict/dataclass defining diagram elements
- **WHEN** passed to DiagramRenderer.render()
- **THEN** a ReportLab Flowable is returned
- **AND** the flowable can be included in document assembly

#### Scenario: Diagram defined in YAML
- **GIVEN** a YAML file in `books/{book-id}/chapters/visuals/diagrams/`
- **WHEN** the chapter renderer encounters `![Diagram](path.yaml)`
- **THEN** the YAML is parsed and rendered as a vector diagram

---

### Requirement: Chapter 1 Diagram Definitions

The system SHALL provide diagram definitions for all Chapter 1 instructional diagrams:

1. **Diagram 1: Anatomy of a Kakuro Grid** - Grid components with labeled callouts
2. **Diagram 2: Understanding Across Runs** - Highlighted horizontal runs
3. **Diagram 3: Understanding Down Runs** - Highlighted vertical runs  
4. **Diagram 4: The No-Repetition Rule** - Side-by-side CORRECT/INCORRECT examples
5. **Diagram 5: Same Digit in Different Runs** - Intersection highlighting with legend
6. **Diagram 6: Complete Solved Example** - Full solved grid with annotations
7. **Diagram 7: Unique Combinations Reference** - Table/chart of common sums

#### Scenario: All Chapter 1 diagrams render without errors
- **GIVEN** the Chapter 1 markdown references diagrams 1-7
- **WHEN** the chapter is rendered to PDF
- **THEN** all diagrams render as vector graphics
- **AND** no fallback to raster images occurs
- **AND** all text is readable at 6"x9" print size

---

### Requirement: Consistent Styling

The system SHALL apply consistent styling across all diagrams:
- Cell size: configurable, default 0.5 inches
- Grid line weight: 2pt for outer border, 1pt for inner lines
- Font: matches book body font (Open Sans or configured font)
- Colors: consistent palette for highlights (defined in book.yaml or defaults)

#### Scenario: Diagram styling matches book theme
- **GIVEN** a book.yaml with custom color palette
- **WHEN** diagrams are rendered
- **THEN** highlight colors use the configured palette
- **AND** fonts match the book's configured fonts

---

### Requirement: No External Dependencies for Diagram Rendering

The system SHALL NOT require external tools for diagram generation:
- No browser automation (Playwright, Selenium)
- No HTML rendering
- No pdf2svg or similar conversion tools
- No ImageMagick or raster processing

#### Scenario: Diagram rendering works in minimal environment
- **GIVEN** a Python environment with only ReportLab and standard dependencies
- **WHEN** diagrams are rendered
- **THEN** rendering succeeds without external tool calls
- **AND** no subprocess invocations are required

