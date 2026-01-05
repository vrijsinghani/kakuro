# Portfolio Management

This directory tracks all Kakuro puzzle books across their lifecycle: planning, development, publication, and performance monitoring.

## Directory Structure

### `published/`
Books that are live on Amazon KDP.

**Contents per book:**
```
published/
├── kakuro_beginner_500/
│   ├── book_info.json          # Metadata, ASIN, publication date
│   ├── interior.pdf            # Final interior PDF (archived)
│   ├── cover.pdf               # Final cover PDF (archived)
│   ├── kdp_listing.md          # Title, description, keywords used
│   ├── sales_data.xlsx         # Sales tracking (updated monthly)
│   ├── reviews.md              # Customer reviews and feedback
│   └── performance_notes.md    # Lessons learned, optimization notes
```

**book_info.json structure:**
```json
{
  "title": "Kakuro Puzzle Book for Adults: 500 Puzzles from Easy to Expert",
  "asin": "B0XXXXXXXXX",
  "publication_date": "2026-01-15",
  "difficulty": "beginner",
  "puzzle_count": 500,
  "page_count": 200,
  "trim_size": "8.5x11",
  "price_usd": 12.99,
  "categories": ["Puzzles & Games", "Logic Puzzles"],
  "keywords": ["kakuro", "puzzle book", "logic puzzles", "brain games"],
  "status": "published",
  "kdp_url": "https://kdp.amazon.com/...",
  "amazon_url": "https://www.amazon.com/dp/B0XXXXXXXXX"
}
```

### `in_progress/`
Books currently being developed.

**Workflow stages:**
1. **Planning** - Concept, target audience, specifications
2. **Puzzle Generation** - Creating and validating puzzles
3. **Layout** - PDF interior creation
4. **Cover Design** - Cover creation and approval
5. **QA** - Quality assurance and validation
6. **Pre-Launch** - Metadata preparation, final checks

**Contents per book:**
```
in_progress/
├── kakuro_large_print_seniors/
│   ├── project_plan.md         # Specifications and timeline
│   ├── progress.md             # Current status and next steps
│   ├── puzzles/                # Generated puzzles (work in progress)
│   ├── drafts/                 # Draft PDFs and covers
│   └── notes.md                # Development notes and decisions
```

### `planned/`
Future book ideas and concepts.

**Contents:**
- Book concepts and specifications
- Target audience research
- Competitive analysis
- Estimated timeline and priority

**Example:**
```
planned/
├── kakuro_expert_1000.md       # 1000 expert-level puzzles
├── kakuro_themed_holidays.md   # Holiday-themed Kakuro
├── kakuro_kids_edition.md      # Simplified for children
└── kakuro_giant_format.md      # Extra-large grids
```

## Portfolio Strategy

### Book Series Structure

#### Beginner Series
- **Target**: Newcomers to Kakuro
- **Puzzle count**: 200-500 puzzles
- **Grid size**: 6×6 to 9×9
- **Price point**: $8.99 - $11.99
- **Volumes**: Multiple volumes for variety

#### Intermediate Series
- **Target**: Experienced puzzle solvers
- **Puzzle count**: 300-500 puzzles
- **Grid size**: 9×9 to 12×12
- **Price point**: $10.99 - $13.99
- **Volumes**: Themed collections

#### Expert Series
- **Target**: Kakuro enthusiasts
- **Puzzle count**: 500-1000 puzzles
- **Grid size**: 12×12 to 15×15
- **Price point**: $13.99 - $17.99
- **Volumes**: Challenge collections

#### Large Print Series
- **Target**: Seniors, visually impaired
- **Puzzle count**: 100-200 puzzles (fewer per page)
- **Font size**: 14-16pt minimum
- **Price point**: $11.99 - $14.99 (premium for large print)
- **Volumes**: All difficulty levels

### Launch Schedule

**Year 1 Goals:**
- Q1 2026: Launch 2 beginner books
- Q2 2026: Launch 1 intermediate, 1 large print
- Q3 2026: Launch 1 expert, 1 beginner volume 2
- Q4 2026: Launch holiday-themed collection

**Prioritization criteria:**
1. Market demand (search volume)
2. Competition level (fewer competitors = higher priority)
3. Production complexity (simpler = faster launch)
4. Profit potential (price point vs. production cost)

## Performance Tracking

### Key Metrics

**Sales Metrics:**
- Daily/weekly/monthly sales
- Revenue and royalties
- Units sold per book
- Sales velocity trends

**Ranking Metrics:**
- Best Sellers Rank (BSR) - overall and per category
- Category rankings
- Keyword rankings
- Competitive position

**Customer Metrics:**
- Review count and average rating
- Review sentiment (positive/negative themes)
- Customer questions
- Return rate

**Marketing Metrics:**
- Page views (Amazon listing)
- Conversion rate (views to sales)
- Click-through rate (search to listing)
- A+ Content performance (if using Brand Registry)

### Tracking Tools

**KDP Dashboard:**
- Sales reports (daily, monthly)
- Royalty reports
- Free book downloads (if running promotions)

**Amazon Author Central:**
- Enhanced sales dashboard
- Review management
- Author page analytics

**Third-Party Tools:**
- Book Bolt - BSR tracking, keyword monitoring
- Helium 10 - Keyword rank tracking
- Publisher Rocket - Category and keyword research

### Monthly Review Process

1. **Export sales data** from KDP Dashboard
2. **Update sales_data.xlsx** for each published book
3. **Check BSR** in all categories
4. **Review customer feedback** (new reviews, questions)
5. **Analyze trends** (sales up/down, seasonal patterns)
6. **Identify optimization opportunities** (keywords, pricing, categories)
7. **Update portfolio strategy** based on performance

## Optimization Strategies

### Underperforming Books
- **Low sales**: Adjust pricing, update keywords, improve description
- **Low conversion**: Redesign cover, enhance preview images
- **Poor reviews**: Analyze feedback, consider quality improvements
- **Low visibility**: Request additional categories, run promotions

### High-Performing Books
- **Create variations**: Different difficulty levels, themed versions
- **Expand series**: Volume 2, 3, etc.
- **Cross-promote**: Mention in other book descriptions
- **Leverage success**: Use as template for new books

### Portfolio-Wide
- **Identify patterns**: Which difficulty levels sell best?
- **Seasonal trends**: When do puzzle books sell most?
- **Price optimization**: Test different price points
- **Bundle opportunities**: Create multi-book bundles

## Templates

### Book Planning Template
See `templates/book_planning_template.md`

### Progress Tracking Template
See `templates/progress_tracking_template.md`

### Performance Review Template
See `templates/performance_review_template.md`

## Best Practices

### Documentation
- Keep detailed notes on decisions and rationale
- Document what works and what doesn't
- Track time spent on each book (for ROI calculation)

### Version Control
- Archive final versions of published books
- Keep source files for potential updates
- Document any post-publication changes

### Continuous Improvement
- Learn from each book launch
- Iterate on successful patterns
- Experiment with new approaches
- Stay updated on KDP policy changes

### Risk Management
- Don't rely on a single book
- Diversify difficulty levels and formats
- Monitor competition regularly
- Have backup plans for underperformance

