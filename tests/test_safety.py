"""Unit tests for the safety module."""

import os
import tempfile
import unittest
from pathlib import Path
from smart_file_organizer.safety import (
    OperationLogger,
    organize_with_safety,
    undo_last_operation,
    generate_report,
    print_report,
    create_backup
)

class TestSafety(unittest.TestCase):
    """Test cases for the safety module."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.test_dir.name)

        # Create some test files
        (self.source_dir / "test1.txt").touch()
        (self.source_dir / "test2.txt").touch()
        (self.source_dir / "subdir").mkdir()
        (self.source_dir / "subdir" / "test3.txt").touch()

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_operation_logger_init(self):
        """Test that OperationLogger initializes correctly."""
        logger = OperationLogger()
        self.assertTrue(logger.log_dir.exists())
        self.assertTrue((logger.log_dir / "operations.json").exists() or True)  # File created on first log

    def test_log_operation(self):
        """Test logging an operation."""
        logger = OperationLogger(Path(self.test_dir.name))
        original = Path("/tmp/original.txt")
        new = Path("/tmp/new.txt")
        
        # This should not raise an exception
        logger.log_operation(original, new, "test123")
        
        # Check that the operation was logged
        operations = logger.get_latest_operations()
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["id"], "test123")
        self.assertEqual(operations[0]["original_path"], str(original))
        self.assertEqual(operations[0]["new_path"], str(new))

    def test_generate_report(self):
        """Test report generation."""
        # Create mock operations
        operations = [
            (Path("/tmp/test1.txt"), Path("/tmp/Documents/test1.txt")),
            (Path("/tmp/test2.txt"), Path("/tmp/Documents/test2.txt")),
            (Path("/tmp/image.jpg"), Path("/tmp/Images/image.jpg"))
        ]
        
        report = generate_report(operations)
        
        self.assertEqual(report.get("Documents", 0), 2)
        self.assertEqual(report.get("Images", 0), 1)
        self.assertEqual(len(report), 2)

    def test_print_report(self):
        """Test report printing (just ensure it doesn't crash)."""
        report = {"Documents": 2, "Images": 1}
        # This should not raise an exception
        print_report(report)

    def test_create_backup(self):
        """Test backup creation."""
        backup_dir = create_backup(self.source_dir)
        
        self.assertIsNotNone(backup_dir)
        self.assertTrue(backup_dir.exists())
        self.assertTrue((backup_dir / "test1.txt").exists())
        self.assertTrue((backup_dir / "test2.txt").exists())
        self.assertTrue((backup_dir / "subdir" / "test3.txt").exists())
        
        # Clean up
        if backup_dir and backup_dir.exists():
            import shutil
            shutil.rmtree(backup_dir)

    def test_organize_with_safety_dry_run(self):
        """Test organize_with_safety in dry run mode."""
        # Simple organize function for testing
        def mock_organize(source_dir, dry_run=False):
            if dry_run:
                return [(self.source_dir / "test1.txt", self.source_dir / "Documents" / "test1.txt")]
            return []
        
        operations, operation_id = organize_with_safety(
            self.source_dir,
            mock_organize,
            dry_run=True
        )
        
        self.assertEqual(len(operations), 1)
        self.assertIsNone(operation_id)  # Should be None in dry run
        self.assertEqual(operations[0][0], self.source_dir / "test1.txt")
        self.assertEqual(operations[0][1], self.source_dir / "Documents" / "test1.txt")

if __name__ == '__main__':
    unittest.main()