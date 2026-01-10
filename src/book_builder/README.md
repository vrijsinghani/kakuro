# Book Builder Module

This module (`src.book_builder`) provides a pipeline for generating professional-quality Kakuro puzzle books in PDF format, ready for Amazon KDP publishing.

## Features

- **Automated Assembly**: Combines front matter, chapters, puzzle sections, and back matter into a single PDF.
- **Markdown Support**: Renders chapters from Markdown files with support for headings, bold/italic text, lists, and images.
- **Programmatic Diagrams**: Renders vector-based diagrams directly using ReportLab (no external image files needed).
- **Dynamic Layout**: Handles page numbering, headers, footers, and large-print formatting.
- **Configuration Driven**: Entire book structure defined in a simple `book.yaml` file.

## Usage

Run the builder as a module:

```bash
python -m src.book_builder [command] [arguments]
```

### Commands

#### 1. Build a Book (`build`)

Builds the PDF for a specific book configuration.

```bash
# Build the full book (chapters + puzzles)
python -m src.book_builder build beginner-to-expert-250

# Build with verbose output (useful for debugging)
python -m src.book_builder -v build beginner-to-expert-250

# Build only the text chapters (fast, skips puzzle generation)
python -m src.book_builder build beginner-to-expert-250 --chapters-only

# Build only the puzzle pages (skips chapters)
python -m src.book_builder build beginner-to-expert-250 --puzzles-only

# Save output to a specific file
python -m src.book_builder build beginner-to-expert-250 --output my-book.pdf
```

#### 2. List Available Books (`list`)

Shows all valid book configurations found in the `books/` directory.

```bash
python -m src.book_builder list
```

#### 3. Validate Configuration (`validate`)

Checks `book.yaml` for errors and ensures all referenced files exist.

```bash
python -m src.book_builder validate beginner-to-expert-250
```

## Configuration (`book.yaml`)

Each book lives in its own directory under `books/` (e.g., `books/my-book/`). The `book.yaml` file defines the structure.

### Configuration Schema

| Section | Field | Type | Description |
|---------|-------|------|-------------|
| **metadata** | `title` | string | Book title (required) |
| | `subtitle` | string | Book subtitle (optional) |
| | `author` | string | Author name |
| | `isbn` | string | ISBN-13 (optional) |
| **content** | `front_matter` | list | List of `{type: title_page|copyright|toc}` |
| | `chapters` | list | List of `{path: str, title: str}` |
| | `puzzle_sections` | list | See below |
| | `back_matter` | list | List of `{type: solutions|about_author|notes, path: str}` |
| **puzzle_sections** | `title` | string | Section title (e.g., "Part 1: Beginner") |
| | `difficulty` | enum | `beginner`, `intermediate`, or `expert` |
| | `count` | int | Number of puzzles to generate |
| | `grid_sizes` | list[int] | List of grid sizes to randomly select from (e.g., `[9, 10]`) |
| **layout** | `page_size` | string | `letter` or `a4` (default: letter) |
| | `large_print` | bool | If true, uses larger fonts and 1 puzzle/page |
| | `puzzles_per_page` | int | Puzzles per page (1, 2, or 4) |
| | `margins` | object | `{top, bottom, left, right}` in inches |

## Guide: Creating a New Book

Follow these steps to create a distinct puzzle book.

### 1. Create Directory Structure
Create a new folder in `books/` using a unique ID (kebab-case).

```bash
mkdir -p books/my-new-book/chapters
```

### 2. Create Configuration
Create `books/my-new-book/book.yaml`:

```yaml
metadata:
  title: "My New Puzzle Book"
  author: "Me"

content:
  front_matter:
    - type: title_page
    - type: toc
  puzzle_sections:
    - title: "Warm Up"
      difficulty: beginner
      count: 20
      grid_sizes: [6, 7]
  back_matter:
    - type: solutions

layout:
  large_print: true
```

### 3. Add Chapters (Optional)
If your book includes tutorial chapters, add Markdown files to `books/my-new-book/chapters/`.

**`books/my-new-book/chapters/intro.md`**:
```markdown
# Introduction

Welcome to Kakuro! The rules are simple...
```

Register it in `book.yaml`:
```yaml
content:
  chapters:
    - path: chapters/intro.md
      title: "Introduction"
```

### 4. Build and Verify
Run the builder to generate the PDF.

```bash
python -m src.book_builder build my-new-book
```

The output will be saved to `books/my-new-book/output/interior.pdf`.

## Architecture

The pipeline consists of several key components:

1.  **`config.py`**: Parses `book.yaml` and validates data models using Pydantic.
2.  **`document.py`**: Manages the high-level `PDFDocument` (ReportLab canvas and templates).
3.  **`chapter_renderer.py`**: Parses Markdown chapters and renders text/diagrams using ReportLab flowables.
4.  **`diagram_renderer.py`**: Programmically draws vector grid diagrams for tutorial chapters.
5.  **`puzzle_flowable.py`**: Renders individual Kakuro puzzles as ReportLab flowables.
6.  **`assembler.py`**: Orchestrates the build: generates puzzles, assembles pages, and builds the TOC.

