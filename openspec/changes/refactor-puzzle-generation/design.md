# Design: Refactor Puzzle Generation

## Context

The existing `docs/kakurov2.py` is a working prototype that successfully generates valid Kakuro puzzles using:
- Grid generation with random black cell placement
- Run computation (horizontal and vertical sequences)
- Backtracking solver with constraint validation
- Matplotlib-based rendering

However, it's a monolithic script (~187 lines) that mixes concerns and lacks production-ready features like type safety, testing, and modularity.

### Constraints
- Must preserve existing algorithm logic (it works!)
- Must maintain puzzle validity guarantees
- Must support future extensions (difficulty scoring, batch generation)
- Must follow project conventions (PEP 8, type hints, docstrings)

### Stakeholders
- Solo developer (immediate user)
- Future maintainers (code must be self-documenting)
- KDP publishing pipeline (reliable puzzle generation)

## Goals / Non-Goals

### Goals
- ✅ Modular architecture with clear separation of concerns
- ✅ Type-safe code with comprehensive type hints
- ✅ Testable components with 80%+ coverage
- ✅ Clean public API for puzzle generation
- ✅ Preserve existing algorithm correctness
- ✅ Remove rendering concerns from core logic
- ✅ Support configuration-driven generation

### Non-Goals
- ❌ Changing the core algorithm (backtracking solver)
- ❌ Adding new features (difficulty scoring, batch generation) - separate changes
- ❌ Implementing PDF generation - separate module
- ❌ Performance optimization - defer until profiling shows need
- ❌ Alternative solving algorithms - future enhancement

## Decisions

### Decision 1: Module Structure
**Choice**: Separate modules for generator, solver, runs, and models

**Rationale**:
- **Single Responsibility**: Each module has one clear purpose
- **Testability**: Can test each component independently
- **Extensibility**: Easy to add alternative implementations
- **Maintainability**: Changes to one concern don't affect others

**Alternatives Considered**:
- Single `generator.py` file: Too large, mixes concerns
- Class-based architecture: Overkill for functional algorithms
- Separate packages: Over-engineering for current scope

### Decision 2: Data Structures
**Choice**: Use dataclasses for Grid, Run, and Puzzle

**Rationale**:
- **Type Safety**: Dataclasses provide automatic type checking
- **Immutability**: Can use `frozen=True` for puzzle state
- **Clarity**: Named fields better than tuples/lists
- **Validation**: Can add `__post_init__` validation

**Structure**:
```python
@dataclass
class Grid:
    height: int
    width: int
    cells: List[List[int]]  # -1=black, 0=empty, 1-9=filled

@dataclass
class Run:
    row: int
    col: int
    length: int
    total: int
    direction: Direction  # HORIZONTAL or VERTICAL

@dataclass
class Puzzle:
    grid: Grid
    horizontal_runs: List[Run]
    vertical_runs: List[Run]
```

**Alternatives Considered**:
- Keep list-based representation: Less type-safe, harder to understand
- Use NumPy arrays: Overkill, adds dependency for simple 2D grids
- Use classes with methods: More complex than needed

### Decision 3: Solver Integration
**Choice**: Solver is a separate module called by generator

**Rationale**:
- **Separation**: Generation and solving are distinct concerns
- **Reusability**: Solver can be used independently (e.g., for validation)
- **Testing**: Can test solver with known puzzles
- **Future**: Can add alternative solvers without changing generator

**Flow**:
```
Generator → Creates grid with black cells
         → Computes runs
         → Calls Solver to validate/fill
         → Returns Puzzle if solvable, else retry
```

### Decision 4: Error Handling
**Choice**: Custom exception hierarchy

**Exceptions**:
- `PuzzleGenerationError` - Base exception
  - `InvalidGridError` - Grid constraints violated
  - `UnsolvableError` - No valid solution found
  - `SolverTimeoutError` - Solver exceeded time limit

**Rationale**:
- **Clarity**: Specific exceptions communicate intent
- **Handling**: Caller can catch specific errors
- **Debugging**: Better error messages with context

### Decision 5: Configuration
**Choice**: Use YAML config with dataclass-based settings

**Config Structure**:
```yaml
puzzle_generation:
  default_size: [9, 9]
  black_density_range: [0.18, 0.25]
  min_run_length: 2
  max_run_length: 9
  solver_timeout_seconds: 30
  max_generation_attempts: 10
```

**Rationale**:
- **Flexibility**: Easy to adjust without code changes
- **Consistency**: Matches existing `config/default_config.yaml`
- **Validation**: Can validate config on load

## Risks / Trade-offs

### Risk 1: Over-engineering
**Risk**: Creating too many abstractions for simple code
**Mitigation**: 
- Keep modules focused and small (<200 lines each)
- Use functions over classes where appropriate
- Only add abstractions when needed for testing/extension

### Risk 2: Breaking existing algorithm
**Risk**: Refactoring introduces bugs in working code
**Mitigation**:
- Preserve original `docs/kakurov2.py` as reference
- Write tests that verify same behavior
- Test with known-good puzzles from original code

### Risk 3: Performance regression
**Risk**: Modular code might be slower than monolithic version
**Mitigation**:
- Profile before and after refactoring
- Defer optimization until proven necessary
- Target: <1 second per puzzle (same as original)

### Trade-off: Type Safety vs. Simplicity
**Trade-off**: Type hints add verbosity
**Decision**: Accept verbosity for better IDE support and error catching
**Rationale**: Long-term maintainability outweighs short-term convenience

## Migration Plan

### Phase 1: Create Structure (No Breaking Changes)
1. Create new modules in `src/puzzle_generation/`
2. Keep `docs/kakurov2.py` unchanged
3. No external dependencies yet

### Phase 2: Migrate Core Logic
1. Copy and refactor `generate_kakuro()` → `generator.py`
2. Copy and refactor `solve_kakuro()` → `solver.py`
3. Copy and refactor `compute_runs()` → `runs.py`
4. Add type hints and docstrings

### Phase 3: Add Tests
1. Write unit tests for each module
2. Write integration tests for full generation
3. Verify behavior matches original

### Phase 4: Create Public API
1. Design clean API in `__init__.py`
2. Add convenience functions
3. Document usage examples

### Rollback Plan
If refactoring fails or introduces critical bugs:
- Keep using `docs/kakurov2.py` for generation
- Fix issues in new code without time pressure
- No production impact (no existing production code)

## Open Questions

1. **Q**: Should we support custom random seeds for reproducibility?
   **A**: Yes - add `seed: Optional[int]` parameter to `generate_puzzle()`

2. **Q**: Should we cache generated puzzles to avoid regeneration?
   **A**: Defer to future optimization - not needed for MVP

3. **Q**: Should we validate puzzle difficulty during generation?
   **A**: No - difficulty scoring is a separate feature (future change)

4. **Q**: Should we support puzzle serialization (save/load)?
   **A**: Yes - add `to_dict()` and `from_dict()` methods to Puzzle class

