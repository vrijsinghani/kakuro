# Kakuro Puzzle Book Generator for Amazon KDP

Automated system for generating professional, print-ready Kakuro puzzle books for publication on Amazon Kindle Direct Publishing (KDP).

## Project Overview

This project capitalizes on a high-demand, low-competition market opportunity: **Kakuro puzzle books**. With ~36,635 monthly searches and exceptionally few existing books on Amazon, Kakuro represents an ideal niche for KDP publishing.

## Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Git workflow, commit conventions, and coding standards
- **[.github/GIT_CHEATSHEET.md](.github/GIT_CHEATSHEET.md)** - Quick reference for common git operations
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current project status and roadmap
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Development environment setup instructions

### What is Kakuro?

Kakuro is a logic puzzle that combines elements of crosswords and Sudoku. Players fill white cells with digits 1-9 such that each "run" (horizontal or vertical sequence) sums to a given clue number, with no repeated digits within a run.

### Business Goals

- Generate high-quality Kakuro puzzle books in multiple difficulty levels
- Create large-format collections (500-1000+ puzzles per book)
- Target diverse audiences (adults, seniors, beginners, experts)
- Automate the entire workflow from puzzle generation to print-ready PDF
- Build a profitable portfolio of puzzle books on Amazon KDP

## Features

### Puzzle Generation
- ✅ Mathematically valid puzzles with unique solutions
- ✅ Difficulty calibration (Beginner, Intermediate, Expert)
- ✅ Customizable grid sizes and complexity
- ✅ Automated validation and quality checks
- ✅ Batch generation for large collections

### Premium PDF Output
- ✅ ReportLab-based PDF generation for professional quality
- ✅ PDF/X-1a:2001 compliance for print production
- ✅ Embedded fonts for consistent rendering
- ✅ CMYK color mode for accurate printing
- ✅ Precise layout control with proper margins and bleed

### Book Assembly
- ✅ Multi-page document assembly
- ✅ Instruction pages ("How to Play")
- ✅ Solution sections with clear formatting
- ✅ Large-print layouts for seniors
- ✅ Professional typography and styling

### KDP Optimization
- ✅ Correct trim sizes (8.5"×11", 8"×10", 7"×10")
- ✅ Proper margins and bleed settings
- ✅ Cover dimension calculator (based on page count)
- ✅ Metadata templates for listings
- ✅ Keyword research and optimization

## Tech Stack

- **Python 3.9+** - Core programming language
- **ReportLab** - Premium PDF generation
- **Pillow (PIL)** - Image processing
- **NumPy** - Numerical operations (optional)
- **pytest** - Testing framework

## Project Structure

```
kakuro/
├── src/                    # Source code
│   ├── puzzle_generation/  # Puzzle generation algorithms
│   ├── pdf_generation/     # ReportLab PDF creation
│   ├── layout/             # Visual layout and rendering
│   ├── utils/              # Shared utilities
│   └── validation/         # Quality assurance
├── tests/                  # Unit and integration tests
├── assets/                 # Fonts, images, templates
├── research/               # Market research and analysis
├── output/                 # Generated puzzles and books
├── kdp/                    # KDP listing metadata
├── docs/                   # Documentation
├── config/                 # Configuration files
├── scripts/                # Automation scripts
└── portfolio/              # Published book tracking
```

See individual README files in each directory for detailed information.

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd kakuro
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download fonts (see `assets/fonts/README.md`)

### Generate Your First Puzzle

```bash
python -c "from src.puzzle_generation.generator import generate_kakuro; print(generate_kakuro())"
```

### Generate a Complete Book

```bash
# Build the example book
python -m src.book_builder build beginner-to-expert-250

# See src/book_builder/README.md for creating your own books.
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Format code with:

```bash
black src/ tests/
flake8 src/ tests/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement feature with tests
3. Update documentation
4. Submit pull request

## Documentation

- **OpenSpec**: See `openspec/project.md` for project conventions and architecture
- **Market Research**: See `research/README.md` and `docs/kdp_niche_research_2026.md`
- **API Documentation**: See `docs/api/`
- **User Guides**: See `docs/guides/`

## Roadmap

### Phase 1: Core Functionality (Current)
- [x] Basic puzzle generation algorithm
- [x] ReportLab PDF generation
- [x] Interior page layouts
- [x] Solution page generation
- [ ] Instruction page templates

### Phase 2: Quality & Automation
- [ ] Difficulty calibration system
- [ ] Automated validation pipeline
- [ ] Batch generation scripts
- [ ] KDP compliance checker
- [ ] Cover template system

### Phase 3: Portfolio Expansion
- [ ] Multiple book series (Beginner, Intermediate, Expert)
- [ ] Large-print editions for seniors
- [ ] Themed collections
- [ ] Multi-language support

### Phase 4: Advanced Features
- [ ] Web-based puzzle previewer
- [ ] Analytics dashboard for sales tracking
- [ ] Automated KDP upload (via API if available)
- [ ] A/B testing for covers and descriptions

## Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## License

[Specify your license here]

## Resources

### KDP Publishing
- [KDP Help Center](https://kdp.amazon.com/help)
- [KDP Community Forums](https://kdpcommunity.amazon.com)
- [KDP Print Specifications](https://kdp.amazon.com/help/topic/G201834180)

### Puzzle Design
- Kakuro rules and strategies
- Logic puzzle design principles
- Difficulty calibration techniques

### Market Research
- Amazon Best Sellers: Puzzles & Games
- Google Trends: Puzzle search patterns
- Competitor analysis tools

## Contact

Vikas Rijsinghani
vikasrij@gmail.com


---

**Note**: This is a commercial project for Amazon KDP publishing. All generated content is intended for sale on Amazon's platform.

