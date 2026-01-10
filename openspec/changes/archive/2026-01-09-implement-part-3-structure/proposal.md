# Implement Part 3 Structure

## Why
The book outline defines "Part 3: Intermediate Level" as a structured progression using 9x9, 10x10, and 11x11 grids (Chapters 7-9). Currently, `book.yaml` groups all these into a single "Intermediate" puzzle section. We need to break this down to match the user's requirement for a high-quality, chapter-based experience.

Additionally, we missed two key "Part 2" items in the previous iteration:
*   Progress Tracker
*   Beginner Tips & Tricks

## What Changes
1.  **Cleanup Part 2**:
    *   Add `progress_tracker.md` (Chapter?)
    *   Add `beginner_tips.md` (Chapter?)
2.  **Part 3 Structure**:
    *   Break "Part 3" monolithic section into:
        *   Chapter 7 (9x9)
        *   Chapter 8 (10x10)
        *   Chapter 9 (11x11)
    *   Generate content placeholders for these chapters.
    *   Configure `book.yaml` to use the new structure.

## Verification
*   **Adversarial TOC Check**: Use `scripts/validate_toc.py` (updated to check for new chapters).
*   **Visual Check**: Inspect PDF to ensure puzzles are correctly sized (9x9 vs 10x10 vs 11x11) and follow their respective chapters.
