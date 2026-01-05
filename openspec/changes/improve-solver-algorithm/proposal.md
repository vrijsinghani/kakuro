# Proposal: Improve Solver Algorithm with CSP Heuristics

**Change ID:** `improve-solver-algorithm`  
**Status:** Proposed  
**Created:** 2026-01-05  
**Author:** AI Agent

## Why

### Problem Statement
The current backtracking solver works well for small puzzles (7x7, 9x9) but becomes impractically slow for larger grids (12x12, 15x15) with low black density. The solver can take minutes or hang indefinitely when generating expert/master difficulty puzzles.

### Root Cause
The naive backtracking algorithm:
- Tries cells in sequential order (no heuristics)
- Doesn't eliminate invalid values early (no forward checking)
- Doesn't propagate constraints (no constraint propagation)
- Results in exponential search space for complex puzzles

### Business Impact
- Cannot generate expert/master difficulty puzzles reliably
- Limits product portfolio to beginner/intermediate only
- Reduces market competitiveness
- Blocks KDP publishing timeline

## What

### Proposed Solution
Implement industry-standard Constraint Satisfaction Problem (CSP) heuristics:

1. **MRV (Minimum Remaining Values)** - Choose the cell with fewest valid options first
2. **Forward Checking** - Eliminate invalid values from neighboring cells after each placement
3. **Constraint Propagation** - Propagate constraints through the grid to reduce search space

### Expected Performance Improvement
- **7x7 puzzles:** ~same speed (already fast)
- **9x9 puzzles:** 2-5x faster
- **12x12 puzzles:** 10-50x faster (from minutes to seconds)
- **15x15 puzzles:** 50-100x faster (from hanging to solvable)

### Technical Approach
1. Add domain tracking for each cell (valid digits 1-9)
2. Implement MRV cell selection
3. Add forward checking to update domains
4. Add constraint propagation for run constraints
5. Maintain backward compatibility with existing API

## Impact

### Files to Modify
- `src/puzzle_generation/solver.py` - Core solver implementation
- `tests/puzzle_generation/test_solver.py` - Add performance tests

### Files to Create
- `benchmarks/solver_performance.py` - Performance benchmarking script

### Breaking Changes
None - API remains the same, only internal implementation changes

### Dependencies
No new dependencies required

## Success Criteria

1. **Performance Benchmarks**
   - 9x9 puzzle solves in < 0.1 seconds
   - 12x12 puzzle solves in < 1 second
   - 15x15 puzzle solves in < 5 seconds

2. **Correctness**
   - All existing tests pass
   - Generated puzzles have unique solutions
   - No regressions in puzzle quality

3. **Code Quality**
   - Type hints on all new functions
   - Comprehensive test coverage
   - Clear documentation of algorithm

## Timeline

- **Estimated Effort:** 4-6 hours
- **Target Completion:** Within 2 days

## Alternatives Considered

1. **Timeout-based approach** - Rejected: Doesn't solve the problem, just fails faster
2. **Different solver algorithm (Dancing Links)** - Deferred: More complex, MRV should be sufficient
3. **Pre-computed lookup tables** - Rejected: Memory intensive, doesn't scale

## References

- [Constraint Satisfaction Problems - Russell & Norvig AI textbook](https://aima.cs.berkeley.edu/)
- [MRV Heuristic](https://en.wikipedia.org/wiki/Minimum_remaining_value)
- [Forward Checking](https://en.wikipedia.org/wiki/Look-ahead_(backtracking))

