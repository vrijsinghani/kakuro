#!/bin/bash
# Setup git hooks for the Kakuro project
# Run this script once after cloning the repository

set -e

HOOKS_DIR=".git/hooks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Setting up git hooks for Kakuro project..."

# Create pre-commit hook
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook for Kakuro project

echo "🔍 Running pre-commit checks..."

# Check if Python files are being committed (exclude third-party fonts)
PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | grep -v '^assets/fonts/' || true)

if [ -n "$PYTHON_FILES" ]; then
    echo "📝 Formatting Python files with Black..."
    black $PYTHON_FILES
    
    echo "🔎 Linting with flake8..."
    if ! flake8 $PYTHON_FILES; then
        echo "❌ Linting failed. Please fix the issues above."
        exit 1
    fi
    
    echo "🔤 Type checking with mypy..."
    if ! mypy $PYTHON_FILES; then
        echo "⚠️  Type checking found issues. Consider fixing them."
        # Don't fail on mypy errors for now, just warn
    fi
    
    # Re-add files that were formatted
    git add $PYTHON_FILES
fi

echo "✅ Pre-commit checks passed!"
EOF

# Create commit-msg hook
cat > "$HOOKS_DIR/commit-msg" << 'EOF'
#!/bin/bash
# Commit message hook for Kakuro project
# Validates commit messages follow Conventional Commits format

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Regex for conventional commit format
CONVENTIONAL_COMMIT_REGEX="^(feat|fix|docs|style|refactor|test|perf|chore|build|ci)(\(.+\))?: .{1,72}"

if ! echo "$COMMIT_MSG" | grep -qE "$CONVENTIONAL_COMMIT_REGEX"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Commit message must follow Conventional Commits format:"
    echo "  <type>(<scope>): <subject>"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, test, perf, chore, build, ci"
    echo ""
    echo "Examples:"
    echo "  feat(puzzle): add difficulty scoring"
    echo "  fix(pdf): correct grid alignment"
    echo "  docs: update README"
    echo ""
    echo "Your message:"
    echo "  $COMMIT_MSG"
    exit 1
fi

# Check subject line length
SUBJECT_LINE=$(echo "$COMMIT_MSG" | head -n1)
if [ ${#SUBJECT_LINE} -gt 72 ]; then
    echo "⚠️  Warning: Subject line is longer than 72 characters"
    echo "Consider shortening it for better readability"
fi

echo "✅ Commit message format is valid"
EOF

# Make hooks executable
chmod +x "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/commit-msg"

echo "✅ Git hooks installed successfully!"
echo ""
echo "Installed hooks:"
echo "  - pre-commit: Formats code, runs linting and type checking"
echo "  - commit-msg: Validates commit message format"
echo ""
echo "To bypass hooks (not recommended):"
echo "  git commit --no-verify"

