"""Rules engine for Smart File Organizer."""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Pattern
import logging

logger = logging.getLogger(__name__)

def compile_patterns(patterns: List[str]) -> List[Pattern]:
    """
    Compile a list of glob or regex patterns into compiled regex objects.
    
    Args:
        patterns: List of glob or regex patterns
        
    Returns:
        List of compiled regex patterns
    """
    compiled = []
    for pattern in patterns:
        try:
            # Try to compile as regex first
            compiled.append(re.compile(pattern))
        except re.error:
            # If regex fails, treat as glob pattern
            # Convert glob to regex
            regex_pattern = re.escape(pattern)
            regex_pattern = regex_pattern.replace(r'\*', '.*')
            regex_pattern = regex_pattern.replace(r'\?', '.')
            compiled.append(re.compile(regex_pattern))
    return compiled

def matches_patterns(file_path: Path, patterns: List[Pattern]) -> bool:
    """
    Check if a file path matches any of the given patterns.
    
    Args:
        file_path: Path to check
        patterns: List of compiled regex patterns
        
    Returns:
        True if file matches any pattern, False otherwise
    """
    # Check against the file name and full path
    file_str = str(file_path)
    name_str = file_path.name
    
    for pattern in patterns:
        if pattern.search(file_str) or pattern.search(name_str):
            return True
    return False

def get_file_category_with_rules(
    file_path: Path, 
    categories: Dict[str, List[str]],
    ignore_patterns: List[str] = None
) -> Tuple[str, bool]:
    """
    Determine the category of a file based on rules, with ignore pattern support.
    
    Args:
        file_path: Path to the file
        categories: Dictionary mapping category names to lists of extensions
        ignore_patterns: List of glob/regex patterns to ignore
        
    Returns:
        Tuple of (category_name, should_ignore)
    """
    if ignore_patterns is None:
        ignore_patterns = []
    
    # Compile ignore patterns
    compiled_ignore = compile_patterns(ignore_patterns)
    
    # Check if file should be ignored
    if matches_patterns(file_path, compiled_ignore):
        return ("", True)
    
    # Get file extension
    extension = file_path.suffix.lower()
    
    # Find matching category
    for category, extensions in categories.items():
        if extension in extensions:
            return (category, False)
    
    # Return "Others" if no match found
    return ("Others", False)

def organize_files_with_rules(
    source_dir: Path,
    categories: Dict[str, List[str]],
    ignore_patterns: List[str] = None,
    dry_run: bool = False
) -> List[Tuple[Path, Path]]:
    """
    Organize files using custom rules engine.
    
    Args:
        source_dir: Directory to organize
        categories: Dictionary mapping category names to file extensions
        ignore_patterns: List of glob/regex patterns to ignore
        dry_run: If True, only simulate the organization
        
    Returns:
        List of tuples (original_path, new_path) for files that were/would be moved
    """
    if ignore_patterns is None:
        ignore_patterns = []
    
    operations = []
    
    # Iterate through all files in the source directory
    for item in source_dir.rglob("*"):
        # Skip directories
        if item.is_dir():
            continue
            
        # Get category and ignore status
        category, should_ignore = get_file_category_with_rules(
            item, categories, ignore_patterns
        )
        
        if should_ignore:
            logger.info(f"Ignoring file (by rules): {item}")
            continue
        
        # Create destination directory
        dest_dir = source_dir / category
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
        
        # Handle file name conflicts
        dest_path = dest_dir / item.name
        counter = 1
        original_dest_path = dest_path
        while dest_path.exists():
            stem = item.stem
            suffix = item.suffix
            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Record the operation
        operations.append((item, dest_path))
        
        # Perform the move if not dry run
        if not dry_run:
            try:
                shutil.move(str(item), str(dest_path))
                logger.info(f"Moved by rules: {item} -> {dest_path}")
            except Exception as e:
                logger.error(f"Failed to move {item}: {e}")
                # Remove the failed operation from the list
                operations.pop()
    
    return operations