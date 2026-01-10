# Implement Part 4 Structure

## Summary
Split Part 4 (Expert Level) into distinct chapters with dedicated grid sizes per the outline:
- **Chapter 10: Expert Entry** - 20 puzzles @ 12x12
- **Chapter 11: Master Class** - 25 puzzles @ 13x13
- **Chapter 12: Ultimate Challenges** - 25 puzzles @ 14x15

Currently Part 4 is a single `puzzle_section` with mixed sizes (12-14). This change mirrors the structure implemented for Part 3.

## Proposed Changes

### [NEW] books/master-kakuro/chapters/chapter_10.md
Chapter introduction for "Expert Entry" section.

### [NEW] books/master-kakuro/chapters/chapter_11.md
Chapter introduction for "Master Class" section.

### [NEW] books/master-kakuro/chapters/chapter_12.md
Chapter introduction for "Ultimate Challenges" section.

### [MODIFY] books/master-kakuro/book.yaml
Replace single Part 4 puzzle_section with:
- Part 4 header
- Chapter 10 + puzzle_section (12x12)
- Chapter 11 + puzzle_section (13x13)
- Chapter 12 + puzzle_section (14x15)

## Verification
1. Build book: `python -m src.book_builder build master-kakuro`
2. Verify TOC: `python scripts/validate_toc.py`
3. Analyze puzzles: `python scripts/analyze_puzzles.py`
4. Visual: Check PDF for correct chapter headers and grid sizes
