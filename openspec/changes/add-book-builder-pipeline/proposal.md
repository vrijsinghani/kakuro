# Change: Add Book Builder Pipeline

## Why

The project has puzzle generation (`src/puzzle_generation/`) and PDF rendering (`src/pdf_generation/`) capabilities, but no unified pipeline to assemble complete books. Currently, there's no way to:

1. Combine instructional chapters (markdown + diagrams) with generated puzzles
2. Produce a complete, print-ready PDF book
3. Support multiple books with different content and configurations
4. Automate the end-to-end book creation workflow

The immediate need is to render Chapters 1-2 (with diagrams) plus generated puzzles into a single PDF. The longer-term need is to support a series of books (Beginner-to-Expert, Easy Kakuro, Hard Kakuro, Seniors Edition, etc.).

## What Changes

### New Capability: Book Builder (`src/book_builder/`)
- **Book configuration** — YAML-based book definition (title, author, chapters, puzzle specs, layout)
- **Chapter rendering** — Convert markdown chapters with embedded images to PDF pages
- **Content assembly** — Combine front matter, chapters, puzzles, solutions, back matter
- **Multi-book support** — Each book is self-contained in `books/{book-id}/`

### New Directory Structure: `books/`
- Each book has its own directory with config, chapters, and visuals
- Shared code infrastructure, unique content per book
- Generated output to `books/{book-id}/output/`

### Integration with Existing Modules
- Uses `src/puzzle_generation/` to generate puzzles per book spec
- Uses `src/pdf_generation/` to render puzzle pages
- Adds new chapter/content rendering capabilities

## Impact

- **New code:** `src/book_builder/` module (~500-800 lines estimated)
- **New directories:** `books/` structure for book projects
- **Migration:** Move current `kdp/book_content/` to `books/beginner-to-expert-250/`
- **Dependencies:** May add `markdown` or `mistune` for markdown parsing

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         BUILD COMMAND                           │
│              python -m book_builder build <book-id>             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    books/{book-id}/book.yaml                    │
│   ┌─────────────┬──────────────┬────────────────┬────────────┐  │
│   │   Metadata  │   Chapters   │  Puzzle Specs  │   Layout   │  │
│   └─────────────┴──────────────┴────────────────┴────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Chapter Renderer│   │Puzzle Generator │   │ Solution Render │
│  (markdown→PDF) │   │(src/puzzle_gen) │   │(src/pdf_gen)    │
└─────────────────┘   └─────────────────┘   └─────────────────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PDF Document Assembly                       │
│   [Front Matter] → [Chapters] → [Puzzles] → [Solutions] → [Back]│
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              books/{book-id}/output/interior.pdf                │
└─────────────────────────────────────────────────────────────────┘
```

## Out of Scope

- Cover generation (separate effort)
- EPUB/Kindle format (future enhancement)
- Automated KDP upload (future enhancement)
- ISBN barcode generation (future enhancement)

## Current Status (2026-01-08)

**Phase 1-2: COMPLETE** — Book config, chapter rendering, image handling working.

**Phase 5: IN PROGRESS** — Programmatic Diagram Renderer

### Problem (Resolved)

The original approach used HTML→Playwright→PDF→SVG conversion pipeline:
- HTML diagrams captured as very tall images (30-50+ inches)
- Multiple conversion steps caused whitespace/sizing issues
- Fallbacks to PNG raster images degraded quality
- External dependencies (Playwright, pdf2svg) were fragile

### Solution

Replace the HTML conversion pipeline with **programmatic ReportLab diagram rendering**:
- Diagrams defined as Python dataclasses
- Rendered directly using ReportLab drawing primitives
- True vector output, perfect scaling
- No external dependencies
- Consistent with puzzle grid rendering approach

See `openspec/changes/add-book-builder-pipeline/specs/diagram-renderer/` for full spec.

**Completed:**
- [x] Removed PNG fallbacks from chapter_renderer.py
- [x] Updated image scaling to prioritize full width

**Next Steps:**
1. Create DiagramRenderer class and data models
2. Define all Chapter 1 diagrams in Python
3. Integrate with ChapterRenderer
4. Complete Phase 6 (Testing & Polish)

