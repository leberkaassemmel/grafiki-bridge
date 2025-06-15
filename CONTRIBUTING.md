# Contributing

Thank you for your interest in contributing! This guide will help you get started with contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git
- Basic understanding of pandas and data visualization

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/leberkaassemmel/grafiki-bridge.git
   cd grafiki-bridge
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Types of Contributions

We welcome several types of contributions:

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include a clear description of the problem
- Provide steps to reproduce the issue
- Include your Python and package versions
- Add sample data or code if possible

### 💡 Feature Requests
- Check existing issues first to avoid duplicates
- Clearly describe the feature and its benefits
- Provide use cases and examples
- Consider if it fits the project's scope

### 📝 Documentation
- Fix typos or unclear explanations
- Add examples or tutorials
- Improve API documentation
- Translate documentation (if applicable)

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring

## Development Guidelines

### Code Style

We follow PEP 8 Python style guidelines:

```bash
# Install development tools
pip install black flake8

# Format code
black grafiki/ tests/

# Check style
flake8 --max-line-length=150 grafiki/ tests/
```

### Testing

All contributions should include appropriate tests:

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=grafiki --cov-report=html
```

#### Writing Tests

- Add tests for new features in the `tests/` directory
- Test both success and failure cases
- Use descriptive test names
- Mock external dependencies when appropriate

Example test:
```python
def test_bridge_df_basic():
    """Test basic DataFrame bridging functionality."""
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    link = bridge_df(df, name="Test Data")
    
    assert isinstance(link, str)
    assert "grafiki.app" in link
    assert len(link) > 0
```

### Documentation

- Update docstrings for any new or modified functions
- Follow Google-style docstrings:

```python
def bridge_df(df: pd.DataFrame, name: Optional[str] = None) -> str:
    """Create a shareable link for a DataFrame.
    
    Args:
        df: The pandas DataFrame to share
        name: Optional name for the dataset
        
    Returns:
        A URL string that opens the data in Grafiki
        
    Raises:
        ValueError: If DataFrame is empty or invalid
        
    Example:
        >>> df = pd.DataFrame({'x': [1, 2, 3]})
        >>> link = bridge_df(df, "My Data")
        >>> print(link)
        https://www.grafiki.app/d#...
    """
```

## Submitting Changes

### Pull Request Process

1. **Ensure your code passes all checks**:
   ```bash
   black grafiki/ tests/
   flake8 --max-line-length=150 grafiki/ tests/
   pytest
   ```

2. **Update documentation** if needed
3. **Add tests** for new functionality
4. **Update CHANGELOG.md** with your changes
5. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "feat: add support for custom compression levels"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

### Commit Message Guidelines

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding tests
- `refactor:` for code refactoring
- `style:` for formatting changes

Examples:
```
feat: add support for custom base URLs
fix: handle empty DataFrames gracefully  
docs: update installation instructions
test: add tests for compression edge cases
```

### Pull Request Template

When creating a PR, please include:

- **Description**: What does this PR do?
- **Type of change**: Bug fix, new feature, documentation, etc.
- **Testing**: How was this tested?
- **Checklist**:
  - [ ] Code follows style guidelines
  - [ ] Self-review completed
  - [ ] Tests added/updated
  - [ ] Documentation updated
  - [ ] CHANGELOG.md updated

## Release Process

Releases are handled by maintainers:

1. Version bumping follows semantic versioning
2. Releases are tagged and published to PyPI automatically
3. Release notes are generated from the changelog

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create a GitHub Issue
- **Chat**: Join our community Discord (if available)
- **Email**: Contact maintainers at [email if available]

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

## AI Assistance Disclosure

This project uses AI tools to assist with development, including:
- Code generation and optimization
- Documentation writing
- Test case generation
- Code review assistance

All AI-generated content is reviewed and validated by human maintainers before inclusion.

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.