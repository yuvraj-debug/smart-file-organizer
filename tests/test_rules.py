"""Unit tests for the rules module."""

import os
import tempfile
import unittest
from pathlib import Path
from smart_file_organizer.rules import (
    compile_patterns,
    matches_patterns,
    get_file_category_with_rules,
    organize_files_with_rules
)

class TestRules(unittest.TestCase):
    """Test cases for the rules module."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.test_dir.name)

        # Create some test files
        (self.source_dir / "test.jpg").touch()
        (self.source_dir / "document.pdf").touch()
        (self.source_dir / "script.py").touch()
        (self.source_dir / "temp.tmp").touch()
        (self.source_dir / "secret.key").touch()

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_compile_patterns(self):
        """Test pattern compilation."""
        patterns = ["*.tmp", "secret.*", r"\d+"]
        compiled = compile_patterns(patterns)
        
        self.assertEqual(len(compiled), 3)
        # Test that they actually work
        self.assertTrue(compiled[0].search("test.tmp"))
        self.assertTrue(compiled[1].search("secret.key"))
        self.assertTrue(compiled[2].search("123abc"))

    def test_matches_patterns(self):
        """Test pattern matching."""
        patterns = [r".*\.tmp$", r"secret.*"]
        compiled = compile_patterns(patterns)
        
        self.assertTrue(matches_patterns(Path("test.tmp"), compiled))
        self.assertTrue(matches_patterns(Path("secret.key"), compiled))
        self.assertFalse(matches_patterns(Path("test.jpg"), compiled))

    def test_get_file_category_with_rules_no_ignore(self):
        """Test categorization without ignore patterns."""
        categories = {
            "Images": [".jpg", ".png"],
            "Documents": [".pdf"],
            "Code": [".py"]
        }
        
        category, ignore = get_file_category_with_rules(
            Path("test.jpg"), categories, []
        )
        self.assertEqual(category, "Images")
        self.assertFalse(ignore)
        
        category, ignore = get_file_category_with_rules(
            Path("document.pdf"), categories, []
        )
        self.assertEqual(category, "Documents")
        self.assertFalse(ignore)
        
        category, ignore = get_file_category_with_rules(
            Path("unknown.xyz"), categories, []
        )
        self.assertEqual(category, "Others")
        self.assertFalse(ignore)

    def test_get_file_category_with_rules_with_ignore(self):
        """Test categorization with ignore patterns."""
        categories = {
            "Images": [".jpg", ".png"],
            "Documents": [".pdf"],
            "Code": [".py"]
        }
        ignore_patterns = ["*.tmp", "secret.*"]
        
        # Test ignored files
        category, ignore = get_file_category_with_rules(
            Path("temp.tmp"), categories, ignore_patterns
        )
        self.assertEqual(category, "")
        self.assertTrue(ignore)
        
        category, ignore = get_file_category_with_rules(
            Path("secret.key"), categories, ignore_patterns
        )
        self.assertEqual(category, "")
        self.assertTrue(ignore)
        
        # Test non-ignored files
        category, ignore = get_file_category_with_rules(
            Path("test.jpg"), categories, ignore_patterns
        )
        self.assertEqual(category, "Images")
        self.assertFalse(ignore)

    def test_organize_files_with_rules_dry_run(self):
        """Test that organize_files_with_rules returns correct operations in dry run mode."""
        categories = {
            "Images": [".jpg", ".png"],
            "Documents": [".pdf"],
            "Code": [".py"]
        }
        ignore_patterns = ["*.tmp", "secret.*"]
        
        operations = organize_files_with_rules(
            self.source_dir,
            categories,
            ignore_patterns,
            dry_run=True
        )

        # We expect 3 files to be moved (jpg, pdf, py) - 2 ignored (tmp, key)
        self.assertEqual(len(operations), 3)

        # Check that each operation is a tuple of (source, destination)
        for src, dest in operations:
            self.assertIsInstance(src, Path)
            self.assertIsInstance(dest, Path)
            # The source should be in the test directory
            self.assertTrue(str(src).startswith(str(self.source_dir)))
            # The destination should be in a category folder
            self.assertTrue(any(cat in str(dest) for cat in categories.keys()))

if __name__ == '__main__':
    unittest.main()