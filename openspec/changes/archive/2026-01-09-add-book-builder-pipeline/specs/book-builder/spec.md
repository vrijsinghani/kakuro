# Book Builder Specification

## ADDED Requirements

### Requirement: Book Configuration

The system SHALL support YAML-based book configuration files that define:
- Book metadata (title, subtitle, author, ISBN)
- Content structure (front matter, chapters, puzzle sections, back matter)
- Layout settings (page size, margins, fonts, large print options)
- Puzzle specifications (difficulty levels, counts, grid sizes)

#### Scenario: Valid book configuration loads successfully
- **GIVEN** a valid `book.yaml` file exists at `books/{book-id}/book.yaml`
- **WHEN** the configuration is loaded
- **THEN** all fields are parsed and validated
- **AND** the configuration object is returned

#### Scenario: Invalid configuration reports errors
- **GIVEN** a `book.yaml` file with missing required fields
- **WHEN** the configuration is loaded
- **THEN** a validation error is raised with specific field details

---

### Requirement: Chapter Rendering

The system SHALL render markdown chapter files to PDF pages using ReportLab, supporting:
- Headings (h1, h2, h3) with appropriate styling
- Paragraphs with proper line spacing
- Bullet and numbered lists
- Bold and italic text
- Embedded images via markdown syntax `![alt](path)`
- Horizontal rules as section dividers

#### Scenario: Chapter with diagrams renders correctly
- **GIVEN** a markdown chapter file with `![Diagram](visuals/diagrams/chapter1/diagram_1.png)`
- **WHEN** the chapter is rendered to PDF
- **THEN** the image appears at the referenced location
- **AND** the image is sized appropriately for the page

#### Scenario: Large print mode increases readability
- **GIVEN** a book configuration with `layout.large_print: true`
- **WHEN** chapters are rendered
- **THEN** body text uses minimum 14pt font
- **AND** line spacing is increased for readability

---

### Requirement: Book Assembly

The system SHALL assemble complete PDF books by combining:
1. Front matter (title page, copyright, table of contents)
2. Instructional chapters (rendered from markdown)
3. Puzzle sections (generated and rendered puzzles)
4. Solutions section (compact grid layout)
5. Back matter (about author, other books, notes pages)

#### Scenario: Complete book builds successfully
- **GIVEN** a valid book configuration
- **AND** all referenced chapter files exist
- **WHEN** the build command is executed
- **THEN** a complete PDF is generated at `books/{book-id}/output/interior.pdf`
- **AND** the PDF contains all sections in order

#### Scenario: Table of contents has correct page numbers
- **GIVEN** a book with multiple chapters and puzzle sections
- **WHEN** the book is built
- **THEN** the table of contents lists all sections
- **AND** page numbers match actual content locations

---

### Requirement: Puzzle Generation Integration

The system SHALL integrate with the puzzle generation module to:
- Generate puzzles according to book configuration specs
- Cache generated puzzles to avoid regeneration on rebuild
- Support multiple difficulty levels within a single book

#### Scenario: Puzzles generated per configuration
- **GIVEN** a puzzle section config with `difficulty: beginner, count: 70, grid_sizes: [6, 7, 8]`
- **WHEN** the book is built
- **THEN** 70 beginner puzzles are generated with grid sizes 6x6, 7x7, and 8x8
- **AND** puzzles are distributed across the specified sizes

#### Scenario: Cached puzzles are reused
- **GIVEN** a book was previously built with puzzles
- **AND** the puzzle configuration has not changed
- **WHEN** the book is rebuilt
- **THEN** cached puzzles are loaded instead of regenerated

---

### Requirement: Build CLI

The system SHALL provide a command-line interface for building books:
- `python -m book_builder build <book-id>` — Build complete book
- `--chapters-only` — Build only chapter content (skip puzzles)
- `--puzzles-only` — Build only puzzle pages (skip chapters)
- `--output <path>` — Custom output path

#### Scenario: Build command produces PDF
- **GIVEN** a valid book configuration at `books/beginner-to-expert-250/book.yaml`
- **WHEN** `python -m book_builder build beginner-to-expert-250` is executed
- **THEN** the build process completes
- **AND** `books/beginner-to-expert-250/output/interior.pdf` is created

#### Scenario: Chapters-only build skips puzzle generation
- **GIVEN** a valid book configuration
- **WHEN** `python -m book_builder build <book-id> --chapters-only` is executed
- **THEN** only front matter and chapters are rendered
- **AND** puzzle generation is skipped
- **AND** the build completes faster

---

### Requirement: Multi-Book Support

The system SHALL support multiple independent book projects, each with:
- Its own directory under `books/{book-id}/`
- Its own configuration, chapters, and visuals
- Its own output directory for generated artifacts

#### Scenario: Different books have isolated content
- **GIVEN** two book projects: `books/beginner-250/` and `books/easy-kakuro-200/`
- **WHEN** each book is built
- **THEN** each produces its own PDF in its respective output directory
- **AND** content from one book does not affect the other

