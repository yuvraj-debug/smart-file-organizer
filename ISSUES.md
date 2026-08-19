# GitHub Issues for Smart File Organizer CLI

## Issue 1: Setup boilerplate & dependencies

### Description
Initialize the Python project structure with proper packaging, dependencies, and basic CLI framework.

### Requirements
- [ ] Create project structure with `src/smart_file_organizer/` package
- [ ] Setup `setup.py` or `pyproject.toml` for packaging
- [ ] Create `requirements.txt` for dependencies
- [ ] Implement basic CLI entry point using `argparse`
- [ ] Create console script entry point (`sfo` command)
- [ ] Add basic `__init__.py` files
- [ ] Create initial README with installation instructions

### Technical Details
- Use `setuptools` for packaging
- Dependencies: `argparse` (standard library), optionally `tqdm` for progress bars
- CLI should support `--help` and `--version` flags
- Entry point should be callable as `sfo` from command line

### Definition of Done
- Project can be installed via `pip install -e .`
- `sfo --help` shows usage information
- `sfo --version` shows version number
- Basic project structure is in place

---

## Issue 2: Implement core logic function

### Description
Implement the core file organization logic that sorts files by extension into appropriate folders.

### Requirements
- [ ] Create `organizer.py` with main organization logic
- [ ] Implement file type detection based on extensions
- [ ] Create predefined categories: Images, Documents, Archives, Code, Media, Others
- [ ] Implement folder creation and file moving functionality
- [ ] Handle file name conflicts (e.g., add counter suffix)
- [ ] Support recursive directory traversal (optional)
- [ ] Add proper error handling for permissions, locked files, etc.

### Technical Details
- Use `pathlib` for cross-platform path handling
- Use `shutil.move()` for file operations
- Implement category mapping as dictionary
- Create destination folders if they don't exist
- Log skipped files (due to permissions, etc.)

### Definition of Done
- Can organize files in a test directory by type
- Creates appropriate category folders
- Moves files to correct folders without data loss
- Handles common edge cases gracefully

---

## Issue 3: Add date-based organization

### Description
Add functionality to organize files by their creation or modification date.

### Requirements
- [ ] Add `--by-date` option to CLI with values: `created`, `modified`
- [ ] Add `--date-format` option with values: `year`, `month`, `day`
- [ ] Implement date-based folder structure (YYYY/MM/DD or variations)
- [ ] Extract file timestamps using `os.path.getctime()` and `os.path.getmtime()`
- [ ] Handle timezone considerations appropriately
- [ ] Ensure date-based organization works alongside extension-based organization

### Technical Details
- Use `datetime` module to convert timestamps to date objects
- Format dates as strings for folder names
- Support different granularities: year-only, year/month, year/month/day
- Validate input options and provide clear error messages

### Definition of Done
- `sfo organize --by-date modified` creates date-based folders
- `sfo organize --by-date created --date-format year` creates YYYY folders
- Combines with extension-based organization when both flags used
- Preserves original file metadata where possible

---

## Issue 4: Implement custom rules engine

### Description
Create a configurable rules engine that allows users to define custom file organization rules via JSON.

### Requirements
- [ ] Add `--config` option to specify custom rules JSON file
- [ ] Implement JSON schema for rules configuration
- [ ] Support regex patterns in file matching
- [ ] Allow custom category names and extensions
- [ ] Implement rule priority/ordering
- [ ] Provide default rules fallback when config not specified
- [ ] Validate JSON configuration and provide helpful error messages

### Technical Details
- Define JSON schema: `{ "categories": { "CategoryName": [".ext1", ".ext2"] }, "ignore": ["pattern1", "pattern2"] }`
- Support glob-style patterns and regex
- Process rules in order, first match wins
- Allow exclusion patterns to skip certain files/folders
- Merge custom rules with defaults appropriately

### Definition of Done
- Can load custom rules from JSON file
- Organizes files according to custom categories
- Falls back to default rules for unspecified extensions
- Handles malformed JSON gracefully with clear errors
- Supports both glob patterns and regex in configuration

---

## Issue 5: Add safety features & reporting

### Description
Implement safety features including dry-run mode, undo functionality, and comprehensive reporting.

### Requirements
- [ ] Add `--dry-run` flag to preview changes without executing
- [ ] Implement undo functionality to revert last organization
- [ ] Add `--ignore` option to skip specific files/directories
- [ ] Create detailed reporting of organized files
- [ ] Implement logging to file with timestamps
- [ ] Add confirmation prompts for potentially destructive operations
- [ ] Create backup/restore mechanism for undo

### Technical Details
- Dry-run: Build plan of operations, display what would happen
- Undo: Store mapping of original->new paths in temporary file
- Ignore: Support wildcards and path patterns
- Reporting: Count files by category, show before/after tree
- Logging: Timestamped log file in user's home directory or temp folder
- Backup: Copy files to temporary location before moving (for safety)

### Definition of Done
- `sfo organize --dry-run` shows planned changes without making them
- `sfo undo` restores files to original locations after organization
- `--ignore "*.tmp" "node_modules"` skips specified patterns
- Clear summary report shows files organized per category
- Log file created with all operations performed