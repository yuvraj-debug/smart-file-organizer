# Smart File Organizer CLI - Project Specification

## Overview
A command-line interface tool built with Python that helps users organize files in directories based on type, date, or custom rules.

## Core Features

### 1. File Type Organization
- Automatically categorizes files by extension into folders
- Predefined categories: Images, Documents, Archives, Code, Media, Others
- Configurable category mappings

### 2. Date-Based Organization
- Organize by file creation date (YYYY/MM/DD structure)
- Organize by file modification date
- Option to use year-only or year/month structure

### 3. Custom Rules Engine
- JSON-based configuration for custom categories
- Support for regex patterns in file matching
- Priority-based rule processing

### 4. Safety Features
- Dry-run mode to preview changes before execution
- Undo functionality to revert last organization
- Ignore patterns for files/folders to skip
- Confirmation prompts for destructive operations

### 5. Reporting & Logging
- Detailed summary of organized files
- Log file with timestamps and actions taken
- Verbose and quiet modes

## Technical Requirements

### Language & Dependencies
- Python 3.8+
- Standard library only for core functionality (os, shutil, pathlib, json, argparse, datetime)
- Optional: tqdm for progress bars, colorama for colored output

### Project Structure
```
smart-file-organizer/
├── src/
│   └── smart_file_organizer/
│       ├── __init__.py
│       ├── cli.py
│       ├── organizer.py
│       ├── rules.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_organizer.py
│   └── test_rules.py
├── bin/
│   └── sfo
├── README.md
├── PROJECT_SPEC.md
├── requirements.txt
├── setup.py
└── LICENSE
```

### CLI Interface
```
usage: sfo [-h] [--version] {organize,undo,config} ...

Smart File Organizer - Organize your files intelligently

positional arguments:
  {organize,undo,config}
                        Sub-command to run
    organize            Organize files in a directory
    undo                Undo the last organization operation
    config              Manage configuration

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

### Organize Command Arguments
```
usage: sfo organize [-h] [--by-date {created,modified}] [--date-format {year,month,day}]
                   [--config CONFIG] [--dry-run] [--verbose] [--ignore IGNORE [IGNORE ...]]
                   [directory]

positional arguments:
  directory             Directory to organize (default: current directory)

optional arguments:
  -h, --help            show this help message and exit
  --by-date {created,modified}
                        Organize by file date (default: None for extension-based)
  --date-format {year,month,day}
                        Date folder structure (default: month)
  --config CONFIG       Path to custom rules JSON file
  --dry-run             Show what would be done without making changes
  -v, --verbose         Increase output verbosity
  --ignore IGNORE [IGNORE ...]
                        Files or directories to ignore (can specify multiple)
```

## Success Criteria
- [ ] Successfully organizes files by type without errors
- [ ] Date-based organization creates correct folder structure
- [ ] Custom rules engine processes JSON configurations correctly
- [ ] Dry-run mode accurately predicts changes
- [ ] Undo functionality restores original state
- [ ] Proper error handling for edge cases (permissions, locked files, etc.)
- [ ] Cross-platform compatibility (Windows, macOS, Linux)
- [ ] Comprehensive test coverage (>80%)
- [ ] Clear documentation and usage examples

## Future Enhancements
- GUI version using tkinter or PySimpleGUI
- Integration with cloud storage services (Dropbox, Google Drive)
- Scheduled organization (cron jobs, Windows Task Scheduler)
- File deduplication detection
- Metadata-based organization (EXIF for photos, ID3 for music)
- Plugin system for custom organizers