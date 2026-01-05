# Kakuro Puzzle Book Generator - Directory Structure

Complete directory structure with descriptions for the Kakuro KDP publishing project.

## Root Level

```
kakuro/
├── .venv/                      # Python virtual environment (not in git)
├── .gitignore                  # Git ignore rules
├── README.md                   # Project overview and quick start
├── SETUP_GUIDE.md              # Detailed setup instructions
├── PROJECT_STATUS.md           # Current project status and roadmap
├── DIRECTORY_STRUCTURE.md      # This file
├── requirements.txt            # Python dependencies
├── setup.py                    # Python package setup
└── create_directories.sh       # Directory creation script
```

## Source Code (`src/`)

```
src/
├── README.md                   # Source code documentation
├── puzzle_generation/          # Puzzle generation algorithms
│   ├── generator.py           # Main puzzle generation engine
│   ├── solver.py              # Backtracking solver
│   ├── difficulty.py          # Difficulty scoring
│   └── constraints.py         # Constraint validation
├── pdf_generation/             # ReportLab PDF creation
│   ├── book_builder.py        # PDF assembly orchestrator
│   ├── page_layouts.py        # Page templates
│   ├── styles.py              # Typography and styling
│   └── pdf_utils.py           # PDF helper functions
├── layout/                     # Visual layout and rendering
│   ├── grid_renderer.py       # Puzzle grid drawing
│   ├── clue_formatter.py      # Clue placement
│   ├── solution_renderer.py   # Solution pages
│   └── large_print.py         # Large-print layouts
├── utils/                      # Shared utilities
│   ├── config.py              # Configuration management
│   ├── file_utils.py          # File operations
│   ├── logger.py              # Logging setup
│   └── constants.py           # Project constants
└── validation/                 # Quality assurance
    ├── puzzle_validator.py    # Puzzle correctness
    ├── pdf_validator.py       # PDF/X compliance
    ├── kdp_validator.py       # KDP specifications
    └── quality_checker.py     # Visual quality
```

## Tests (`tests/`)

```
tests/
├── unit/                       # Unit tests
│   ├── test_generator.py
│   ├── test_solver.py
│   ├── test_pdf_builder.py
│   └── test_validators.py
├── integration/                # Integration tests
│   ├── test_full_pipeline.py
│   └── test_book_generation.py
└── fixtures/                   # Test data and fixtures
    ├── sample_puzzles.json
    └── test_config.yaml
```

## Assets (`assets/`)

```
assets/
├── README.md                   # Asset management guide
├── fonts/                      # Font files for PDF
│   ├── liberation/            # Liberation fonts (Arial alternative)
│   ├── dejavu/                # DejaVu fonts
│   └── roboto/                # Roboto fonts
├── images/                     # Image assets
│   ├── logos/                 # Brand logos
│   └── graphics/              # Decorative elements
└── templates/                  # Reusable templates
    ├── covers/                # Cover design templates
    ├── interiors/             # Interior page templates
    └── instructions/          # "How to Play" templates
```

## Research (`research/`)

```
research/
├── README.md                   # Research documentation
├── competitors/                # Competitor analysis
│   ├── competitor_analysis.xlsx
│   ├── top_sellers.md
│   └── screenshots/
├── keywords/                   # Keyword research
│   ├── primary_keywords.md
│   ├── long_tail_keywords.md
│   └── keyword_performance.xlsx
├── pricing/                    # Pricing strategy
│   ├── pricing_calculator.xlsx
│   └── pricing_strategy.md
└── trends/                     # Market trends
    ├── search_trends.md
    └── opportunity_gaps.md
```

## Output (`output/`)

```
output/
├── README.md                   # Output management guide
├── puzzles/                    # Generated puzzles (JSON)
│   ├── beginner/              # Easy puzzles
│   ├── intermediate/          # Medium puzzles
│   └── expert/                # Hard puzzles
├── books/                      # Complete book files
│   ├── interiors/             # Interior PDFs
│   ├── covers/                # Cover PDFs
│   └── final/                 # Final, ready-to-upload books
├── previews/                   # Preview images for Amazon
└── marketing/                  # Marketing materials
```

## KDP Listings (`kdp/`)

```
kdp/
├── README.md                   # KDP listing guide
├── metadata/                   # Book metadata
│   └── {book_title}_metadata.json
├── descriptions/               # Product descriptions
│   └── {book_title}_description.md
├── keywords/                   # Backend keywords
│   └── {book_title}_keywords.txt
└── categories/                 # Category selections
    └── category_strategy.md
```

## Documentation (`docs/`)

```
docs/
├── kdp_niche_research_2026.md  # Market research report
├── kakurov2.py                 # Original prototype code
├── api/                        # API documentation
├── guides/                     # User guides
│   ├── puzzle_generation.md
│   ├── pdf_creation.md
│   └── kdp_publishing.md
└── examples/                   # Code examples
    ├── generate_puzzle.py
    └── create_pdf.py
```

## Configuration (`config/`)

```
config/
├── default_config.yaml         # Default configuration
├── book_specs/                 # Book specifications
│   ├── beginner_spec.yaml
│   ├── intermediate_spec.yaml
│   └── expert_spec.yaml
└── difficulty_profiles/        # Difficulty calibration
    └── difficulty_settings.yaml
```

## Data (`data/`)

```
data/
├── generated_puzzles/          # Puzzle database
├── puzzle_cache/               # Cached puzzles for reuse
└── analytics/                  # Performance analytics
    └── sales_data.xlsx
```

## Scripts (`scripts/`)

```
scripts/
├── batch_generation/           # Batch processing scripts
│   ├── generate_puzzles.py    # Generate puzzle batches
│   ├── create_interior.py     # Create interior PDFs
│   └── create_cover.py        # Cover generation
├── quality_control/            # QA scripts
│   ├── validate_book.py       # Book validation
│   └── check_kdp_compliance.py
└── deployment/                 # Deployment scripts
    └── prepare_upload.py      # Prepare for KDP upload
```

## Portfolio (`portfolio/`)

```
portfolio/
├── README.md                   # Portfolio management guide
├── published/                  # Live books on Amazon
│   └── {book_title}/
│       ├── book_info.json
│       ├── sales_data.xlsx
│       └── reviews.md
├── in_progress/                # Books in development
│   └── {book_title}/
│       ├── project_plan.md
│       └── progress.md
└── planned/                    # Future book ideas
    └── {book_idea}.md
```

## OpenSpec (`openspec/`)

```
openspec/
├── AGENTS.md                   # AI assistant instructions
├── project.md                  # Project context and conventions
├── specs/                      # Current specifications
└── changes/                    # Proposed changes
```

## Total Structure

- **52 directories** organized by function
- **Separation of concerns**: Code, assets, output, research, documentation
- **Scalable**: Easy to add new books, features, and tools
- **Professional**: Follows industry best practices
- **KDP-optimized**: Aligned with Amazon publishing workflow

## Key Principles

1. **Modularity**: Each directory has a single, clear purpose
2. **Documentation**: README files in all major directories
3. **Automation**: Scripts for repetitive tasks
4. **Quality**: Validation and testing at every stage
5. **Scalability**: Structure supports portfolio growth

## Navigation Tips

- Start with root `README.md` for project overview
- Check `SETUP_GUIDE.md` for installation
- Review `PROJECT_STATUS.md` for current progress
- Read directory-specific README files for details
- Use `openspec/project.md` for architectural context

---

**This structure supports the complete workflow from puzzle generation to KDP publishing.**

