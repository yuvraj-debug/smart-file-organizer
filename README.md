# Smart File Organizer CLI

A command-line tool that automatically organizes files in a directory based on their type, date, or custom rules.

## Features

- 🗂️ Organize files by extension (images, documents, archives, etc.)
- 📅 Option to organize by date modified/created
- ⚙️ Custom rule support via JSON configuration
- 👀 Dry-run mode to preview changes
- ↩️ Undo functionality
- 🚫 Ignore specific files or folders
- 📊 Detailed reporting of organized files

## Installation

```bash
pip install smart-file-organizer
```

## Usage

### Basic Organization
```bash
# Organize files in current directory by file type
sfo organize

# Organize files in a specific directory
sfo organize /path/to/directory
```

### Organize by Date
```bash
# Organize by date modified (creates YYYY/MM folders)
sfo organize --by-date modified

# Organize by date created
sfo organize --by-date created
```

### Custom Rules
```bash
# Use custom rules from config file
sfo organize --config my-rules.json
```

### Dry Run
```bash
# Preview what would happen without making changes
sfo organize --dry-run
```

### Undo
```bash
# Undo the last organization operation
sfo undo
```

## Configuration

Create a `file-organizer.config.json` to define custom rules:

```json
{
  "categories": {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".xml"]
  },
  "ignore": [
    "node_modules",
    ".git",
    "*.tmp",
    "Thumbs.db"
  ]
}
```

## Development

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running Tests
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=smart_file_organizer
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various file organization tools
- Built with Python's excellent standard library