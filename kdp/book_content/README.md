# DEPRECATED

This directory is deprecated. Book content has been migrated to the new `books/` directory structure.

## New Location

Book content is now located at:
- `books/beginner-to-expert-250/` - The beginner-to-expert 250 puzzle book

## Using the New Book Builder

To build books, use the new book builder CLI:

```bash
# List available books
python -m src.book_builder list

# Validate a book configuration
python -m src.book_builder validate beginner-to-expert-250

# Build chapters only (no puzzles)
python -m src.book_builder build beginner-to-expert-250 --chapters-only

# Build full book
python -m src.book_builder build beginner-to-expert-250
```

## Migration Notes

- Chapter markdown files: `books/beginner-to-expert-250/chapters/`
- Diagrams are now rendered programmatically via `src/book_builder/diagrams/`
- Book configuration: `books/beginner-to-expert-250/book.yaml`

