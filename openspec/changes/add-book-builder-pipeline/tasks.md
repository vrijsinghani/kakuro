# Tasks: Book Builder Pipeline

## Phase 1: Foundation ✓ COMPLETE

### 1.1 Project Structure
- [x] 1.1.1 Create `src/book_builder/` module structure
- [x] 1.1.2 Create `books/` directory structure
- [x] 1.1.3 Migrate `kdp/book_content/chapters/` to `books/beginner-to-expert-250/chapters/`
- [x] 1.1.4 Migrate `kdp/book_content/chapters/visuals/` to `books/beginner-to-expert-250/chapters/visuals/`

### 1.2 Configuration System
- [x] 1.2.1 Define `BookConfig` Pydantic model (metadata, content, layout, fonts)
- [x] 1.2.2 Define `ChapterConfig`, `PuzzleSectionConfig`, `LayoutConfig` models
- [x] 1.2.3 Implement YAML loader with validation
- [x] 1.2.4 Create initial `book.yaml` for beginner-to-expert-250
- [ ] 1.2.5 Write tests for config loading and validation

## Phase 2: Chapter Rendering ✓ COMPLETE

### 2.1 Markdown Parser
- [x] 2.1.1 ~~Add `mistune` dependency~~ Used regex-based parsing instead (simpler)
- [x] 2.1.2 Create `ChapterRenderer` class with inline markdown parsing
- [x] 2.1.3 Handle headings (h1, h2, h3) → ReportLab Paragraph styles
- [x] 2.1.4 Handle paragraphs → ReportLab Paragraph
- [x] 2.1.5 Handle bullet lists → ReportLab ListFlowable
- [x] 2.1.6 Handle bold/italic → ReportLab inline markup
- [x] 2.1.7 Handle horizontal rules → ReportLab HRFlowable
- [ ] 2.1.8 Write tests for markdown parsing

### 2.2 Image Handling
- [x] 2.2.1 Parse image references `![alt](path)` from markdown
- [x] 2.2.2 Resolve image paths relative to chapter file
- [x] 2.2.3 Create ReportLab Image flowables with proper sizing (aspect ratio preserved)
- [x] 2.2.4 Handle image captions (italic text after image)
- [x] 2.2.5 Test with Chapter 1 and Chapter 2 diagrams

### 2.3 Chapter Renderer
- [x] 2.3.1 Create `ChapterRenderer` class
- [x] 2.3.2 Implement chapter title rendering
- [x] 2.3.3 Convert parsed markdown to ReportLab flowables
- [x] 2.3.4 Handle horizontal rules as section dividers
- [x] 2.3.5 Implement large-print styling (14pt base font, increased line spacing)
- [x] 2.3.6 Test rendering Chapter 1 to PDF
- [x] 2.3.7 Test rendering Chapter 2 to PDF

### 2.4 Page Formatting (Added)
- [x] 2.4.1 Add page numbers (bottom center)
- [x] 2.4.2 Each chapter starts on new page

## Phase 3: Book Assembly

### 3.1 Document Structure
- [ ] 3.1.1 Create `BookDocument` class extending PDFDocument
- [ ] 3.1.2 Implement front matter templates (title page, copyright)
- [ ] 3.1.3 Implement TOC placeholder and finalization
- [ ] 3.1.4 Implement section dividers between parts

### 3.2 Puzzle Integration
- [ ] 3.2.1 Integrate with `src/puzzle_generation/` for puzzle creation
- [ ] 3.2.2 Implement puzzle caching (avoid regenerating on every build)
- [ ] 3.2.3 Create puzzle section headers
- [ ] 3.2.4 Integrate with `src/pdf_generation/` for puzzle rendering

### 3.3 Solutions Section
- [ ] 3.3.1 Implement compact solution grid layout (6 per page)
- [ ] 3.3.2 Add solution section header
- [ ] 3.3.3 Match solution numbers to puzzle numbers

### 3.4 Back Matter
- [ ] 3.4.1 Implement about author page (from markdown)
- [ ] 3.4.2 Implement "other books" placeholder page
- [ ] 3.4.3 Implement notes/scratch pages

## Phase 4: Build CLI

