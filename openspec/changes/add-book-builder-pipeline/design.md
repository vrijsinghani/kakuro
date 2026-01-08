# Design: Book Builder Pipeline

## Context

The Kakuro project needs to produce complete, print-ready PDF books combining:
- Instructional content (markdown chapters with diagrams)
- Generated puzzles (using existing puzzle generation)
- Solutions section
- Front/back matter

Each book in the series is self-contained with unique content. The puzzle generation and PDF rendering code is shared infrastructure.

## Goals / Non-Goals

### Goals
- Build complete PDF books from a single command
- Support multiple independent book projects
- Render markdown chapters with embedded PNG diagrams
- Integrate with existing puzzle generation and PDF rendering
- Produce KDP-compliant output

### Non-Goals
- Cover generation (separate module)
- EPUB/digital formats (future)
- Automated publishing workflow (future)
- Real-time preview/editing (future)

## Directory Structure

```
kakuro/
├── src/
│   ├── puzzle_generation/     # Existing - shared
│   ├── pdf_generation/        # Existing - shared
│   └── book_builder/          # NEW - book assembly pipeline
│       ├── __init__.py
│       ├── config.py          # Book config schema (Pydantic)
│       ├── builder.py         # Main build orchestration
│       ├── chapter_renderer.py # Markdown → PDF
│       └── assembler.py       # Combine all sections
│
├── books/                     # NEW - book projects
│   └── beginner-to-expert-250/
│       ├── book.yaml          # Book configuration
│       ├── chapters/
│       │   ├── chapter_1.md
│       │   ├── chapter_2.md
│       │   └── visuals/
│       │       └── diagrams/
│       │           ├── chapter1/
│       │           └── chapter2/
│       └── output/            # Generated artifacts
│           ├── interior.pdf
│           └── puzzles/       # Cached puzzle data
│
└── kdp/                       # DEPRECATED - migrate to books/
    └── book_content/          # Current location (to be moved)
```

## Book Configuration Schema

```yaml
# books/beginner-to-expert-250/book.yaml

metadata:
  title: "Kakuro Puzzle Book for Adults"
  subtitle: "250 Large Print Puzzles from Beginner to Expert with Solutions"
  author: "Author Name"
  isbn: null  # Optional

content:
  front_matter:
    - type: title_page
    - type: copyright
    - type: toc
  
  chapters:
    - path: chapters/chapter_1.md
      title: "Understanding Kakuro"
    - path: chapters/chapter_2.md
      title: "Essential Solving Techniques"
  
  puzzle_sections:
    - title: "Part 2: Beginner Level"
      difficulty: beginner
      count: 70
      grid_sizes: [6, 7, 8]
    - title: "Part 3: Intermediate Level"
      difficulty: intermediate
      count: 90
      grid_sizes: [9, 10, 11]
    - title: "Part 4: Expert Level"
      difficulty: expert
      count: 70
      grid_sizes: [12, 13, 14]
  
  back_matter:
    - type: solutions
    - type: about_author
      path: chapters/about.md

layout:
  page_size: letter          # letter, a4, or custom [w, h]
  margins:
    top: 0.75
    bottom: 0.75
    left: 0.75
    right: 0.75
  large_print: true
  puzzles_per_page: 1
  solutions_per_page: 6

fonts:
  body: "Helvetica"
  heading: "Helvetica-Bold"
  puzzle: "Helvetica"
```

## Chapter Rendering Approach

### Option A: ReportLab Platypus (Recommended)
Use ReportLab's Platypus for document-level flow:
- Parse markdown to extract paragraphs, headings, lists, images
- Convert to ReportLab Flowables (Paragraph, Image, Spacer)
- Let Platypus handle page breaks and flow

**Pros:** Native ReportLab, consistent with puzzle rendering, precise control
**Cons:** Must build markdown parser, more code

### Option B: Markdown → HTML → PDF (WeasyPrint)
Convert markdown to HTML, then use WeasyPrint for PDF.

**Pros:** Markdown parsing handled, CSS styling
**Cons:** Additional dependency, different rendering engine than puzzles

### Decision: Option A (ReportLab Platypus)
Keeps everything in ReportLab for consistency. Use `mistune` for markdown parsing.

## Build Pipeline

```python
def build_book(book_id: str) -> Path:
    """Build a complete book PDF."""
    # 1. Load configuration
    config = load_book_config(f"books/{book_id}/book.yaml")
    
    # 2. Initialize PDF document
    doc = BookDocument(config)
    
    # 3. Render front matter
    doc.add_title_page()
    doc.add_copyright_page()
    doc.add_toc_placeholder()  # Filled after pagination
    
    # 4. Render chapters
    for chapter in config.chapters:
        chapter_path = f"books/{book_id}/{chapter.path}"
        doc.add_chapter(chapter_path, chapter.title)
    
    # 5. Generate and render puzzles
    for section in config.puzzle_sections:
        puzzles = generate_puzzles(section)
        doc.add_puzzle_section(section.title, puzzles)
    
    # 6. Render solutions
    doc.add_solutions_section()
    
    # 7. Render back matter
    for item in config.back_matter:
        doc.add_back_matter(item)
    
    # 8. Finalize TOC with page numbers
    doc.finalize_toc()
    
    # 9. Save
    return doc.save(f"books/{book_id}/output/interior.pdf")
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Markdown parsing edge cases | Start simple (headings, paragraphs, lists, images), extend as needed |
| Page break control | Use Platypus KeepTogether for diagrams, manual breaks via markdown |
| Large print layout complexity | Define layout presets, test with target demographic |
| Puzzle generation time | Cache generated puzzles, regenerate only when spec changes |

## Migration Plan

1. Create `books/beginner-to-expert-250/` structure
2. Move `kdp/book_content/chapters/` content to new location
3. Create `book.yaml` configuration
4. Build and validate output matches expectations
5. Deprecate `kdp/book_content/` (keep for reference initially)

## Design Decisions (Resolved)

1. **Table of Contents:** Generate automatically from chapter headings
2. **Page numbering:** Normal page numbering, start at 1 from first page of content
3. **Chapter start pages:** Always start on right-hand (odd) page

