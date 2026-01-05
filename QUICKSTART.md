# Quick Start Guide

Get up and running with the Kakuro project in minutes.

## First Time Setup

### 1. Install Git Hooks (Recommended)

```bash
./scripts/setup-git-hooks.sh
```

This installs hooks that will:
- Auto-format your code with Black
- Run linting checks before commits
- Validate commit message format

### 2. Verify Environment

```bash
# Check Python version (should be 3.10+)
python --version

# Verify all dependencies are installed
python -c "import reportlab, PIL, numpy; print('✓ All core dependencies installed')"

# Run tests (when available)
pytest
```

## Daily Workflow

### Starting New Work

```bash
# 1. Update develop branch
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Start coding!
```

### Making Commits

```bash
# 1. Check what changed
git status

# 2. Stage changes
git add .

# 3. Commit with conventional message
git commit -m "feat(puzzle): add new feature"

# Git hooks will automatically:
# - Format your code
# - Run linting
# - Validate commit message
```

### Common Commit Types

```bash
# New feature
git commit -m "feat(puzzle): add difficulty scoring"

# Bug fix
git commit -m "fix(pdf): correct grid alignment"

# Documentation
git commit -m "docs: update README"

# Refactoring
git commit -m "refactor(generator): simplify logic"

# Tests
git commit -m "test(validation): add solvability tests"

# Maintenance
git commit -m "chore: update dependencies"
```

### Finishing Work

```bash
# 1. Push to remote
git push origin feature/your-feature-name

# 2. Create Pull Request on GitHub
# - Review your own changes
# - Ensure tests pass
# - Merge when ready

# 3. Clean up
git checkout develop
git pull origin develop
git branch -d feature/your-feature-name
```

## Code Quality Checks

### Before Committing (Manual)

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/

# Run tests
pytest

# Check coverage
pytest --cov=src
```

### Auto-formatting

```bash
# Format all Python files
black .

# Check what would be formatted (dry run)
black --check .
```

## Common Tasks

### Generate a Puzzle

```bash
# (Once implemented)
python -m src.puzzle_generation.generator --size 10 --difficulty easy
```

### Create a PDF

```bash
# (Once implemented)
python -m src.pdf_generation.book_builder --puzzles 100 --output output/books/
```

### Run Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_generator.py

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v
```

### View Test Coverage

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Troubleshooting

### Git Hooks Not Working

```bash
# Re-run setup script
./scripts/setup-git-hooks.sh

# Check hooks are executable
ls -la .git/hooks/
```

### Commit Message Rejected

Make sure your message follows this format:
```
<type>(<scope>): <description>
```

Examples:
- `feat(puzzle): add scoring`
- `fix: correct bug`
- `docs: update guide`

### Code Formatting Issues

```bash
# Auto-fix with Black
black src/ tests/

# Then commit again
git add .
git commit -m "style: format code with black"
```

### Import Errors

```bash
# Reinstall dependencies
uv pip install -r requirements.txt

# Verify installation
python -c "import reportlab; print(reportlab.Version)"
```

## Useful Commands

### Git

```bash
# View commit history
git log --oneline --graph

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git checkout -- .

# View diff
git diff
```

### Python

```bash
# Run Python module
python -m src.module_name

# Interactive Python with project imports
python -i -c "from src.puzzle_generation import generator"

# Check installed packages
pip list
```

## Next Steps

1. **Read the full documentation:**
   - [DEVELOPMENT.md](DEVELOPMENT.md) - Complete development guidelines
   - [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current status and roadmap

2. **Set up your IDE:**
   - Configure Black as formatter
   - Enable flake8 linting
   - Set up mypy type checking

3. **Start coding:**
   - Check PROJECT_STATUS.md for next tasks
   - Create a feature branch
   - Write tests first (TDD)
   - Commit often with good messages

## Resources

- [Git Cheat Sheet](.github/GIT_CHEATSHEET.md)
- [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

## Getting Help

- Check existing documentation first
- Review git history for examples: `git log --oneline`
- Look at test files for usage examples
- Refer to the cheat sheets in `.github/`

---

**Happy coding! 🚀**