### 4.1 Command Interface
- [ ] 4.1.1 Create `__main__.py` for `python -m book_builder`
- [ ] 4.1.2 Implement `build <book-id>` command
- [ ] 4.1.3 Implement `--chapters-only` flag (skip puzzles)
- [ ] 4.1.4 Implement `--puzzles-only` flag (skip chapters)
- [ ] 4.1.5 Implement `--output` flag for custom output path
- [ ] 4.1.6 Add progress reporting during build

### 4.2 Validation
- [ ] 4.2.1 Validate book.yaml on load
- [ ] 4.2.2 Validate all referenced files exist
- [ ] 4.2.3 Validate image paths resolve correctly
- [ ] 4.2.4 Report missing or broken references

## Phase 5: Programmatic Diagram Renderer (BLOCKING)

**See:** `openspec/changes/add-book-builder-pipeline/specs/diagram-renderer/`

**Decision:** Replace HTML→browser→screenshot pipeline with ReportLab direct rendering.

### 5.1 Diagram Renderer Foundation
- [x] 5.1.1 Remove PNG fallbacks from chapter_renderer.py
- [x] 5.1.2 Update image scaling to prioritize full width for vector graphics
- [ ] 5.1.3 Create `src/book_builder/diagram_models.py` with dataclass definitions
- [ ] 5.1.4 Create `src/book_builder/diagram_renderer.py` with DiagramRenderer class
- [ ] 5.1.5 Implement grid rendering (cells, clues, highlights)
- [ ] 5.1.6 Implement annotation box rendering
- [ ] 5.1.7 Implement legend rendering
- [ ] 5.1.8 Implement side-by-side layout for comparison diagrams

### 5.2 Chapter 1 Diagram Definitions
- [ ] 5.2.1 Create `src/book_builder/diagrams/__init__.py`
- [ ] 5.2.2 Create `src/book_builder/diagrams/chapter1.py`
- [ ] 5.2.3 Define Diagram 1: Anatomy of a Kakuro Grid
- [ ] 5.2.4 Define Diagram 2: Understanding Across Runs (Horizontal)
- [ ] 5.2.5 Define Diagram 3: Understanding Down Runs (Vertical)
- [ ] 5.2.6 Define Diagram 4: The No-Repetition Rule (side-by-side CORRECT/INCORRECT)
- [ ] 5.2.7 Define Diagram 5: Same Digit in Different Runs
- [ ] 5.2.8 Define Diagram 6: Complete Solved Example
- [ ] 5.2.9 Define Diagram 7: Unique Combinations Reference

### 5.3 Chapter 2 Diagram Definitions
- [ ] 5.3.1 Create `src/book_builder/diagrams/chapter2.py`
- [ ] 5.3.2 Define all Chapter 2 diagrams (solving techniques)

### 5.4 Integration
- [ ] 5.4.1 Update ChapterRenderer to detect programmatic diagram references
- [ ] 5.4.2 Update chapter markdown to use new diagram references
- [ ] 5.4.3 Verify all diagrams render at full width
- [ ] 5.4.4 Verify all text is readable at print size (minimum 10pt effective)

### 5.5 Cleanup (after verification)
- [ ] 5.5.1 Deprecate HTML diagram source files
- [ ] 5.5.2 Deprecate scripts/convert_diagrams_to_svg.py
- [ ] 5.5.3 Remove PNG/SVG diagram files from books/ (keep as backup initially)

## Phase 6: Testing & Polish

### 6.1 Integration Tests
- [ ] 6.1.1 Test full build of beginner-to-expert-250 (chapters only)
- [ ] 6.1.2 Test full build with sample puzzles (10 per difficulty)
- [ ] 6.1.3 Validate output PDF opens correctly
- [ ] 6.1.4 Visual inspection of rendered chapters - ALL DIAGRAMS READABLE

### 6.2 Documentation
- [ ] 6.2.1 Write README for `src/book_builder/`
- [ ] 6.2.2 Document book.yaml schema
- [ ] 6.2.3 Write "Creating a New Book" guide
- [ ] 6.2.4 Update project README with book building instructions

### 6.3 Cleanup
- [ ] 6.3.1 Deprecate `kdp/book_content/` (add README pointing to new location)
- [ ] 6.3.2 Update any scripts referencing old paths
- [ ] 6.3.3 Final code review and cleanup

