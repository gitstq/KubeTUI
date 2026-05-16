# Contributing to KubeTUI

Thank you for your interest in contributing to KubeTUI! 🎉

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/kubetui.git
   cd kubetui
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Maximum line length: 100 characters

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example:
```
feat: add pod logs streaming support
fix: handle connection timeout gracefully
docs: update installation instructions
```

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/kubetui
```

### Linting

```bash
ruff check src/kubetui
```

## 🐛 Reporting Issues

When reporting issues, please include:

1. Python version
2. KubeTUI version
3. Operating system
4. Steps to reproduce
5. Expected vs actual behavior

## 💡 Feature Requests

Feature requests are welcome! Please:

1. Check if the feature already exists or is planned
2. Describe the feature in detail
3. Explain the use case

## 📦 Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

Thank you for contributing! 🙏
