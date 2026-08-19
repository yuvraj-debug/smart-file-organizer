"""Unit tests for the organizer module."""

import os
import tempfile
import unittest
from pathlib import Path
from smart_file_organizer.organizer import (
    get_file_category,
    organize_files_by_extension,
    organize_files_by_date,
    DEFAULT_CATEGORIES
)

class TestOrganizer(unittest.TestCase):
    """Test cases for the organizer module."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.test_dir.name)

        # Create some test files
        (self.source_dir / "test.jpg").touch()
        (self.source_dir / "document.pdf").touch()
        (self.source_dir / "script.py").touch()
        (self.source_dir / "archive.zip").touch()
        (self.source_dir / "unknown.xyz").touch()

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_get_file_category(self):
        """Test that files are categorized correctly."""
        self.assertEqual(get_file_category(Path("test.jpg"), DEFAULT_CATEGORIES), "Images")
        self.assertEqual(get_file_category(Path("document.pdf"), DEFAULT_CATEGORIES), "Documents")
        self.assertEqual(get_file_category(Path("script.py"), DEFAULT_CATEGORIES), "Code")
        self.assertEqual(get_file_category(Path("archive.zip"), DEFAULT_CATEGORIES), "Archives")
        self.assertEqual(get_file_category(Path("unknown.xyz"), DEFAULT_CATEGORIES), "Others")

    def test_organize_files_by_extension_dry_run(self):
        """Test that organize_files_by_extension returns correct operations in dry run mode."""
        operations = organize_files_by_extension(
            self.source_dir,
            DEFAULT_CATEGORIES,
            dry_run=True
        )

        # We expect 5 files to be moved (one for each test file)
        self.assertEqual(len(operations), 5)

        # Check that each operation is a tuple of (source, destination)
        for src, dest in operations:
            self.assertIsInstance(src, Path)
            self.assertIsInstance(dest, Path)
            # The source should be in the test directory
            self.assertTrue(str(src).startswith(str(self.source_dir)))
            # The destination should be in a category folder
            self.assertTrue(any(cat in str(dest) for cat in DEFAULT_CATEGORIES.keys()))

    def test_organize_files_by_date_dry_run(self):
        """Test that organize_files_by_date returns correct operations in dry run mode."""
        operations = organize_files_by_date(
            self.source_dir,
            date_type="modified",
            date_format="year",
            dry_run=True
        )

        # We expect 5 files to be moved (one for each test file)
        self.assertEqual(len(operations), 5)

        # Check that each operation is a tuple of (source, destination)
        for src, dest in operations:
            self.assertIsInstance(src, Path)
            self.assertIsInstance(dest, Path)
            # The source should be in the test directory
            self.assertTrue(str(src).startswith(str(self.source_dir)))
            # The destination should be in a year folder (based on the file's modified time)
            # Since we just created the files, they should all be in the same year folder
            # We can't predict the exact year, but we can check the structure
            self.assertRegex(str(dest), r'.*\/\d{4}\/.*')

if __name__ == '__main__':
    unittest.main()