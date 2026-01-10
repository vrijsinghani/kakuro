# Change: Add Chapter 3 Content

## Why
The book outline specifies a "Chapter 3: Your First Puzzle Walkthrough" which is currently missing.
This chapter is critical for bridging the gap between basic rules (Chapter 1) and independent solving (Part 2).

## What Changes
- Create `books/master-kakuro/chapters/chapter_3.md`
- Create 4 illustrative diagrams in `books/master-kakuro/chapters/visuals/diagrams/chapter3/*.yaml` (utilizing the new `diagram-renderer` capability)

## Impact
- **Content**: Adds ~4 pages of content to Part 1.
- **Build**: The book builder will include this new chapter.
- **Specs**: No spec changes required (uses existing `diagram-renderer` and `book-builder` capabilities).
