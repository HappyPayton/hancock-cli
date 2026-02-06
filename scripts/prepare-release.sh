#!/bin/bash

# Hancock Release Preparation Script
# This script helps prepare Hancock for release

set -e

echo "🚀 Hancock Release Preparation"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from hancock-cli root directory"
    exit 1
fi

# Get version from pyproject.toml
VERSION=$(grep "^version = " pyproject.toml | cut -d'"' -f2)
echo "📦 Current version: $VERSION"
echo ""

# Clean up
echo "🧹 Cleaning up..."
rm -rf build/ dist/ *.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "✓ Cleanup complete"
echo ""

# Run tests (if pytest is available)
if command -v pytest &> /dev/null; then
    echo "🧪 Running tests..."
    pytest || {
        echo "❌ Tests failed! Fix tests before releasing."
        exit 1
    }
    echo "✓ Tests passed"
    echo ""
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Hancock v${VERSION}"
    echo "✓ Git initialized"
    echo ""
fi

# Build package
echo "📦 Building package..."
python3 -m build || {
    echo "❌ Build failed!"
    echo "Install build tools: pip install build"
    exit 1
}
echo "✓ Package built"
echo ""

# Show package info
echo "📊 Package info:"
ls -lh dist/
echo ""

# Check if GitHub remote is set
if git remote get-url origin &> /dev/null; then
    echo "✓ GitHub remote configured"
    REPO_URL=$(git remote get-url origin)
    echo "  Repository: $REPO_URL"
else
    echo "⚠️  GitHub remote not configured yet"
    echo "  Run: git remote add origin https://github.com/USERNAME/hancock-signatures.git"
fi
echo ""

echo "✅ Release preparation complete!"
echo ""
echo "Next steps:"
echo "  1. Test the package: pip install dist/*.whl"
echo "  2. Create GitHub repo if not exists"
echo "  3. Push to GitHub: git push -u origin main"
echo "  4. Create release: git tag -a v${VERSION} -m 'Release v${VERSION}'"
echo "  5. Push tag: git push origin v${VERSION}"
echo ""
echo "See DEPLOYMENT.md for detailed instructions."
