"""Safety features for Smart File Organizer including dry-run, undo, and reporting."""

import os
import shutil
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import tempfile
from datetime import datetime

class OperationLogger:
    """Logs file organization operations for undo functionality."""
    
    def __init__(self, log_dir: Optional[Path] = None):
        if log_dir is None:
            log_dir = Path.home() / ".smart_file_organizer"
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        self.operations_file = self.log_dir / "operations.json"
    
    def log_operation(self, original_path: Path, new_path: Path, operation_id: str = None):
        """
        Log a file operation for potential undo.
        
        Args:
            original_path: Original file path
            new_path: New file path after operation
            operation_id: Optional ID for the operation batch
        """
        if operation_id is None:
            operation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        operation = {
            "id": operation_id,
            "timestamp": datetime.now().isoformat(),
            "original_path": str(original_path),
            "new_path": str(new_path),
            "type": "move"
        }
        
        # Load existing operations
        operations = []
        if self.operations_file.exists():
            try:
                with open(self.operations_file, 'r') as f:
                    operations = json.load(f)
            except (json.JSONDecodeError, IOError):
                operations = []
        
        # Add new operation
        operations.append(operation)
        
        # Save back to file
        try:
            with open(self.operations_file, 'w') as f:
                json.dump(operations, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not log operation: {e}")
    
    def get_latest_operations(self, limit: int = 100) -> List[Dict]:
        """
        Get the latest logged operations.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of operation dictionaries
        """
        if not self.operations_file.exists():
            return []
        
        try:
            with open(self.operations_file, 'r') as f:
                operations = json.load(f)
            return operations[-limit:] if limit > 0 else operations
        except (json.JSONDecodeError, IOError):
            return []
    
    def clear_operations(self):
        """Clear all logged operations."""
        if self.operations_file.exists():
            self.operations_file.unlink()

def organize_with_safety(
    source_dir: Path,
    organize_func,
    *args,
    dry_run: bool = False,
    enable_undo: bool = True,
    **kwargs
) -> Tuple[List[Tuple[Path, Path]], Optional[str]]:
    """
    Organize files with safety features including dry-run and undo logging.
    
    Args:
        source_dir: Directory to organize
        organize_func: Function to call for organization (should return list of operations)
        *args: Arguments to pass to organize_func
        dry_run: If True, only simulate the organization
        enable_undo: If True, log operations for undo
        **kwargs: Keyword arguments to pass to organize_func
        
    Returns:
        Tuple of (operations_list, operation_id)
    """
    logger = OperationLogger() if enable_undo else None
    operation_id = None
    
    if enable_undo and not dry_run:
        operation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Call the organization function
    operations = organize_func(source_dir, *args, dry_run=dry_run, **kwargs)
    
    # Log operations if not dry run and undo is enabled
    if not dry_run and enable_undo and logger and operations:
        for original_path, new_path in operations:
            logger.log_operation(original_path, new_path, operation_id)
    
    return operations, operation_id

def undo_last_operation(log_dir: Optional[Path] = None) -> bool:
    """
    Undo the last file organization operation.
    
    Args:
        log_dir: Directory where operations are logged
        
    Returns:
        True if undo was successful, False otherwise
    """
    if log_dir is None:
        log_dir = Path.home() / ".smart_file_organizer"
    
    operations_file = log_dir / "operations.json"
    
    if not operations_file.exists():
        print("No operations to undo.")
        return False
    
    try:
        with open(operations_file, 'r') as f:
            operations = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading operations log: {e}")
        return False
    
    if not operations:
        print("No operations to undo.")
        return False
    
    # Get the most recent operation
    last_operation = operations[-1]
    
    original_path = Path(last_operation["original_path"])
    new_path = Path(last_operation["new_path"])
    
    # Check if the file still exists at the new location
    if not new_path.exists():
        print(f"Error: File {new_path} no longer exists.")
        return False
    
    # Check if the original location still exists (directory)
    if not original_path.parent.exists():
        print(f"Error: Original directory {original_path.parent} no longer exists.")
        return False
    
    # Handle file name conflicts during undo
    final_path = original_path
    counter = 1
    while final_path.exists() and final_path != new_path:
        stem = original_path.stem
        suffix = original_path.suffix
        final_path = original_path.parent / f"{stem}_{counter}{suffix}"
        counter += 1
    
    try:
        # Move the file back
        shutil.move(str(new_path), str(final_path))
        print(f"Undone: {new_path} -> {final_path}")
        
        # Remove the operation from the log
        operations.pop()
        with open(operations_file, 'w') as f:
            json.dump(operations, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error during undo: {e}")
        return False

def generate_report(operations: List[Tuple[Path, Path]]) -> Dict[str, int]:
    """
    Generate a summary report of file organization operations.
    
    Args:
        operations: List of (original_path, new_path) tuples
        
    Returns:
        Dictionary with counts by category
    """
    report = {}
    
    for original_path, new_path in operations:
        # Extract category from the new path (parent directory name)
        category = new_path.parent.name
        report[category] = report.get(category, 0) + 1
    
    return report

def print_report(report: Dict[str, int]):
    """
    Print a formatted report of file organization operations.
    
    Args:
        report: Dictionary with counts by category
    """
    if not report:
        print("No files were organized.")
        return
    
    print("\n=== Organization Report ===")
    total_files = sum(report.values())
    print(f"Total files organized: {total_files}")
    print("-" * 30)
    
    for category, count in sorted(report.items()):
        print(f"{category:>15}: {count:>4} files")
    
    print("-" * 30)
    print(f"{'TOTAL':>15}: {total_files:>4} files")
    print("==========================\n")

def create_backup(source_dir: Path, backup_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Create a backup of files before organization (extra safety measure).
    
    Args:
        source_dir: Directory to backup
        backup_dir: Directory to store backup (if None, creates temp directory)
        
    Returns:
        Path to backup directory, or None if backup failed
    """
    if backup_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(tempfile.gettempdir()) / f"sfo_backup_{timestamp}"
    
    try:
        # Copy the entire directory structure
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(source_dir, backup_dir)
        print(f"Backup created at: {backup_dir}")
        return backup_dir
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
        return None