# Agent Context - Kakuro Project

> **For project status, current tasks, and roadmap:** See `PROJECT_STATUS.md`

## Quick Overview
This is a **Kakuro Puzzle Book Generator** for Amazon KDP publishing. Solo developer project using Python, ReportLab for PDF generation, and targeting PDF/X-1a compliance for print-on-demand.

## Current Session Status (2026-01-05)

### Recently Completed ✅
1. **Puzzle Generation Module** - Fully working with all difficulty levels
2. **CSP Solver Optimizations** - MRV, forward checking, backtrack limiting
3. **Strategic Grid Generation** - `max_run_length=7` to prevent exponentially hard puzzles

### Performance Achieved
| Difficulty | Grid | Density | Time |
|------------|------|---------|------|
| Beginner | 7x7 | 30% | 0.001s |
| Intermediate | 9x9 | 22% | 0.004s |
| Expert | 12x12 | 15% | 0.010s |
| Master | 15x15 | 12% | 0.019s |

### Next Priorities
1. **PDF Generation with ReportLab** - Design puzzle book layout, implement rendering
2. **Batch Generation Utilities** - Scripts for generating puzzle books
3. **Difficulty Calibration** - Scoring algorithm for puzzle difficulty

### Key Files Modified Recently
- `src/puzzle_generation/generator.py` - Added `_limit_run_lengths()` for strategic black cell placement
- `src/puzzle_generation/solver.py` - CSP optimizations (MRV, forward checking, domains)
- `docs/SOLVER_PERFORMANCE_ISSUE.md` - Analysis of solved performance issue
- `openspec/changes/improve-solver-algorithm/CURRENT_STATUS.md` - Solver improvement progress

### Unpushed Commits (develop branch)
Run `git log --oneline origin/develop..HEAD` to see commits ready to push.

## Technical Environment
- **Python:** 3.10.12
- **Package Manager:** `uv` (use `uv pip install` for dependencies)
- **Primary Libraries:** ReportLab (PDF), Pillow (images), NumPy (numerical)
- **Tests:** 80 tests passing (pytest)

## Git Workflow

### Branch Structure
```
main (production-ready releases)
  └── develop (integration branch - CURRENT)
       └── feature/* (feature branches)
```

### Commit Convention
**REQUIRED:** All commits MUST follow Conventional Commits format:
```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, perf, chore, build, ci
```

**Examples:**
- `feat(puzzle): add difficulty scoring algorithm`
- `fix(pdf): correct grid alignment issue`
- `docs: update README with setup instructions`
- `chore(deps): update reportlab to 4.0.1`

### Pre-commit Hooks (ACTIVE)
Git hooks are **installed and active** in `.git/hooks/`:

**Pre-commit hook:**
- Runs Black (code formatter)
- Runs flake8 (linter)
- Runs mypy (type checker - warnings only)
- **Excludes:** `assets/fonts/` directory (third-party code)

**Commit-msg hook:**
- Validates Conventional Commits format
- Enforces 72-character subject line limit

**To bypass hooks (NOT recommended):**
```bash
git commit --no-verify
```

### Important Git Rules
1. ✅ **Always commit to `develop` branch** (not `main`)
2. ✅ **Use feature branches** for major features: `git checkout -b feature/name`
3. ✅ **Follow commit conventions** - hooks will enforce this
4. ⚠️ **Ask before pushing** to remote
5. ⚠️ **Ask before merging** to `main`
6. ⚠️ **Ask before rebasing** or force-pushing

## Project Structure
```
kakuro/
├── src/
│   └── puzzle_generation/  # ✅ COMPLETE - Puzzle generation logic
│       ├── models.py       # Grid, Run, Puzzle dataclasses
│       ├── runs.py         # Run detection and computation
│       ├── solver.py       # CSP solver (MRV, forward checking)
│       ├── generator.py    # Puzzle generation with strategic grid layout
│       └── config.py       # YAML-based configuration
│   ├── pdf_generation/     # 🔜 NEXT - ReportLab PDF creation
│   └── utils/              # Utilities
├── tests/
│   └── puzzle_generation/  # ✅ 80 tests passing
├── config/
│   └── default_config.yaml # Difficulty profiles
├── docs/
│   └── SOLVER_PERFORMANCE_ISSUE.md  # Solved performance analysis
├── openspec/               # Change proposals and specs
│   └── changes/
│       ├── refactor-puzzle-generation/  # ✅ COMPLETE
│       └── improve-solver-algorithm/    # ✅ COMPLETE
├── assets/
│   └── fonts/              # Commercial fonts (Roboto, Open Sans, Noto Sans)
└── output/                 # Generated PDFs
```

