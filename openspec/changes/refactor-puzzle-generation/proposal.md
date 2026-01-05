# Change: Refactor Puzzle Generation to Production Structure

## Why

The existing Kakuro puzzle generation code in `docs/kakurov2.py` is a working prototype but needs to be refactored into a production-ready, modular structure to support:

1. **Maintainability** - Current monolithic script mixes concerns (generation, solving, rendering)
2. **Testability** - No unit tests; difficult to test individual components
3. **Extensibility** - Hard to add new features like difficulty scoring, batch generation, or alternative algorithms
4. **Code Quality** - Missing type hints, docstrings, and proper error handling
5. **Project Structure** - Code needs to move from `docs/` to proper `src/` package structure

This refactoring is the foundation for Phase 1 development and enables all subsequent features.

## What Changes

- **Migrate code** from `docs/kakurov2.py` to `src/puzzle_generation/` module structure
- **Separate concerns** into distinct modules:
  - `generator.py` - Grid generation and black cell placement
  - `solver.py` - Backtracking solver and validation
  - `runs.py` - Run computation and constraint management
  - `models.py` - Data structures (Grid, Run, Puzzle classes)
- **Add type hints** to all functions and classes
- **Write docstrings** following Google/NumPy style
- **Create unit tests** for each module (target 80%+ coverage)
- **Remove matplotlib dependency** from core logic (move to separate rendering module)
- **Add configuration** for puzzle parameters (size, density, difficulty)
- **Implement proper error handling** with custom exceptions
- **Add logging** for debugging and monitoring

## Impact

### Affected Specs
- **NEW**: `puzzle-generation` - Core puzzle generation capability (new spec)

### Affected Code
- **Created**: `src/puzzle_generation/generator.py` - Grid generation logic
- **Created**: `src/puzzle_generation/solver.py` - Constraint solver
- **Created**: `src/puzzle_generation/runs.py` - Run computation
- **Created**: `src/puzzle_generation/models.py` - Data structures
- **Created**: `src/puzzle_generation/__init__.py` - Public API
- **Created**: `tests/puzzle_generation/test_generator.py` - Generator tests
- **Created**: `tests/puzzle_generation/test_solver.py` - Solver tests
- **Created**: `tests/puzzle_generation/test_runs.py` - Run computation tests
- **Created**: `tests/puzzle_generation/test_models.py` - Model tests
- **Preserved**: `docs/kakurov2.py` - Keep as reference (not deleted)

### Breaking Changes
None - this is new production code, not modifying existing APIs.

### Migration Path
No migration needed - this is initial production implementation.

## Success Criteria

- [ ] All code moved to `src/puzzle_generation/` with proper module structure
- [ ] Type hints on all public functions and classes
- [ ] Docstrings on all public APIs
- [ ] Unit tests achieve 80%+ coverage
- [ ] All tests pass
- [ ] Code passes linting (flake8, black, mypy)
- [ ] Can generate valid Kakuro puzzles programmatically
- [ ] Puzzle validation confirms unique solutions
- [ ] No matplotlib dependency in core puzzle logic

## Timeline

**Estimated effort**: 8-12 hours
- Module structure and data models: 2 hours
- Core logic migration: 3-4 hours
- Testing: 3-4 hours
- Documentation and cleanup: 1-2 hours

**Target completion**: Within 1 week

