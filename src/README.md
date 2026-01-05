# Source Code

This directory contains all the Python source code for the Kakuro puzzle book generation system.

## Directory Structure

### `puzzle_generation/`
Core puzzle generation algorithms and logic.
- Kakuro grid generation
- Constraint satisfaction solver (backtracking)
- Run computation (horizontal/vertical)
- Difficulty calibration
- Puzzle validation

**Key modules:**
- `generator.py` - Main puzzle generation engine
- `solver.py` - Backtracking solver for validation
- `difficulty.py` - Difficulty scoring and calibration
- `constraints.py` - Constraint validation logic

### `pdf_generation/`
Premium PDF creation using ReportLab.
- PDF/X-1a:2001 compliant output
- Font embedding and management
- Page layout and composition
- Multi-page document assembly

**Key modules:**
- `book_builder.py` - Main PDF assembly orchestrator
- `page_layouts.py` - Page templates (puzzle pages, solution pages, instruction pages)
- `styles.py` - Typography, colors, and styling definitions
- `pdf_utils.py` - Helper functions for PDF operations

### `layout/`
Visual layout and rendering of puzzle grids.
- Grid drawing with precise measurements
- Clue placement and formatting
- Solution visualization
- Large-print layouts for seniors

**Key modules:**
- `grid_renderer.py` - Puzzle grid drawing
- `clue_formatter.py` - Clue number placement and styling
- `solution_renderer.py` - Solution page generation
- `large_print.py` - Large-print specific layouts

### `utils/`
Shared utilities and helper functions.
- File I/O operations
- Configuration management
- Logging and debugging
- Common data structures

**Key modules:**
- `config.py` - Configuration loading and management
- `file_utils.py` - File operations (save, load, export)
- `logger.py` - Logging setup and utilities
- `constants.py` - Project-wide constants

### `validation/`
Quality assurance and validation.
- Puzzle solvability verification
- PDF compliance checking
- KDP specification validation
- Visual quality checks

**Key modules:**
- `puzzle_validator.py` - Puzzle correctness validation
- `pdf_validator.py` - PDF/X compliance checking
- `kdp_validator.py` - KDP specification validation
- `quality_checker.py` - Visual quality assessment

## Development Guidelines

### Adding New Features
1. Create feature branch from `main`
2. Add module to appropriate subdirectory
3. Write unit tests in `tests/unit/`
4. Update this README if adding new modules
5. Follow PEP 8 style guidelines

### Code Organization Principles
- **Separation of concerns**: Each module has a single, clear responsibility
- **Modularity**: Functions and classes should be reusable
- **Type hints**: Use Python type hints for better code clarity
- **Documentation**: Docstrings for all public functions and classes

### Import Conventions
```python
# Standard library imports
import os
from pathlib import Path

# Third-party imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image

# Local imports
from src.puzzle_generation.generator import generate_kakuro
from src.utils.config import load_config
```

## Testing
All source code should have corresponding tests in `tests/unit/` or `tests/integration/`.

Run tests with:
```bash
pytest tests/
```

## Dependencies
See `requirements.txt` in project root for all Python dependencies.

