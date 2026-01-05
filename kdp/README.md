# KDP Listings

This directory contains all metadata, descriptions, keywords, and category information for Amazon KDP book listings.

## Directory Structure

### `metadata/`
Core book metadata for KDP listings.

**Files per book:**
- `{book_title}_metadata.json` - Structured metadata
- `{book_title}_metadata.txt` - Human-readable version

**Metadata fields:**
```json
{
  "title": "The Ultimate Kakuro Puzzle Book for Adults: 500 Puzzles from Easy to Expert",
  "subtitle": "Brain-Boosting Logic Puzzles with Solutions | Large Print Format",
  "author": "Your Author Name",
  "contributors": [],
  "description": "See descriptions/ directory",
  "language": "English",
  "publication_date": "2026-01-15",
  "isbn": "979-8-XXXXXXXXX",
  "edition": "1",
  "publisher": "Your Publisher Name",
  "categories": ["Games & Activities > Puzzles", "Humor & Entertainment > Puzzles & Games"],
  "keywords": "See keywords/ directory",
  "age_range": "Adult",
  "grade_range": null,
  "bisac_codes": ["GAM003000", "GAM017000"],
  "pricing": {
    "usd": 12.99,
    "gbp": 9.99,
    "eur": 11.99
  }
}
```

### `descriptions/`
Book descriptions for Amazon product pages.

**Description structure:**
1. **Hook** (1-2 sentences) - Grab attention, highlight main benefit
2. **Features** (bullet points) - What's inside the book
3. **Benefits** (paragraph) - Why customers should buy
4. **Specifications** (bullet points) - Technical details
5. **Call to action** - Encourage purchase

**Example template:**
```markdown
# {Book Title}

## Hook
Discover the addictive world of Kakuro puzzles with this comprehensive collection of 500 brain-boosting challenges! Perfect for puzzle enthusiasts who love Sudoku and crosswords but want something fresh and exciting.

## What's Inside
• 500 carefully crafted Kakuro puzzles ranging from easy to expert
• Clear, step-by-step instructions for beginners
• Large print format for comfortable solving
• Complete solutions for every puzzle
• Progressive difficulty to build your skills

## Why You'll Love This Book
Kakuro combines the best of crosswords and Sudoku into one captivating puzzle. Each puzzle exercises your logical thinking, pattern recognition, and arithmetic skills while providing hours of entertainment. Whether you're new to Kakuro or a seasoned solver, this book offers the perfect challenge level for you.

## Specifications
• 200 pages of premium quality puzzles
• 8.5" x 11" large format
• Professional layout with clear grids
• Durable paperback binding
• Solutions included

## Perfect For
✓ Puzzle lovers seeking new challenges
✓ Adults who enjoy logic puzzles
✓ Seniors who prefer large print
✓ Gift-givers looking for thoughtful presents
✓ Anyone wanting to keep their mind sharp

Scroll up and click "Buy Now" to start your Kakuro journey today!
```

**Files:**
- `{book_title}_description.md` - Markdown source
- `{book_title}_description.txt` - Plain text for KDP (max 4,000 characters)
- `{book_title}_description_html.txt` - HTML formatted (if using enhanced formatting)

### `keywords/`
Keyword research and backend keyword sets.

**KDP keyword slots:**
- 7 keyword fields
- Max 50 characters per field
- No need to repeat words (Amazon indexes all combinations)

**Keyword strategy:**
```
Slot 1: kakuro puzzle book adults
Slot 2: logic puzzles brain games
Slot 3: number puzzles large print
Slot 4: japanese crossword sudoku
Slot 5: brain teasers seniors
Slot 6: puzzle books for adults variety
Slot 7: math puzzles activity book
```

**Files per book:**
- `{book_title}_keywords.txt` - Backend keywords for KDP
- `{book_title}_keyword_research.md` - Research notes and alternatives
- `{book_title}_keyword_performance.xlsx` - Track which keywords drive traffic

