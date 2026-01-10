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

**Phase 5: COMPLETE** — Programmatic Diagram Renderer

### Problem (Resolved)

The original approach used HTML→Playwright→PDF→SVG conversion pipeline:
- HTML diagrams captured as very tall images (30-50+ inches)
- Multiple conversion steps caused whitespace/sizing issues
- Fallbacks to PNG raster images degraded quality
- External dependencies (Playwright, pdf2svg) were fragile

### Solution (Implemented)

Replaced the HTML conversion pipeline with **programmatic ReportLab diagram rendering**:
- Diagrams defined as Python dataclasses (`DiagramDefinition`, `DiagramGrid`, `DiagramCell`)
- Rendered directly using ReportLab drawing primitives (`DiagramFlowable`)
- True vector output, perfect scaling
- No external dependencies
- Consistent with puzzle grid rendering approach

See `openspec/changes/add-book-builder-pipeline/specs/diagram-renderer/` for full spec.

### Completed Implementation

**Foundation:**
- [x] `src/book_builder/diagram_models.py` — Data models for diagrams, grids, cells, legends, annotations
- [x] `src/book_builder/diagram_renderer.py` — DiagramFlowable with grid, legend, annotation rendering
- [x] `src/book_builder/reference_table_renderer.py` — ReferenceTableFlowable for combination tables

**Chapter 1 Diagrams (7 diagrams):**
- [x] `src/book_builder/diagrams/chapter1.py` — All 7 diagrams defined and rendering correctly
- [x] Diagram 1: Anatomy of a Kakuro Grid
- [x] Diagram 2-3: Across/Down runs
- [x] Diagram 4: No-Repetition Rule (horizontal side-by-side layout)
- [x] Diagram 5: Same Digit in Different Runs
- [x] Diagram 6: Complete Solved Example
- [x] Diagram 7: Unique Combinations Reference (ReferenceTableDefinition)

**Chapter 2 Diagrams (9 diagrams):**
- [x] `src/book_builder/diagrams/chapter2.py` — All 9 diagrams defined and rendering correctly
- [x] Diagram 1: Unique Combinations Reference Table
- [x] Diagrams 2a/2b: Elimination Method (Setup/Solution)
- [x] Diagram 3: The Cascade Effect
- [x] Diagram 4: Identifying Good Starting Points
- [x] Diagrams 5a/5b: Complex Intersection Analysis
- [x] Diagrams 6a/6b: Troubleshooting (Repeated Digits/Wrong Sums)

**Integration:**
- [x] ChapterRenderer detects `chapter{N}/diagram_{M}` paths and routes to programmatic diagrams
- [x] `PROGRAMMATIC_DIAGRAMS` registry includes chapter1 and chapter2
- [x] Per-grid title height calculation (no double-counting)
- [x] Legend positioning (right-side, vertically centered)
- [x] Annotation box spacing consistency

**Next Steps:**
1. Phase 5.5: Cleanup deprecated HTML/PNG/SVG diagram files
2. Phase 3: Book Assembly (front matter, TOC, puzzle integration)
3. Phase 4: Build CLI
4. Phase 6: Testing & Polish

