# Output

This directory contains all generated output files, from individual puzzles to final print-ready books.

## Directory Structure

### `puzzles/`
Individual generated puzzles organized by difficulty.

#### `puzzles/beginner/`
Easy puzzles for newcomers to Kakuro.
- Smaller grids (6×6 to 9×9)
- Shorter runs (2-3 cells)
- Simpler solving techniques required
- Clear, unambiguous solutions

**Naming convention:** `beginner_YYYYMMDD_NNN.json`
Example: `beginner_20260105_001.json`

#### `puzzles/intermediate/`
Medium difficulty puzzles.
- Standard grids (9×9 to 12×12)
- Mixed run lengths
- Requires some logical deduction
- Moderate solving time

**Naming convention:** `intermediate_YYYYMMDD_NNN.json`

#### `puzzles/expert/`
Challenging puzzles for experienced solvers.
- Larger grids (12×12 to 15×15)
- Complex run patterns
- Advanced solving techniques required
- Longer solving time

**Naming convention:** `expert_YYYYMMDD_NNN.json`

**Puzzle file format (JSON):**
```json
{
  "id": "beginner_20260105_001",
  "difficulty": "beginner",
  "grid_size": [9, 9],
  "grid": [[0, -1, -1, ...], ...],
  "h_runs": [[row, col, length, sum], ...],
  "v_runs": [[row, col, length, sum], ...],
  "solution": [[0, -1, 5, ...], ...],
  "metadata": {
    "generated_at": "2026-01-05T10:30:00Z",
    "difficulty_score": 2.3,
    "estimated_solve_time": "5-10 minutes"
  }
}
```

### `books/`
Complete book files ready for KDP upload.

#### `books/interiors/`
Interior PDF files (puzzle and solution pages).

**File naming:** `{title}_interior_v{version}.pdf`
Examples:
- `kakuro_beginner_500_interior_v1.pdf`
- `kakuro_large_print_seniors_interior_v2.pdf`
- `kakuro_expert_challenge_interior_v1.pdf`

**Requirements:**
- PDF/X-1a:2001 compliant
- Embedded fonts
- CMYK color mode
- Correct trim size with bleed
- Page count must match cover spine calculation

#### `books/covers/`
Cover PDF files (front, spine, back).

**File naming:** `{title}_cover_v{version}.pdf`
Examples:
- `kakuro_beginner_500_cover_v1.pdf`
- `kakuro_large_print_seniors_cover_v2.pdf`

**Requirements:**
- Dimensions: (trim width × 2) + spine width + (bleed × 2) by trim height + (bleed × 2)
- 300 DPI minimum
- CMYK color mode
- Barcode placement (if using ISBN)
- Spine text readable when book is on shelf

**Cover dimensions calculator:**
- Trim size: 8.5" × 11"
- Bleed: 0.125"
- Spine width: 0.002252 × page count (for white paper, black ink)
- Example (200 pages): 17.375" × 11.25"

#### `books/final/`
Final, QA-approved books ready for upload.

**Contents:**
- Interior PDF (final version)
- Cover PDF (final version)
- Preview images (for marketing)
- Metadata file (title, description, keywords)
- Upload checklist

**File structure:**
```
final/
├── kakuro_beginner_500/
│   ├── interior.pdf
│   ├── cover.pdf
│   ├── preview_01.jpg
│   ├── preview_02.jpg
│   ├── preview_03.jpg
│   ├── metadata.json
│   └── upload_checklist.md
```

### `previews/`
Preview images for Amazon listing and marketing.

**Amazon preview requirements:**
- First 7-10 pages of the book
- JPG or PNG format
- 72-300 DPI
- RGB color mode (for screen display)

**Marketing previews:**
- Sample puzzle pages
- Solution examples
- "How to Play" instructions
- Cover image (high-res)

**Naming convention:** `{book_title}_preview_{page_number}.jpg`

### `marketing/`
Marketing materials and promotional assets.

**Contents:**
- Social media graphics (Instagram, Facebook, Pinterest)
- Amazon A+ Content images (if using Brand Registry)
- Email newsletter graphics
- Blog post images
- Promotional banners

**Formats:**
- JPG/PNG for web use
- Optimized file sizes for fast loading
- Multiple sizes for different platforms

## Output Workflow

### 1. Puzzle Generation
```bash
python scripts/batch_generation/generate_puzzles.py --difficulty beginner --count 500
```
Output: `output/puzzles/beginner/beginner_YYYYMMDD_*.json`

### 2. Interior PDF Generation
```bash
python scripts/batch_generation/create_interior.py --puzzles output/puzzles/beginner/ --output output/books/interiors/
```
Output: `output/books/interiors/kakuro_beginner_500_interior_v1.pdf`

### 3. Cover Creation
- Design cover in Canva/Photoshop
- Export as PDF with correct dimensions
- Save to `output/books/covers/`

### 4. Quality Control
```bash
python scripts/quality_control/validate_book.py --interior output/books/interiors/kakuro_beginner_500_interior_v1.pdf --cover output/books/covers/kakuro_beginner_500_cover_v1.pdf
```

### 5. Final Preparation
- Move approved files to `output/books/final/{book_title}/`
- Generate preview images
- Create metadata file
- Complete upload checklist

### 6. KDP Upload
- Upload interior PDF
- Upload cover PDF
- Add metadata (title, description, keywords)
- Set pricing
- Publish!

## File Management

### Version Control
- Use version numbers in filenames: `_v1`, `_v2`, etc.
- Keep previous versions until book is published
- Archive old versions after successful publication

### Backup Strategy
- Daily backup of `output/` directory
- Cloud storage (Google Drive, Dropbox) for final books
- Local external drive backup weekly

### Cleanup
- Archive published books to `portfolio/published/`
- Delete intermediate files after final book is approved
- Keep puzzle JSON files for potential reuse

## Quality Checklist

Before moving to `final/`:
- [ ] Interior PDF is PDF/X-1a:2001 compliant
- [ ] All fonts are embedded
- [ ] Page count matches cover spine calculation
- [ ] Puzzles are validated (all solvable, unique solutions)
- [ ] Solutions are correct and match puzzles
- [ ] Cover dimensions are correct for page count
- [ ] Bleed and margins meet KDP requirements
- [ ] Preview images are generated
- [ ] Metadata is complete and accurate

