"""Unit tests for the utils module."""

import os
import tempfile
import unittest
from pathlib import Path
from smart_file_organizer.utils import (
    get_file_timestamp,
    timestamp_to_date_string,
    load_config,
    should_ignore_file
)

class TestUtils(unittest.TestCase):
    """Test cases for the utils module."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.test_dir.name)

        # Create a test file
        self.test_file = self.source_dir / "test.txt"
        self.test_file.touch()

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_get_file_timestamp(self):
        """Test that we can get file timestamps."""
        created_time = get_file_timestamp(self.test_file, "created")
        modified_time = get_file_timestamp(self.test_file, "modified")
        
        # Both should be positive numbers
        self.assertGreater(created_time, 0)
        self.assertGreater(modified_time, 0)

    def test_timestamp_to_date_string(self):
        """Test timestamp conversion to date strings."""
        # Use a known timestamp (January 1, 2023)
        timestamp = 1672531200  # 2023-01-01 00:00:00 UTC
        
        self.assertEqual(timestamp_to_date_string(timestamp, "year"), "2023")
        self.assertEqual(timestamp_to_date_string(timestamp, "month"), "2023/01")
        self.assertEqual(timestamp_to_date_string(timestamp, "day"), "2023/01/01")

    def test_load_config_default(self):
        """Test loading default config when no file is provided."""
        config = load_config(None)
        
        # Should have default categories
        self.assertIn("Images", config["categories"])
        self.assertIn("Documents", config["categories"])
        self.assertIn(".jpg", config["categories"]["Images"])
        self.assertIn(".pdf", config["categories"]["Documents"])

    def test_load_config_custom(self):
        """Test loading custom config from file."""
        config_file = self.source_dir / "test_config.json"
        config_content = {
            "categories": {
                "Custom": [".xyz", ".abc"]
            },
            "ignore": ["*.tmp"]
        }
        
        with open(config_file, 'w') as f:
            import json
            json.dump(config_content, f)
        
        config = load_config(config_file)
        
        # Should have the custom config (current implementation replaces, doesn't merge)
        self.assertIn("Custom", config["categories"])
        self.assertIn(".xyz", config["categories"]["Custom"])
        # Categories are replaced, not merged in current implementation
        self.assertNotIn("Images", config["categories"])
        self.assertIn("*.tmp", config["ignore"])

    def test_should_ignore_file(self):
        """Test file ignoring logic."""
        # Test basic pattern matching
        self.assertTrue(should_ignore_file(Path("test.tmp"), ["*.tmp"]))
        self.assertFalse(should_ignore_file(Path("test.txt"), ["*.tmp"]))
        
        # Test multiple patterns
        self.assertTrue(should_ignore_file(Path("test.tmp"), ["*.tmp", "*.log"]))
        self.assertTrue(should_ignore_file(Path("test.log"), ["*.tmp", "*.log"]))
        self.assertFalse(should_ignore_file(Path("test.txt"), ["*.tmp", "*.log"]))

if __name__ == '__main__':
    unittest.main()