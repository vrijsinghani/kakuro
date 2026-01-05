# Project Context: Kakuro Puzzle Book Generator

## Purpose

This project generates high-quality Kakuro puzzle books for publication on Amazon KDP (Kindle Direct Publishing). The goal is to create professional, print-ready puzzle books that capitalize on the identified market opportunity: high demand (~36,635 monthly searches) with exceptionally low competition.

### Business Objectives
- Generate Kakuro puzzle books in various difficulty levels (Beginner, Intermediate, Expert)
- Create large-format collections (500-1000+ puzzles per book)
- Target multiple audience segments (adults, seniors with large print, beginners)
- Produce print-ready PDFs optimized for KDP specifications
- Automate the entire book generation workflow from puzzle creation to final PDF

### Success Criteria
- Puzzles must be mathematically valid and have unique solutions
- Professional layout suitable for print publication
- Clear "How to Play" instructions (Kakuro is less familiar than Sudoku)
- Clean solution sections
- KDP-compliant formatting (trim sizes, margins, bleed)

## Tech Stack

### Core Technologies
- **Python 3.x** - Primary programming language
- **ReportLab** - Premium PDF generation with precise control over layout, typography, and print quality
  - `reportlab.pdfgen.canvas` - Low-level drawing operations
  - `reportlab.platypus` - High-level document assembly (Flowables, Frames, PageTemplates)
  - `reportlab.lib.pagesizes` - Standard page dimensions (LETTER, A4, custom KDP sizes)
  - `reportlab.lib.units` - Precise measurements (inch, cm, mm, pica)
  - `reportlab.pdfbase` - Font embedding and management
- **PIL/Pillow** - Image processing for cover design and graphics
- **Cairo/CairoSVG** (optional) - Vector graphics rendering for ultra-sharp puzzle grids

### Puzzle Generation
- **Custom backtracking algorithm** - Constraint satisfaction solver for Kakuro puzzles
- **Random sampling** - Puzzle variation and difficulty control
- **Constraint validation** - Ensures unique solutions and valid puzzle states
- **Difficulty calibration** - Algorithmic difficulty scoring based on solving techniques required

### Output Formats
- **PDF/X-1a:2001** - Print-ready PDF with embedded fonts, CMYK color, no transparency
- **High-resolution preview images** - 300 DPI JPG/PNG for marketing and Amazon preview
- **EPUB** (future) - Digital edition for Kindle Direct Publishing
- **Print-on-demand ready** - Separate interior and cover PDFs meeting KDP specifications

## Project Conventions

### Code Style
- **PEP 8 compliance** - Standard Python style guide
- **Descriptive variable names** - `h_runs`, `v_runs`, `black_density` clearly indicate purpose
- **Function naming** - Snake_case for functions: `generate_kakuro()`, `compute_runs()`, `solve_kakuro()`
- **Modular design** - Separate functions for generation, solving, rendering, and PDF creation
- **Comments** - Document complex algorithms, especially constraint solving logic

### Architecture Patterns

#### Separation of Concerns
1. **Puzzle Logic Layer** - Generation and solving algorithms
   - `generate_kakuro()` - Creates valid puzzle grids
   - `compute_runs()` - Identifies horizontal and vertical runs
   - `solve_kakuro()` - Validates puzzle solvability using backtracking

2. **Rendering Layer** - Visual presentation
   - Grid drawing with matplotlib
   - Clue placement and formatting
   - Solution visualization

3. **Output Layer** - File generation
   - PDF compilation with PdfPages
   - Image export for previews
   - Multi-page book assembly

#### Data Structures
- **Grid representation**: 2D list where `-1` = black cell, `0` = empty cell, `1-9` = filled cell
- **Runs**: List of `[row/col, start, length, sum]` tuples for horizontal/vertical constraints
- **Puzzle state**: Tuple of `(grid, h_runs, v_runs)` for complete puzzle representation

### Testing Strategy

#### Puzzle Validation
- **Solvability testing** - Every generated puzzle must have a unique solution
- **Constraint verification** - All runs must sum correctly with no duplicate digits
- **Edge case handling** - Minimum run length (2 cells), grid boundaries, black cell placement

#### Quality Assurance
- **Visual inspection** - Sample puzzles reviewed for clarity and professional appearance
- **Difficulty calibration** - Verify puzzles match intended difficulty level
- **PDF validation** - Check KDP compliance (margins, bleed, resolution)
- **Solution accuracy** - Verify solution pages match puzzle pages

#### Performance Testing
- **Generation speed** - Target: <1 second per puzzle for batch generation
- **Memory efficiency** - Handle large book generation (1000+ puzzles) without memory issues
- **PDF file size** - Optimize for reasonable upload/download times

### Git Workflow
- **Main branch** - Production-ready code for book generation
- **Feature branches** - New puzzle types, layout improvements, difficulty algorithms
- **Commit conventions** - Descriptive messages: "Add large-print layout option", "Improve backtracking performance"
- **Version tagging** - Tag releases for each published book version

## Domain Context

### Kakuro Puzzle Rules
Kakuro is a logic puzzle similar to a crossword but with numbers. Key rules:
- Fill white cells with digits 1-9
- Each "run" (horizontal or vertical sequence) must sum to the clue number
- No digit can repeat within a single run
- Black cells contain clues (sum for the run)
- Puzzles must have exactly one solution

