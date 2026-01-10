## ADDED Requirements

### Requirement: Chapter 3 Diagram Definitions

The system SHALL provide diagram definitions for Chapter 3 instructional diagrams (First Puzzle Walkthrough):

1.  **Diagram 1: Unique Combinations Analysis** - Highlighting the starting clue (4)
2.  **Diagram 2: Elimination Step** - Showing why one candidate fits an intersection
3.  **Diagram 3: Intersections Fill** - Completing cells based on the solved intersection
4.  **Diagram 4: Completion** - Filling the final cell and verifying sums

#### Scenario: Chapter 3 walkthrough diagrams render correctly
- **GIVEN** the Chapter 3 markdown references diagrams `chapter3_diagram1` through `chapter3_diagram4`
- **WHEN** the chapter is rendered to PDF
- **THEN** all diagrams render as vector graphics using the `programmatic` renderer
- **AND** match the step-by-step narrative of the walkthrough
