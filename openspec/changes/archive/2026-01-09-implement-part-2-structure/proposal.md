# Implement Part 2 Structure

## Why
The current `book.yaml` defines "Part 2: Beginner Level" as a single monolithic puzzle section. However, `books/master-kakuro/outline.md` specifies a detailed structure with three distinct chapters:
*   **Chapter 4: Warm-Up Puzzles** (6x6 grids)
*   **Chapter 5: Building Skills** (7x7 grids)
*   **Chapter 6: Beginner Mastery** (8x8 grids)
*   *Plus "Beginner Tips & Tricks"*

The current `src/book_builder` implementation does not easily support interleaving puzzle sections with chapter text, or breaking a "Part" into multiple sub-headers without a major "Section Header" page for each. We need to align the configuration and the builder logic to support this granular structure.

## What Changes
1.  **Update `book.yaml`**:
    *   Remove the single "Part 2" entry.
    *   Add entries for Chapters 4, 5, and 6.
    *   Configure these entries to point to both markdown content (intro text) and puzzle specifications.
    
2.  **Update `src/book_builder`**:
    *   Modify `BookConfig` and `BookAssembler` to support a new content type or a more flexible list that allows mixing chapters and puzzle sections freely under a unified "Part" header.
    *   Ensure "Part 2" page header is generated once, followed by the chapters.

3.  **Generate Content**:
    *   Create `books/master-kakuro/chapters/chapter_4.md` (Warm-Up intro).
    *   Create `books/master-kakuro/chapters/chapter_5.md` (Building Skills intro).
    *   Create `books/master-kakuro/chapters/chapter_6.md` (Mastery intro).
    
## Verification
*   **PDF Inspection**: Verify that Part 2 starts correctly, and Chapters 4, 5, 6 follow in order with their respective puzzles.
*   **Puzzle Verification**: Ensure the puzzles in each chapter match the grid size specs (6x6, 7x7, 8x8).