## Development Environment

### Installing Dependencies
```bash
uv pip install -r requirements.txt
```

**Key dependencies:**
- ReportLab (PDF generation)
- Pillow (image processing)
- NumPy (numerical operations)
- pytest + pytest-cov (testing)
- black, flake8, mypy (code quality)

### Assets
- Commercial fonts in `assets/fonts/` (Roboto, Open Sans, Noto Sans)
- All fonts verified for commercial use in KDP publishing

## Key Documentation Files

- **PROJECT_STATUS.md** - **START HERE** - Current status, tasks, and roadmap
- **DEVELOPMENT.md** - Complete git workflow and coding standards
- **QUICKSTART.md** - Quick reference for daily workflow
- **.github/GIT_CHEATSHEET.md** - Git command reference
- **README.md** - Project overview

## Important Project Rules
1. **Use `uv pip install`** for all package management (not plain `pip`)
2. **Follow PEP 8** style guide (black, flake8 --max-line-length=88 --extend-ignore=E203)
3. **Write tests** for all new features (target 80%+ coverage)
4. **Add type hints** to all functions
5. **Write docstrings** for all public functions/classes
6. **Fonts are commercial-use licensed** - verified for KDP publishing
7. **OpenSpec workflow** - Use `openspec` for major changes (refactors, new features)

## Common Commands
```bash
# Daily workflow
git status                          # Check current state
git add <files>                     # Stage changes
git commit -m "type: message"       # Commit (hooks run automatically)
git log --oneline --graph -10       # View recent commits

# Running tests (when implemented)
pytest                              # Run all tests
pytest --cov=src                    # Run with coverage

# Code quality (manual)
black src/                          # Format code
flake8 src/                         # Lint code
mypy src/                           # Type check
```

## What NOT to Do

- ❌ Don't commit directly to `main`
- ❌ Don't push without asking
- ❌ Don't use `pip install` (use `uv pip install`)
- ❌ Don't edit font files in `assets/fonts/`
- ❌ Don't bypass pre-commit hooks without good reason
- ❌ Don't create new files unless necessary for the task

## Questions to Ask User

If starting a new task, clarify:

1. What task should I work on? (Check `PROJECT_STATUS.md` for priorities)
2. Do you want me to push commits to remote?
3. Should I create a feature branch or work on `develop`?
4. Any specific coding patterns or preferences to follow?

## Quick Start for New Session

```bash
# Check current state
git status
git log --oneline -5

# Run tests to verify everything works
python -m pytest tests/puzzle_generation/ -v --tb=short

# Test puzzle generation (all difficulties)
python -c "
from src.puzzle_generation.generator import generate_puzzle
for name, h, w, d in [('Beginner',7,7,0.30), ('Intermediate',9,9,0.22), ('Expert',12,12,0.15), ('Master',15,15,0.12)]:
    p = generate_puzzle(height=h, width=w, black_density=d)
    print(f'{name}: {len(p.horizontal_runs)}H/{len(p.vertical_runs)}V runs')
"
```

## Recent Architectural Decisions

1. **Max Run Length = 7**: Strategic black cell placement limits all runs to ≤7 cells, preventing exponentially hard search spaces. This was the key fix for 12x12+ puzzle generation.

2. **CSP Solver**: Uses MRV (Minimum Remaining Values) heuristic + forward checking. Constraint propagation infrastructure exists but is disabled during generation (run.total=0 during generation).

3. **Backtrack Limit = 500,000**: Prevents infinite loops on unsolvable grids. Generator retries with different random seed if limit exceeded.
