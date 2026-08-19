# Contributing to Smart File Organizer

Thank you for considering contributing to Smart File Organizer! Please read this guide to understand how to contribute effectively.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or suggest features
- Please include:
  - Clear description of the issue
  - Steps to reproduce (for bugs)
  - Expected vs actual behavior
  - Your operating system and Python version
  - Any relevant logs or error messages

### Making Changes
1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass
6. Submit a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
# For testing
pip install pytest pytest-cov

# Run tests
python -m pytest tests/ -v
```

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings to all public functions
- Keep functions focused and small
- Write clear, concise comments

### Pull Request Process
1. Ensure your code passes all tests
2. Update documentation if needed
3. Describe your changes in the pull request
4. Reference any related issues
5. Wait for code review feedback
6. Make any requested changes
7. Maintainers will merge your PR

## Contribution Guidelines

### What We're Looking For
- Bug fixes
- Feature enhancements
- Documentation improvements
- Test additions
- Performance improvements
- Code refactoring

### What We're Not Looking For
- Changes that break backward compatibility without good reason
- Features that don't align with the project scope
- Pull requests without tests (for functional changes)
- Large changes without prior discussion

## Getting Help
If you need help, please:
- Check existing issues and documentation
- Ask questions in the issue tracker
- Be patient and respectful of maintainers' time

Thank you for contributing to Smart File Organizer!