### KDP Publishing Requirements

#### Trim Sizes (Common for Puzzle Books)
- **8.5" x 11"** - Standard large format
- **8" x 10"** - Slightly smaller, still comfortable
- **7" x 10"** - Compact format
- **Large Print** - Minimum 14pt font for senior-friendly books

#### Technical Specifications
- **Interior**: Black & white or premium color
- **Paper**: White or cream paper
- **Binding**: Paperback (perfect binding)
- **Margins**: Minimum 0.25" on all sides (0.375" for books >150 pages)
- **Bleed**: 0.125" if using full-bleed images
- **Resolution**: 300 DPI minimum for images
- **File format**: PDF (PDF/X-1a:2001 or PDF/X-3:2002 preferred)

### Target Audience Segments

1. **Beginners** - Need clear instructions, easier puzzles, gradual difficulty progression
2. **Adults** - Standard difficulty, professional appearance, variety of puzzle sizes
3. **Seniors** - Large print (14-16pt), high contrast, simpler layouts, fewer puzzles per page
4. **Experts** - Challenging puzzles, complex grids, minimal hand-holding

### Competitive Positioning
- **High demand, low supply** - Market gap opportunity
- **Quality over quantity** - Professional layout beats rushed competitors
- **Clear instructions** - Essential since Kakuro is less familiar than Sudoku
- **Variety** - Multiple difficulty levels and formats in portfolio

## Important Constraints

### Mathematical Constraints
- **Unique solutions** - Every puzzle must have exactly one valid solution
- **Valid sums** - All clue sums must be achievable with available digits (1-9, no repeats)
- **Minimum run length** - At least 2 cells per run
- **Maximum run length** - At most 9 cells (limited by available unique digits)

### Publishing Constraints
- **KDP file size limits** - Maximum 650 MB per file
- **Page count economics** - Printing costs increase with page count; balance puzzle count vs. price
- **Cover requirements** - Separate cover file with specific dimensions based on page count
- **ISBN requirements** - Optional but recommended for wider distribution

### Technical Constraints
- **PDF generation** - Must produce KDP-compliant PDFs
- **Print quality** - 300 DPI minimum for all visual elements
- **Font licensing** - Use only commercially licensed or open-source fonts
- **Color mode** - CMYK for print (not RGB)

### Business Constraints
- **Time to market** - Faster generation = quicker market entry
- **Scalability** - Must support portfolio expansion (multiple books)
- **Quality consistency** - All books must meet minimum quality standards
- **Cost efficiency** - Minimize manual intervention in book creation process

## External Dependencies

### Python Libraries (Required)
- **ReportLab** (v4.x+) - Premium PDF generation engine
  - Professional typography and layout control
  - Embedded fonts for consistent rendering
  - PDF/X compliance for print production
  - Precise positioning and measurements
- **Pillow** (PIL fork, v10.x+) - Image processing and manipulation
  - Cover image creation and optimization
  - Preview image generation
  - Image format conversion (PNG, JPG, TIFF)

### Python Libraries (Optional/Enhancement)
- **NumPy** - Numerical operations for puzzle generation optimization
- **CairoSVG** - Vector graphics rendering for ultra-sharp grids
- **PyPDF2/pypdf** - PDF manipulation and merging
- **python-barcode** - ISBN barcode generation for covers
- **qrcode** - QR code generation for marketing materials

### Publishing Platforms
- **Amazon KDP** - Primary distribution platform
  - KDP Dashboard: https://kdp.amazon.com
  - KDP Cover Creator (optional)
  - KDP Previewer tool for validation

### Design Tools (Optional)
- **Canva** - Cover design
- **Adobe InDesign** (alternative) - Professional layout
- **GIMP/Photoshop** - Image editing for covers

### Research & Validation
- **Amazon Best Sellers** - Competitive analysis
- **Google Trends** - Keyword research and demand validation
- **Book Bolt** - KDP research and puzzle generation tools (commercial alternative)

### Font Resources
- **Google Fonts** - Free, commercially licensed fonts
- **Font Squirrel** - Free fonts for commercial use
- **Recommended fonts**: Arial, Helvetica, Times New Roman (widely available, print-friendly)

## Workflow Automation Goals

### Automated Book Generation Pipeline
1. **Puzzle Generation** - Batch create N puzzles at specified difficulty
2. **Layout Assembly** - Arrange puzzles on pages with proper spacing
3. **Instruction Pages** - Auto-generate "How to Play" section
4. **Solution Section** - Create answer key with clear formatting
5. **PDF Compilation** - Assemble complete book-ready PDF
6. **Metadata Generation** - Create title, description, keywords for KDP listing

### Quality Control Checkpoints
- Validate all puzzles have unique solutions
- Check PDF meets KDP specifications
- Verify page count and pricing calculations
- Preview sample pages for visual quality

### Portfolio Management
- Track published books (title, difficulty, puzzle count, publish date)
- Generate variations (same puzzles, different layouts)
- Create series (Beginner Vol 1, Vol 2, etc.)
- Maintain consistent branding across books
