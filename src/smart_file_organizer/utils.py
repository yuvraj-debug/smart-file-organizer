"""Utility functions for Smart File Organizer."""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import json
from datetime import datetime

def get_file_timestamp(file_path: Path, timestamp_type: str = "modified") -> float:
    """
    Get file timestamp (creation or modification time).
    
    Args:
        file_path: Path to the file
        timestamp_type: Either "created" or "modified"
        
    Returns:
        Timestamp as float
    """
    if timestamp_type == "created":
        return os.path.getctime(file_path)
    else:  # modified
        return os.path.getmtime(file_path)

def timestamp_to_date_string(timestamp: float, date_format: str = "month") -> str:
    """
    Convert a timestamp to a date string based on the specified format.
    
    Args:
        timestamp: Unix timestamp
        date_format: Either "year", "month", or "day"
        
    Returns:
        Date string formatted according to date_format
    """
    date_obj = datetime.fromtimestamp(timestamp)
    
    if date_format == "year":
        return str(date_obj.year)
    elif date_format == "month":
        return f"{date_obj.year}/{date_obj.month:02d}"
    else:  # day
        return f"{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}"

def load_config(config_path: Optional[Path] = None) -> dict:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the JSON config file
        
    Returns:
        Configuration dictionary
    """
    default_config = {
        "categories": {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".md"],
            "Media": [".mp3", ".wav", ".flac", ".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            "Others": []
        },
        "ignore": [
            "node_modules",
            ".git",
            "*.tmp",
            "Thumbs.db",
            "*.log"
        ]
    }
    
    if config_path is None or not config_path.exists():
        return default_config
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Merge with defaults to ensure all required keys exist
        for key in default_config:
            if key not in config:
                config[key] = default_config[key]
        return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        print("Using default configuration.")
        return default_config

def should_ignore_file(file_path: Path, ignore_patterns: List[str]) -> bool:
    """
    Check if a file should be ignored based on ignore patterns.
    
    Args:
        file_path: Path to the file
        ignore_patterns: List of glob patterns to ignore
        
    Returns:
        True if file should be ignored, False otherwise
    """
    return any(file_path.match(pattern) for pattern in ignore_patterns)