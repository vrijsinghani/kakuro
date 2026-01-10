# PDF Generation Capability

## ADDED Requirements

### Requirement: Grid Rendering

The system SHALL render a Kakuro puzzle grid to a PDF canvas with the following elements:
- Black cells filled with solid color
- White cells with visible borders
- Clue cells with diagonal split and clue numbers positioned correctly
- Consistent cell sizing based on configuration

#### Scenario: Render puzzle grid

- **WHEN** a Puzzle object is passed to the grid renderer
- **THEN** the grid is drawn on the PDF canvas with correct dimensions
- **AND** all black cells are filled
- **AND** all clue numbers are positioned in the correct quadrant

#### Scenario: Render solution grid

- **WHEN** a solved Puzzle is rendered with show_solution=True
- **THEN** the solution digits are displayed in each white cell
- **AND** the grid structure remains identical to the puzzle grid

### Requirement: Page Layout

The system SHALL support configurable page layouts for puzzle rendering:
- Standard layout: 8.5" x 11" with 2 puzzles per page
- Large-print layout: 8.5" x 11" with 1 puzzle per page
- Configurable margins (top, bottom, left, right, gutter)
- Configurable cell sizes

#### Scenario: Standard layout with two puzzles

- **WHEN** a page is created with standard layout
- **THEN** two puzzles are positioned on the page
- **AND** each puzzle fits within the available space with proper margins

#### Scenario: Large-print layout

- **WHEN** a page is created with large-print layout
- **THEN** one puzzle is centered on the page
- **AND** the cell size is increased for readability

### Requirement: Document Assembly

The system SHALL assemble multiple puzzle pages into a complete PDF document:
- Sequential puzzle pages
- Solution section at the end
- Page numbering
- Consistent formatting throughout

#### Scenario: Create multi-page book

- **WHEN** 10 puzzles are passed to the document builder
- **THEN** a PDF is generated with puzzle pages followed by solution pages
- **AND** pages are numbered correctly

#### Scenario: Save document to file

- **WHEN** the document save() method is called with a file path
- **THEN** a valid PDF file is written to the specified location
- **AND** the file can be opened in standard PDF readers

### Requirement: Font Management

The system SHALL embed fonts in generated PDFs:
- Support custom font files from assets/fonts/
- Fallback to built-in fonts if custom fonts unavailable
- All text rendered with embedded fonts for consistent display

#### Scenario: Use custom font

- **WHEN** a font file exists in assets/fonts/
- **THEN** the font is embedded in the PDF
- **AND** clue numbers and text use the custom font

#### Scenario: Fallback to built-in font

- **WHEN** no custom font files are available
- **THEN** the system uses built-in Helvetica font
- **AND** the PDF generates successfully without errors

### Requirement: Clue Cell Rendering

The system SHALL render clue cells with proper formatting:
- Diagonal line from top-left to bottom-right corner
- Horizontal clue number in bottom-left triangle
- Vertical clue number in top-right triangle
- Clue numbers sized appropriately for cell dimensions

#### Scenario: Render clue with both directions

- **WHEN** a clue cell has both horizontal and vertical clues
- **THEN** both numbers are displayed in their respective positions
- **AND** neither number overlaps the diagonal line

#### Scenario: Render clue with single direction

- **WHEN** a clue cell has only a horizontal or vertical clue
- **THEN** only that clue number is displayed
- **AND** the empty quadrant remains blank

