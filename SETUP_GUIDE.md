# Kakuro Puzzle Book Generator - Setup Guide

Complete setup instructions for getting the Kakuro puzzle book generation system up and running.

## Prerequisites

### Required Software
- **Python 3.9 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** - Python package manager (included with Python)

### Optional Software
- **Visual Studio Code** - Recommended IDE
- **GIMP or Photoshop** - For cover design
- **Adobe Acrobat Reader** - For PDF validation

## Installation Steps

### 1. Clone or Download the Repository

```bash
# If using Git
git clone <repository-url>
cd kakuro

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Optional: Install development tools
pip install -e ".[dev]"

# Optional: Install graphics enhancement
pip install -e ".[graphics]"
```

### 4. Download Fonts

Free, commercially-licensed fonts are required for PDF generation.

**Recommended fonts:**

1. **Liberation Fonts** (Arial/Times New Roman alternatives)
   - Download: https://github.com/liberationfonts/liberation-fonts/releases
   - Extract to: `assets/fonts/liberation/`

2. **DejaVu Fonts** (Excellent Unicode coverage)
   - Download: https://dejavu-fonts.github.io/Download.html
   - Extract to: `assets/fonts/dejavu/`

3. **Roboto** (Modern sans-serif)
   - Download: https://fonts.google.com/specimen/Roboto
   - Extract to: `assets/fonts/roboto/`

**Directory structure:**
```
assets/fonts/
├── liberation/
│   ├── LiberationSans-Regular.ttf
│   ├── LiberationSans-Bold.ttf
│   ├── LiberationSerif-Regular.ttf
│   └── LiberationSerif-Bold.ttf
├── dejavu/
│   ├── DejaVuSans.ttf
│   └── DejaVuSans-Bold.ttf
└── roboto/
    ├── Roboto-Regular.ttf
    └── Roboto-Bold.ttf
```

### 5. Verify Installation

```bash
# Test Python imports
python -c "from reportlab.pdfgen import canvas; from PIL import Image; print('✓ All imports successful')"

# Run tests (if available)
pytest tests/ -v

# Check configuration
python -c "import yaml; yaml.safe_load(open('config/default_config.yaml')); print('✓ Configuration valid')"
```

## Configuration

### 1. Review Default Configuration

Edit `config/default_config.yaml` to customize:
- Puzzle generation settings
- PDF layout preferences
- KDP publishing defaults
- Output paths

### 2. Set Up Environment Variables (Optional)

Create `.env` file for sensitive information:

```bash
# .env
KDP_EMAIL=your-kdp-email@example.com
PUBLISHER_NAME=Your Publisher Name
AUTHOR_NAME=Your Author Name
```

### 3. Configure Logging

Create logs directory:
```bash
mkdir -p logs
```

## Quick Start

### Generate Your First Puzzle

```python
# test_puzzle.py
from src.puzzle_generation.generator import generate_kakuro

# Generate a simple puzzle
grid, h_runs, v_runs = generate_kakuro(h=9, w=9, black_density=0.22)

print("Puzzle generated successfully!")
print(f"Grid size: {len(grid)}x{len(grid[0])}")
print(f"Horizontal runs: {len(h_runs)}")
print(f"Vertical runs: {len(v_runs)}")
```

Run it:
```bash
python test_puzzle.py
```

### Generate a Batch of Puzzles

```bash
# Generate 10 beginner puzzles
python scripts/batch_generation/generate_puzzles.py \
  --difficulty beginner \
  --count 10 \
  --output output/puzzles/beginner/
```

### Create a PDF (Coming Soon)

```bash
# Create interior PDF from puzzles
python scripts/batch_generation/create_interior.py \
  --puzzles output/puzzles/beginner/ \
  --output output/books/interiors/ \
  --title "Kakuro Beginner 100"
```

## Project Structure Overview

```
kakuro/
├── src/                    # Source code
│   ├── puzzle_generation/  # Puzzle algorithms
│   ├── pdf_generation/     # PDF creation (ReportLab)
│   ├── layout/             # Visual layouts
│   ├── utils/              # Utilities
│   └── validation/         # Quality checks
├── assets/                 # Fonts, images, templates
├── config/                 # Configuration files
├── output/                 # Generated files
├── research/               # Market research
├── kdp/                    # KDP metadata
└── portfolio/              # Book tracking
```

## Next Steps

### 1. Explore the Documentation
- Read `openspec/project.md` for project architecture
- Review `docs/kdp_niche_research_2026.md` for market insights
- Check individual README files in each directory

### 2. Set Up Your First Book Project
- Choose difficulty level (beginner recommended)
- Decide on puzzle count (200-500 for first book)
- Plan cover design
- Prepare KDP metadata

### 3. Development Workflow
1. Generate puzzles
2. Validate puzzles
3. Create interior PDF
4. Design cover
5. Quality assurance
6. Prepare KDP listing
7. Publish!

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'reportlab'"**
- Solution: Activate virtual environment and run `pip install -r requirements.txt`

**Issue: "Font not found" error**
- Solution: Download fonts to `assets/fonts/` as described in step 4

**Issue: PDF generation fails**
- Solution: Check that all fonts are properly installed
- Verify `config/default_config.yaml` font paths

**Issue: Puzzle generation is slow**
- Solution: Reduce grid size or adjust `black_density` parameter
- Check `max_generation_attempts` in config

### Getting Help

- Check documentation in `docs/` directory
- Review example code in `docs/examples/`
- Open an issue on GitHub (if applicable)
- Consult ReportLab documentation: https://www.reportlab.com/docs/

## Development Tools

### Code Formatting
```bash
# Format code with Black
black src/ tests/

# Check code style
flake8 src/ tests/
```

### Type Checking
```bash
# Run mypy for type checking
mypy src/
```

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Resources

### KDP Publishing
- [KDP Help Center](https://kdp.amazon.com/help)
- [KDP Print Specifications](https://kdp.amazon.com/help/topic/G201834180)
- [KDP Community Forums](https://kdpcommunity.amazon.com)

### ReportLab Documentation
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [ReportLab API Reference](https://www.reportlab.com/docs/reportlab-reference.pdf)

### Python Resources
- [Python Official Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://pep8.org/)

## Support

For questions or issues:
1. Check this setup guide
2. Review project documentation
3. Search existing issues
4. Create a new issue with details

---

**Ready to start generating Kakuro puzzle books!** 🎉

