"""Unit tests for hidden file handling in the organizer module."""

import os
import tempfile
import unittest
from pathlib import Path
from smart_file_organizer.organizer import (
    organize_files_by_extension,
    organize_files_by_date,
    DEFAULT_CATEGORIES
)

class TestOrganizerHiddenFiles(unittest.TestCase):
    """Test cases for hidden file handling in the organizer module."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.test_dir.name)

        # Create some test files including hidden files
        (self.source_dir / "test.jpg").touch()
        (self.source_dir / "document.pdf").touch()
        (self.source_dir / ".hidden_file").touch()  # Hidden file
        (self.source_dir / ".config").touch()       # Hidden file
        (self.source_dir / "normal.txt").touch()

        # Create a hidden directory with files
        hidden_dir = self.source_dir / ".hidden_dir"
        hidden_dir.mkdir()
        (hidden_dir / "secret.txt").touch()

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_organize_files_by_extension_skips_hidden_files(self):
        """Test that organize_files_by_extension skips hidden files."""
        operations = organize_files_by_extension(
            self.source_dir,
            DEFAULT_CATEGORIES,
            dry_run=True
        )

        # We expect 3 files to be moved (test.jpg, document.pdf, normal.txt)
        # Hidden files (.hidden_file, .config) and files in hidden dir should be skipped
        self.assertEqual(len(operations), 3)

        # Check that none of the operations involve hidden files
        for src, dest in operations:
            src_str = str(src)
            # Ensure source is not a hidden file
            self.assertFalse(any(part.startswith('.') and part not in ['.', '..'] 
                               for part in src.parts))
            # Ensure source is not in a hidden directory
            self.assertFalse(any(part.startswith('.') and part not in ['.', '..'] 
                               for part in src.parts[:-1]))  # Exclude the filename itself

    def test_organize_files_by_date_skips_hidden_files(self):
        """Test that organize_files_by_date skips hidden files."""
        operations = organize_files_by_date(
            self.source_dir,
            date_type="modified",
            date_format="year",
            dry_run=True
        )

        # We expect 3 files to be moved (test.jpg, document.pdf, normal.txt)
        # Hidden files (.hidden_file, .config) and files in hidden dir should be skipped
        self.assertEqual(len(operations), 3)

        # Check that none of the operations involve hidden files
        for src, dest in operations:
            src_str = str(src)
            # Ensure source is not a hidden file
            self.assertFalse(any(part.startswith('.') and part not in ['.', '..'] 
                               for part in src.parts))
            # Ensure source is not in a hidden directory
            self.assertFalse(any(part.startswith('.') and part not in ['.', '..'] 
                               for part in src.parts[:-1]))  # Exclude the filename itself

if __name__ == '__main__':
    unittest.main()