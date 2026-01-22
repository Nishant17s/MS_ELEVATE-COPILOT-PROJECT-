# Contributing Guide

Thank you for your interest in contributing to InsightPro! We welcome contributions from the community.

## Code of Conduct

Be respectful and inclusive. We're committed to providing a welcoming environment for all contributors.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write or update tests
5. Submit a pull request

## Development Workflow

### Setup Development Environment

```bash
git clone https://github.com/yourusername/InsightPro.git
cd InsightPro
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black
```

### Code Style

- Follow PEP 8 guidelines
- Use `black` for formatting: `black *.py engine/*.py`
- Use `flake8` for linting: `flake8 *.py engine/*.py`
- Add docstrings to all functions
- Use type hints where applicable

### Testing

```bash
# Run tests
pytest -v

# Run tests with coverage
pytest --cov=. --cov-report=html
```

### Commit Messages

Format: `type(scope): message`

Examples:
- `feat(api): add retry logic for rate limits`
- `fix(ui): align settings button text`
- `docs(readme): update installation steps`
- `refactor(ml): optimize burn rate calculation`

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Pull Request Process

1. Update documentation and README
2. Add tests for new functionality
3. Ensure all tests pass: `pytest`
4. Ensure code style: `black` and `flake8`
5. Fill out the PR template completely
6. Request review from maintainers

## Areas for Contribution

- [ ] Bug fixes
- [ ] Performance improvements
- [ ] Documentation
- [ ] Feature implementations
- [ ] Testing
- [ ] UI/UX improvements
- [ ] Code refactoring

## Questions?

Open a GitHub issue or discussion. We're here to help!

---

**Thank you for contributing!** 🚀