**Keyword research sources:**
- Amazon autocomplete
- Competitor book keywords (visible in titles/subtitles)
- Google Keyword Planner
- Book Bolt / Publisher Rocket
- Customer reviews (language customers use)

### `categories/`
Amazon category selections and BISAC codes.

**KDP allows:**
- 2 categories selected during upload
- Up to 10 total via KDP support request
- BISAC codes for broader classification

**Relevant categories for Kakuro:**
1. Books > Humor & Entertainment > Puzzles & Games > Logic & Brain Teasers
2. Books > Humor & Entertainment > Puzzles & Games > Sudoku
3. Books > Crafts, Hobbies & Home > Games & Activities > Puzzles

**BISAC codes:**
- GAM003000 - GAMES & ACTIVITIES / Logic & Brain Teasers
- GAM017000 - GAMES & ACTIVITIES / Sudoku
- GAM000000 - GAMES & ACTIVITIES / General

**Files:**
- `category_strategy.md` - Overall category selection strategy
- `{book_title}_categories.txt` - Selected categories for each book
- `category_performance.xlsx` - Track BSR in each category

## KDP Listing Workflow

### 1. Pre-Launch Preparation
- [ ] Complete metadata template
- [ ] Write compelling description
- [ ] Research and select keywords
- [ ] Choose optimal categories
- [ ] Determine pricing strategy

### 2. Title Optimization
**Formula:** [Main Keyword] + [Differentiator] + [Benefit]

Examples:
- "Kakuro Puzzle Book for Adults: 500 Brain-Boosting Logic Puzzles"
- "Large Print Kakuro: Easy to Expert Puzzles for Seniors"
- "The Ultimate Kakuro Challenge: 1000 Expert-Level Number Puzzles"

**Best practices:**
- Include primary keyword in title
- Keep under 200 characters (title + subtitle)
- Make it descriptive and searchable
- Avoid keyword stuffing

### 3. Description Writing
- Write in markdown for easy editing
- Convert to plain text for KDP (remove formatting)
- Use HTML for enhanced formatting (bold, italics, lists)
- Test character count (max 4,000)
- Include relevant keywords naturally

### 4. Keyword Selection
- Brainstorm 50+ potential keywords
- Prioritize by search volume and relevance
- Avoid repeating words across slots
- Use all 7 keyword slots
- Don't waste characters on words already in title

### 5. Category Selection
- Start with 2 most relevant categories
- Monitor BSR (Best Sellers Rank) after launch
- Request additional categories via KDP support if needed
- Target categories with lower competition

## Performance Tracking

### Metrics to Monitor
- **BSR (Best Sellers Rank)** - Overall and per category
- **Keyword rankings** - Where book appears for target keywords
- **Conversion rate** - Views to purchases
- **Review count and rating** - Customer satisfaction
- **Sales velocity** - Daily/weekly sales trends

### Optimization Opportunities
- **A/B test descriptions** - Try different hooks and benefits
- **Adjust pricing** - Test different price points
- **Update keywords** - Replace underperforming keywords
- **Add categories** - Request more categories if BSR is good
- **Refresh cover** - Update cover if CTR is low

### Tools
- KDP Dashboard - Sales and royalty reports
- Amazon Author Central - Enhanced analytics
- Book Bolt - Keyword and category tracking
- Helium 10 - Keyword rank tracking

## Templates

See `templates/` subdirectory for:
- Metadata template (JSON)
- Description template (Markdown)
- Keyword research worksheet
- Category selection guide
- Launch checklist

## Best Practices

### Title & Subtitle
- Front-load with primary keyword
- Make it descriptive and specific
- Include puzzle count if it's a selling point
- Mention "large print" if applicable

### Description
- Start with a strong hook
- Use bullet points for scannability
- Highlight unique features
- Include social proof (if available)
- End with clear call to action

### Keywords
- Use all 7 slots
- Don't repeat words
- Include misspellings if common
- Use long-tail keywords
- Avoid brand names (Amazon, Sudoku brands)

### Categories
- Choose most specific categories
- Avoid overly competitive categories
- Request additional categories after launch
- Monitor BSR in each category

