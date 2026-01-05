# Tasks: Improve Solver Algorithm

**Change ID:** `improve-solver-algorithm`  
**Status:** Not Started  
**Created:** 2026-01-05

## 1. Domain Tracking
- [ ] 1.1 Add `CellDomain` class to track valid digits for each cell
- [ ] 1.2 Initialize domains for all empty cells (1-9)
- [ ] 1.3 Add domain update methods (remove value, restore value)
- [ ] 1.4 Add domain query methods (get valid values, count remaining)

## 2. MRV Heuristic
- [ ] 2.1 Implement `select_mrv_cell()` function
- [ ] 2.2 Find cell with minimum remaining values
- [ ] 2.3 Handle tie-breaking (use degree heuristic or first found)
- [ ] 2.4 Add tests for MRV cell selection

## 3. Forward Checking
- [ ] 3.1 Implement `forward_check()` function
- [ ] 3.2 Update domains of cells in same horizontal run
- [ ] 3.3 Update domains of cells in same vertical run
- [ ] 3.4 Track domain changes for backtracking
- [ ] 3.5 Add tests for forward checking

## 4. Constraint Propagation
- [ ] 4.1 Implement `propagate_constraints()` function
- [ ] 4.2 Check run sum constraints
- [ ] 4.3 Check uniqueness constraints within runs
- [ ] 4.4 Eliminate impossible values based on remaining sum
- [ ] 4.5 Add tests for constraint propagation

## 5. Integrate with Backtracking
- [ ] 5.1 Update `_backtrack()` to use MRV for cell selection
- [ ] 5.2 Update `_backtrack()` to use forward checking
- [ ] 5.3 Update `_backtrack()` to propagate constraints
- [ ] 5.4 Handle domain restoration on backtrack
- [ ] 5.5 Maintain backward compatibility with existing API

## 6. Testing
- [ ] 6.1 Verify all existing tests still pass
- [ ] 6.2 Add unit tests for domain tracking
- [ ] 6.3 Add unit tests for MRV selection
- [ ] 6.4 Add unit tests for forward checking
- [ ] 6.5 Add unit tests for constraint propagation
- [ ] 6.6 Add integration tests for full solver

## 7. Performance Benchmarking
- [ ] 7.1 Create `benchmarks/solver_performance.py` script
- [ ] 7.2 Benchmark 7x7 puzzles (baseline)
- [ ] 7.3 Benchmark 9x9 puzzles (should be 2-5x faster)
- [ ] 7.4 Benchmark 12x12 puzzles (should be 10-50x faster)
- [ ] 7.5 Benchmark 15x15 puzzles (should be 50-100x faster)
- [ ] 7.6 Compare old vs new solver performance
- [ ] 7.7 Document performance improvements

## 8. Documentation
- [ ] 8.1 Add docstrings to all new functions
- [ ] 8.2 Document algorithm in solver.py module docstring
- [ ] 8.3 Add inline comments for complex logic
- [ ] 8.4 Update README with performance characteristics

## 9. Code Quality
- [ ] 9.1 Add type hints to all new functions
- [ ] 9.2 Run black formatter
- [ ] 9.3 Run flake8 linter
- [ ] 9.4 Run mypy type checker
- [ ] 9.5 Ensure all quality checks pass

## 10. Validation
- [ ] 10.1 Generate 10 puzzles of each difficulty level
- [ ] 10.2 Verify all puzzles solve correctly
- [ ] 10.3 Verify solution uniqueness
- [ ] 10.4 Verify no regressions in puzzle quality
- [ ] 10.5 Test with example scripts

## Status Summary
- **Completed:** 0/50 tasks (0%)
- **Remaining:** 50 tasks
- **Estimated Effort:** 4-6 hours
- **Target:** Complete within 2 days

