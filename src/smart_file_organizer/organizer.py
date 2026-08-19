"""Core file organization logic for Smart File Organizer."""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Default file categories
DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".md", ".txt"],
    "Media": [".mp3", ".wav", ".flac", ".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Others": []  # Catch-all for files that don't match any category
}

def get_file_category(file_path: Path, categories: Dict[str, List[str]]) -> str:
    """
    Determine the category of a file based on its extension.
    
    Args:
        file_path: Path to the file
        categories: Dictionary mapping category names to lists of extensions
        
    Returns:
        Category name for the file
    """
    extension = file_path.suffix.lower()
    
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    
    # Return "Others" if no match found
    return "Others"

def organize_files_by_extension(
    source_dir: Path, 
    categories: Dict[str, List[str]],
    dry_run: bool = False,
    ignore_patterns: List[str] = None
) -> List[Tuple[Path, Path]]:
    """
    Organize files in source_dir by their file extension into category folders.
    
    Args:
        source_dir: Directory to organize
        categories: Dictionary mapping category names to file extensions
        dry_run: If True, only simulate the organization
        ignore_patterns: List of glob patterns to ignore
        
    Returns:
        List of tuples (original_path, new_path) for files that were/would be moved
    """
    if ignore_patterns is None:
        ignore_patterns = []
    
    # Convert ignore patterns to Path objects for matching
    ignore_paths = []
    for pattern in ignore_patterns:
        ignore_paths.extend(source_dir.glob(pattern))
    
    operations = []
    
    # Iterate through all files in the source directory
    for item in source_dir.rglob("*"):
        # Skip directories
        if item.is_dir():
            continue
            
        # Skip symlinks for safety
        if item.is_symlink():
            logger.info(f"Skipping symlink: {item}")
            continue
            
        # Skip if file matches any ignore pattern
        if any(item.match(pattern) for pattern in ignore_patterns):
            logger.info(f"Ignoring file: {item}")
            continue
            
        # Skip if file is in any ignore path
        if any(item.is_relative_to(ignore_path) for ignore_path in ignore_paths if ignore_path.is_dir()):
            logger.info(f"Ignoring file in ignored path: {item}")
            continue
        
        # Determine file category
        category = get_file_category(item, categories)
        
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
                logger.info(f"Moved: {item} -> {dest_path}")
            except Exception as e:
                logger.error(f"Failed to move {item}: {e}")
                # Remove the failed operation from the list
                operations.pop()
    
    return operations

def organize_files_by_date(
    source_dir: Path,
    date_type: str = "modified",
    date_format: str = "month",
    dry_run: bool = False,
    ignore_patterns: List[str] = None
) -> List[Tuple[Path, Path]]:
    """
    Organize files in source_dir by their creation or modification date.
    
    Args:
        source_dir: Directory to organize
        date_type: Either "created" or "modified"
        date_format: Either "year", "month", or "day"
        dry_run: If True, only simulate the organization
        ignore_patterns: List of glob patterns to ignore
        
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
            
        # Skip symlinks for safety
        if item.is_symlink():
            logger.info(f"Skipping symlink: {item}")
            continue
            
        # Skip if file matches any ignore pattern
        if any(item.match(pattern) for pattern in ignore_patterns):
            logger.info(f"Ignoring file: {item}")
            continue
        
        # Get file timestamp
        if date_type == "created":
            timestamp = os.path.getctime(item)
        else:  # modified
            timestamp = os.path.getmtime(item)
        
        # Convert timestamp to date components
        from datetime import datetime
        date_obj = datetime.fromtimestamp(timestamp)
        
        # Build destination path based on date format
        if date_format == "year":
            date_str = str(date_obj.year)
        elif date_format == "month":
            date_str = f"{date_obj.year}/{date_obj.month:02d}"
        else:  # day
            date_str = f"{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}"
        
        # Create destination directory
        dest_dir = source_dir / date_str
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
        
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
                logger.info(f"Moved by date: {item} -> {dest_path}")
            except Exception as e:
                logger.error(f"Failed to move {item}: {e}")
                # Remove the failed operation from the list
                operations.pop()
    
    return operations