# Agent Context - Kakuro Project

> **For project status, current tasks, and roadmap:** See `PROJECT_STATUS.md`

## Quick Overview
This is a **Kakuro Puzzle Book Generator** for Amazon KDP publishing. Solo developer project using Python, ReportLab for PDF generation, and targeting PDF/X-1a compliance for print-on-demand.

## Technical Environment
- **Python:** 3.10.12
- **Package Manager:** `uv` (use `uv pip install` for dependencies)
- **Primary Libraries:** ReportLab (PDF), Pillow (images), NumPy (numerical)

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
├── src/                    # Source code (empty - needs implementation)
│   ├── puzzle_generation/  # Puzzle generation logic
│   ├── pdf_generation/     # ReportLab PDF creation
│   └── utils/              # Utilities
├── docs/
│   └── kakurov2.py         # EXISTING working puzzle generator (needs migration)
├── assets/
│   └── fonts/              # Commercial fonts (Roboto, Open Sans, Noto Sans)
├── tests/                  # Unit tests (empty)
├── config/                 # Configuration files
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
2. **Follow PEP 8** style guide
3. **Write tests** for all new features (target 80%+ coverage)
4. **Add type hints** to all functions
5. **Write docstrings** for all public functions/classes
6. **Fonts are commercial-use licensed** - verified for KDP publishing

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

