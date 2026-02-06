# Contributing to Hancock

Thank you for your interest in contributing to Hancock! 🎉

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Workspace account (for testing)
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hancock-cli.git
   cd hancock-cli
   ```

2. **Install development dependencies:**
   ```bash
   pip install -e .
   pip install pytest black flake8
   ```

3. **Run Hancock from source:**
   ```bash
   python -m hancock --help
   ```

## Making Changes

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions small and focused

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hancock

# Run specific test
pytest tests/test_matching.py
```

### Code Formatting

```bash
# Format code with black
black hancock/

# Check with flake8
flake8 hancock/
```

## Submitting Changes

### Pull Request Process

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Add tests if applicable
   - Update README if needed

3. **Test your changes:**
   ```bash
   python -m hancock deploy test-signatures/ --dry-run
   ```

4. **Commit with a clear message:**
   ```bash
   git commit -m "feat: add support for bulk signature validation"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Build process or tooling changes

## Reporting Issues

### Bug Reports

Include:
- Hancock version (`hancock --version`)
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

### Feature Requests

Describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered
- How it benefits other users

## Development Guidelines

### Adding a New Command

1. Create command file in `hancock/commands/`
2. Implement the command logic
3. Register in `hancock/cli.py`
4. Add tests
5. Update documentation

Example:
```python
# hancock/commands/yourcommand.py
def run_yourcommand(arg1, arg2):
    """Your command implementation."""
    pass

# hancock/cli.py
@main.command()
@click.argument('arg1')
def yourcommand(arg1):
    """Your command description."""
    from .commands.yourcommand import run_yourcommand
    run_yourcommand(arg1)
```

### Improving UI

- Use the `rich` library for terminal output
- Keep colors consistent with the theme
- Provide clear error messages
- Show progress for long operations

### Testing

- Test with real Google Workspace when possible
- Use mocks for API calls in unit tests
- Test edge cases (empty folders, large files, etc.)
- Test error handling

## Getting Help

- **Documentation:** [README.md](README.md)
- **Issues:** [GitHub Issues](https://github.com/yourusername/hancock-cli/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/hancock-cli/discussions)

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to make Hancock better!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Hancock! 🚀
