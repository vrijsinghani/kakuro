# Issue: Chapter Diagram Font Sizes Are Too Small

**Date:** 2026-01-08  
**Status:** Open  
**Priority:** High  
**Affects:** PDF book generation, specifically chapter diagrams

## Summary

The instructional diagrams in Chapters 1 and 2 have font sizes that are too small when rendered in the final PDF. Despite multiple attempts to increase font sizes in the source HTML, the diagrams remain difficult to read.

## Root Cause Analysis

The diagrams are created via this pipeline:
1. **Source HTML** (`kdp/book_content/chapters/visuals/kakuro_chapter*.html`) - contains styled diagrams
2. **Playwright conversion** (`scripts/convert_diagrams_to_svg.py`) - captures diagrams as PDF + PNG
3. **Chapter renderer** (`src/book_builder/chapter_renderer.py`) - embeds images in book PDF

**The core issue:** The HTML diagrams have large vertical heights (some are 30-50+ inches tall as captured). When scaled to fit a book page (~6-9 inches), everything shrinks proportionally, making text unreadable.

### Diagram Dimensions (as captured)

| Diagram | Dimensions (pts) | Aspect Ratio | Notes |
|---------|------------------|--------------|-------|
| Ch2 Diagram 1 | 930x1278 | 1.4:1 | Nearly fits |
| Ch2 Diagram 2 | 930x3849 | 4.1:1 | Way too tall |
| Ch2 Diagram 3 | 930x1196 | 1.3:1 | Nearly fits |
| Ch2 Diagram 5 | 930x2654 | 2.9:1 | Too tall |
| Ch2 Diagram 6 | 930x2513 | 2.7:1 | Too tall |

## Current Issues

### Chapter 1 Issues
1. **Diagram 1** - "How to Read Clues" box has excessive blank lines at bottom
2. **Diagram 3** - Not full width, excessive white space at bottom  
3. **Diagram 4** - "Notice the digit 9" box has excessive blank lines at bottom
4. **Diagram 5** - Annotations box has excessive blank lines

### Chapter 2 Issues (Critical)
1. **Diagram 1** - Not centered, text too small
2. **Diagram 2** - Not centered, text too small
3. **Diagram 3** - Not centered, text too small
4. **Diagram 5** - Not centered, text too small
5. **Diagram 6** - Not centered, text too small

## Attempted Fixes

### HTML Font Size Increases
- Increased `.caption` from 18px to 28px
- Increased `.annotation` from 16-18px to 28px
- Increased `.legend-item` from 18px to 28px
- Increased `table` and `th` from 18-20px to 28px
- Removed inline font-size overrides

**Result:** No visible improvement - the scaling factor is the problem, not the source font size.

### Renderer Scaling Changes
- Changed from 6-inch max height to page-height based scaling
- Added aspect ratio detection (>1.5) to fallback to PNG for tall PDFs
- Added `_create_raster_image` helper method

**Result:** Images now fit on page but are still scaled down too much.

## Proposed Solutions

### Option A: Split Tall Diagrams (Recommended)
Split the HTML source for tall diagrams into multiple smaller `diagram-container` divs:
- Diagram 2 → Already split in markdown references (`diagram_2_page1.png`, `diagram_2_page2.png`)
- Diagram 5 → Split into 2-3 parts
- Diagram 6 → Split into 2-3 parts

**Files to modify:**
- `kdp/book_content/chapters/visuals/kakuro_chapter2_visuals.html`

### Option B: Increase Capture Resolution
Modify `scripts/convert_diagrams_to_svg.py` to capture at higher resolution (e.g., 2x or 3x scale) so when scaled down, text remains readable.

### Option C: Use Fixed Font Sizes in Points
Instead of using pixel-based font sizes that scale with the image, use larger base font sizes in the HTML that remain readable after the expected scaling factor is applied.

**Example:** If diagram will be scaled to 30% of original, use 40px fonts so they become ~12pt when rendered.

### Option D: Redesign Diagrams for Print
Create separate "print-optimized" versions of diagrams designed for 8.5"x11" output:
- Maximum height of 8 inches
- Minimum font size of 36px (to be ~12pt after scaling)
- Simplified layouts that don't require scrolling

## Files Involved

- `kdp/book_content/chapters/visuals/kakuro_chapter1_visuals.html`
- `kdp/book_content/chapters/visuals/kakuro_chapter2_visuals.html`
- `scripts/convert_diagrams_to_svg.py`
- `src/book_builder/chapter_renderer.py`
- `books/beginner-to-expert-250/chapters/chapter_1.md`
- `books/beginner-to-expert-250/chapters/chapter_2.md`

## Testing

After fixes, verify by:
1. Running `python scripts/convert_diagrams_to_svg.py`
2. Building test PDF: check `books/beginner-to-expert-250/output/test_complete_*.pdf`
3. Visually inspect each diagram in the PDF viewer
4. Confirm text is readable without zooming
5. Confirm diagrams are centered on the page

## Related Work

- Change proposal: `openspec/changes/add-pdf-generation/`

