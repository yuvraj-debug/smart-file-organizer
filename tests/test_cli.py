"""Unit tests for the CLI module."""

import unittest
from unittest.mock import patch, MagicMock
from smart_file_organizer.cli import main

class TestCLI(unittest.TestCase):
    """Test cases for the CLI module."""

    @patch('sys.argv', ['sfo', '--help'])
    @patch('sys.stdout')
    def test_help_command(self, mock_stdout):
        """Test that --help shows usage information."""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)

    @patch('sys.argv', ['sfo', '--version'])
    @patch('sys.stdout')
    def test_version_command(self, mock_stdout):
        """Test that --version shows version information."""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)

    @patch('sys.argv', ['sfo', 'organize'])
    @patch('smart_file_organizer.cli.organize_with_safety')
    @patch('smart_file_organizer.cli.load_config')
    @patch('smart_file_organizer.cli.generate_report')
    @patch('smart_file_organizer.cli.print_report')
    def test_organize_command_calls_correct_functions(
        self, mock_print_report, mock_generate_report, 
        mock_load_config, mock_organize_with_safety
    ):
        """Test that organize command calls the correct functions."""
        # Setup mocks
        mock_load_config.return_value = {"categories": {"Test": [".txt"]}, "ignore": []}
        mock_organize_with_safety.return_value = ([], "test123")
        mock_generate_report.return_value = {}
        
        # This should not raise an exception
        with patch('sys.argv', ['sfo', 'organize']):
            try:
                main()
            except SystemExit:
                pass  # main() calls sys.exit() which raises SystemExit
        
        # Verify that the functions were called
        mock_load_config.assert_called_once()
        mock_organize_with_safety.assert_called_once()
        mock_generate_report.assert_called_once_with([])
        mock_print_report.assert_called_once_with({})

if __name__ == '__main__':
    unittest.main()