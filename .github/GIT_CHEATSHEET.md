# Git Workflow Cheat Sheet

Quick reference for common git operations in this project.

## Starting New Work

```bash
# Update develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name
```

## Making Changes

```bash
# Check status
git status

# Stage changes
git add .                    # Stage all changes
git add src/file.py          # Stage specific file

# Commit with conventional commit message
git commit -m "feat(scope): description"
git commit -m "fix: bug description"
git commit -m "docs: update README"

# Push to remote
git push origin feature/your-feature-name
```

## Commit Message Quick Reference

```
feat:      New feature
fix:       Bug fix
docs:      Documentation only
style:     Formatting, no code change
refactor:  Code restructuring
test:      Adding/updating tests
perf:      Performance improvement
chore:     Maintenance, dependencies
build:     Build system changes
ci:        CI/CD changes
```

## Syncing with Remote

```bash
# Pull latest changes
git pull origin develop

# Rebase feature branch on develop
git checkout feature/your-feature
git rebase develop

# Force push after rebase (use with caution)
git push origin feature/your-feature --force-with-lease
```

## Finishing Work

```bash
# Push final changes
git push origin feature/your-feature

# Create PR on GitHub (or merge locally)
# After PR is merged:

# Switch back to develop
git checkout develop
git pull origin develop

# Delete local feature branch
git branch -d feature/your-feature

# Delete remote feature branch (if not auto-deleted)
git push origin --delete feature/your-feature
```

## Useful Commands

```bash
# View commit history
git log --oneline --graph --all

# View changes
git diff                     # Unstaged changes
git diff --staged            # Staged changes

# Undo changes
git checkout -- file.py      # Discard changes in file
git reset HEAD file.py       # Unstage file
git reset --soft HEAD~1      # Undo last commit, keep changes
git reset --hard HEAD~1      # Undo last commit, discard changes

# Stash changes
git stash                    # Save changes temporarily
git stash pop                # Restore stashed changes
git stash list               # List all stashes

# View branches
git branch                   # Local branches
git branch -a                # All branches (local + remote)
git branch -d branch-name    # Delete local branch
```

## Pre-Commit Checklist

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
pytest --cov=src --cov-report=term-missing
```

## Branch Naming Examples

```
feature/pdf-generation
feature/difficulty-scoring
fix/grid-alignment
fix/font-loading-error
refactor/puzzle-generator
docs/api-documentation
test/validation-suite
chore/update-dependencies
```

## Commit Message Examples

```bash
# Good
git commit -m "feat(puzzle): add difficulty scoring algorithm"
git commit -m "fix(pdf): correct grid alignment on A4 pages"
git commit -m "docs: update installation instructions"
git commit -m "refactor(generator): simplify backtracking logic"
git commit -m "test(validation): add solvability tests"

# Bad (avoid these)
git commit -m "update"
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "changes"
```

## Emergency Fixes

```bash
# Made a mistake in last commit message
git commit --amend -m "new message"

# Forgot to add a file to last commit
git add forgotten-file.py
git commit --amend --no-edit

# Need to undo pushed commit (use with extreme caution)
git revert HEAD
git push origin branch-name
```

## Release Workflow

```bash
# Merge develop to main for release
git checkout main
git pull origin main
git merge develop

# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# Return to develop
git checkout develop
```

## Troubleshooting

```bash
# Merge conflict during pull
git status                   # See conflicted files
# Edit files to resolve conflicts
git add resolved-file.py
git commit -m "fix: resolve merge conflict"

# Accidentally committed to wrong branch
git log                      # Note the commit hash
git checkout correct-branch
git cherry-pick <commit-hash>
git checkout wrong-branch
git reset --hard HEAD~1

# Lost commits (find them)
git reflog                   # Shows all HEAD movements
git checkout <commit-hash>   # Recover lost commit
```

## Aliases (Optional)

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --oneline --graph --all --decorate
    amend = commit --amend --no-edit
```

Then use:
```bash
git st          # Instead of git status
git co develop  # Instead of git checkout develop
git visual      # Pretty commit graph
```

