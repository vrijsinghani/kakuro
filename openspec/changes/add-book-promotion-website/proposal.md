# Change: Add Book Promotion Website

## Why

Need a promotional landing page to drive book sales and capture leads. The website will serve as a marketing hub for the Master Kakuro book, featuring book description, purchase links, and sample puzzles.

## What Changes

- Add new `book-website` capability for promotional website
- Create React/Vite website in `website/` directory using Tailwind CSS
- Implement responsive landing page with:
  - Hero section with book cover and tagline
  - Features/benefits section from book description
  - Difficulty levels breakdown
  - Call-to-action buttons for Amazon purchase
  - Sample puzzle preview (optional)
- Design system: Sage/cream/wood/stone theme matching the book cover aesthetic

## Impact

- Affected specs: None (new capability)
- Affected code: `website/` directory (currently empty except README.md)
- New dependencies: Vite, React, TypeScript, shadcn/ui, Tailwind CSS
