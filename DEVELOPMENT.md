# Development Guidelines

This document outlines the development workflow, git practices, and coding standards for the Kakuro Puzzle Book Generator project.

## Table of Contents
- [Git Workflow](#git-workflow)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Code Standards](#code-standards)
- [Testing](#testing)

---

## Git Workflow

This project uses a **simplified GitHub Flow** optimized for solo development:

### Branch Structure

```
main (production-ready)
  └── develop (integration branch)
       ├── feature/puzzle-generator
       ├── feature/pdf-layout
       └── fix/grid-rendering
```

### Branches

- **`main`** - Production-ready code only. Always stable and deployable.
- **`develop`** - Integration branch where features come together. Test here before merging to main.
- **Feature branches** - Short-lived branches for specific features or fixes.

### Workflow Steps

1. **Start new work:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit regularly:**
   ```bash
   git add .
   git commit -m "feat: add puzzle difficulty scoring"
   ```

3. **Push to remote:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request** (even for solo work - good for documentation)
   - PR from `feature/your-feature-name` → `develop`
   - Review your own changes
   - Merge when tests pass

5. **Periodic releases:**
   - PR from `develop` → `main`
   - Tag with version number
   - Deploy/publish

---

## Branch Naming

Use descriptive, lowercase names with hyphens:

### Format
```
<type>/<short-description>
```

### Types
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `refactor/` - Code restructuring without changing behavior
- `docs/` - Documentation updates
- `test/` - Adding or updating tests
- `chore/` - Maintenance, dependencies, tooling

### Examples
```
feature/pdf-generation
feature/difficulty-calibration
fix/grid-alignment-issue
refactor/puzzle-generator-cleanup
docs/api-documentation
test/puzzle-validation-suite
chore/update-dependencies
```

### Rules
- Keep names short but descriptive (max 50 chars)
- Use hyphens, not underscores or spaces
- Be specific: `feature/add-clue-validation` not `feature/validation`
- Delete branches after merging

---

## Commit Messages

Follow **Conventional Commits** specification for consistency and tooling support.

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style/formatting (no logic change)
- `refactor:` - Code restructuring
- `test:` - Adding or updating tests
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks
- `build:` - Build system or dependencies
- `ci:` - CI/CD changes

### Scope (optional)
The area of codebase affected: `puzzle`, `pdf`, `layout`, `validation`, etc.

### Examples

**Good commits:**
```
feat(puzzle): add difficulty scoring algorithm
fix(pdf): correct grid alignment on A4 pages
docs: update README with installation instructions
refactor(generator): simplify backtracking logic
test(validation): add tests for puzzle solvability
chore: update dependencies to latest versions
```

**Bad commits:**
```
update stuff
fixed bug
WIP
asdf
changes
```

### Commit Message Rules

1. **Subject line:**
   - Use imperative mood ("add" not "added" or "adds")
   - Don't capitalize first letter after type
   - No period at the end
   - Max 72 characters

2. **Body (optional but recommended for complex changes):**
   - Explain WHAT and WHY, not HOW
   - Wrap at 72 characters
   - Separate from subject with blank line

3. **Footer (optional):**
   - Reference issues: `Closes #123`
   - Breaking changes: `BREAKING CHANGE: description`

### Example with body:
```
feat(pdf): implement ReportLab PDF generation

Replace matplotlib-based PDF generation with ReportLab for
professional print quality. This provides better control over
fonts, spacing, and PDF/X-1a compliance for KDP publishing.

- Add font management system
- Implement page templates
- Support custom page sizes
```

---

## Pull Requests

Even as a solo developer, use PRs for documentation and self-review.

### PR Title Format
Same as commit messages:
```
feat(puzzle): add difficulty calibration system
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation
- [ ] Testing

## Changes Made
- Bullet point list of changes

## Testing
- How was this tested?
- What test cases were added?

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented if present)
```

### PR Workflow
1. Create PR from feature branch to `develop`
2. Review your own code (fresh eyes catch issues!)
3. Ensure tests pass
4. Merge using "Squash and merge" for clean history
5. Delete feature branch

---

## Code Standards

### Python Style
- Follow **PEP 8** style guide
- Use **Black** for formatting (already installed)
- Use **flake8** for linting
- Use **mypy** for type checking

### Type Hints
Always use type hints:
```python
def generate_puzzle(size: int, difficulty: str) -> Puzzle:
    """Generate a Kakuro puzzle.
    
    Args:
        size: Grid size (e.g., 10 for 10x10)
        difficulty: One of 'easy', 'medium', 'hard'
        
    Returns:
        Generated Puzzle object
    """
    pass
```

### Docstrings
Use Google-style docstrings for all public functions and classes.

### File Organization
- One class per file (generally)
- Group related functions in modules
- Keep files under 500 lines

---

## Testing

### Test Requirements
- Write tests for all new features
- Maintain 80%+ code coverage
- Run tests before committing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_generator.py

# Run with verbose output
pytest -v
```

### Test Organization
```
tests/
  ├── unit/           # Unit tests (fast, isolated)
  ├── integration/    # Integration tests (slower)
  └── fixtures/       # Test data and fixtures
```

### Test Naming
```python
def test_puzzle_generator_creates_valid_grid():
    """Test that generator creates a valid grid structure."""
    pass

def test_difficulty_scorer_handles_edge_cases():
    """Test difficulty scoring with edge cases."""
    pass
```

---

## Quick Reference

### Daily Workflow
```bash
# Start work
git checkout develop
git pull
git checkout -b feature/my-feature

# Work and commit
git add .
git commit -m "feat: add feature"

# Push and create PR
git push origin feature/my-feature
# Create PR on GitHub

# After merge
git checkout develop
git pull
git branch -d feature/my-feature
```

### Before Committing
```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Run tests
pytest

# Type check
mypy src/
```

---

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

