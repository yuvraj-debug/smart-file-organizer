# Contributing to Smart File Organizer

Thank you for considering contributing to Smart File Organizer! Please read this document carefully to understand our contribution process.

## How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Label the issue as "bug"
- Provide steps to reproduce the issue
- Include your operating system and Python version
- Attach relevant logs or screenshots if applicable

### Suggesting Features
- Use the GitHub issue tracker
- Label the issue as "enhancement"
- Clearly describe the feature and its benefits
- Consider any potential drawbacks or edge cases

### Submitting Changes
1. Fork the repository
2. Create a new branch from `main`: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Ensure all tests pass: `python -m unittest discover tests/ -v`
5. Commit your changes: `git commit -m "feat: add amazing feature"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request against the `main` branch

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- pip

### Installation for Development
```bash
# Clone your fork
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer

# Install in development mode
pip install -e .

# Install test dependencies
pip install -r requirements.txt
```

### Running Tests
```bash
# Run all tests
python -m unittest discover tests/ -v

# Run tests with coverage
pip install pytest pytest-cov
python -m pytest tests/ --cov=smart_file_organizer
```

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings to all public functions and classes
- Keep lines to a maximum of 88 characters
- Use 4 spaces for indentation (no tabs)

## Pull Request Process

1. Update the README.md if needed to reflect changes
2. Ensure all tests pass
3. Update documentation if applicable
4. The PR will be reviewed by maintainers
5. Address any feedback promptly
6. Once approved, maintainers will merge the PR

## Getting Help
If you need help with anything, please:
- Check the existing documentation
- Look through existing issues
- Ask in the GitHub discussions
- Contact the maintainers

Thank you for contributing to Smart File Organizer!
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