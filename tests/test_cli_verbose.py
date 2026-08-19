"""Unit tests for the CLI verbose mode functionality."""

import unittest
from unittest.mock import patch, MagicMock
import logging
import io
import sys
from smart_file_organizer.cli import main

class TestCLIVerbose(unittest.TestCase):
    """Test cases for the CLI verbose mode."""

    @patch('sys.argv', ['sfo', 'organize', '--verbose'])
    @patch('smart_file_organizer.cli.organize_with_safety')
    @patch('smart_file_organizer.cli.load_config')
    @patch('smart_file_organizer.cli.generate_report')
    @patch('smart_file_organizer.cli.print_report')
    def test_verbose_mode_enabled(
        self, mock_print_report, mock_generate_report, 
        mock_load_config, mock_organize_with_safety
    ):
        """Test that verbose mode enables logging and shows verbose output."""
        # Setup mocks
        mock_load_config.return_value = {"categories": {"Test": [".txt"]}, "ignore": []}
        mock_organize_with_safety.return_value = ([], "test123")
        mock_generate_report.return_value = {}
        
        # Capture logging output
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()  # Get root logger
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        try:
            with patch('sys.argv', ['sfo', 'organize', '--verbose']):
                try:
                    main()
                except SystemExit:
                    pass  # main() calls sys.exit() which raises SystemExit
        finally:
            logger.removeHandler(handler)
        
        # Verify that the functions were called
        mock_load_config.assert_called_once()
        mock_organize_with_safety.assert_called_once()
        mock_generate_report.assert_called_once_with([])
        mock_print_report.assert_called_once_with({})
        
        # Check that verbose output was produced in logs
        log_output = log_stream.getvalue()
        self.assertIn("Verbose mode enabled", log_output)
        self.assertIn("Organizing directory:", log_output)

    @patch('sys.argv', ['sfo', 'organize', '--verbose', '--by-date', 'created'])
    @patch('smart_file_organizer.cli.organize_with_safety')
    @patch('smart_file_organizer.cli.load_config')
    @patch('smart_file_organizer.cli.generate_report')
    @patch('smart_file_organizer.cli.print_report')
    def test_verbose_mode_with_date_organization(
        self, mock_print_report, mock_generate_report, 
        mock_load_config, mock_organize_with_safety
    ):
        """Test that verbose mode shows date organization details."""
        # Setup mocks
        mock_load_config.return_value = {"categories": {"Test": [".txt"]}, "ignore": []}
        mock_organize_with_safety.return_value = ([], "test123")
        mock_generate_report.return_value = {}
        
        # Capture logging output
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()  # Get root logger
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        try:
            with patch('sys.argv', ['sfo', 'organize', '--verbose', '--by-date', 'created']):
                try:
                    main()
                except SystemExit:
                    pass  # main() calls sys.exit() which raises SystemExit
        finally:
            logger.removeHandler(handler)
        
        # Verify that the functions were called
        mock_load_config.assert_called_once()
        mock_organize_with_safety.assert_called_once()
        mock_generate_report.assert_called_once_with([])
        mock_print_report.assert_called_once_with({})
        
        # Check that verbose output shows date organization details
        log_output = log_stream.getvalue()
        self.assertIn("Verbose mode enabled", log_output)
        self.assertIn("Organization method: by date (created)", log_output)
        self.assertIn("format: month", log_output)  # default date format

    @patch('sys.argv', ['sfo', 'organize', '--verbose', '--config', 'test.json'])
    @patch('smart_file_organizer.cli.organize_with_safety')
    @patch('smart_file_organizer.cli.load_config')
    @patch('smart_file_organizer.cli.generate_report')
    @patch('smart_file_organizer.cli.print_report')
    def test_verbose_mode_with_config(
        self, mock_print_report, mock_generate_report, 
        mock_load_config, mock_organize_with_safety
    ):
        """Test that verbose mode shows config organization details."""
        # Setup mocks
        mock_load_config.return_value = {"categories": {"Test": [".txt"]}, "ignore": ["*.tmp"]}
        mock_organize_with_safety.return_value = ([], "test123")
        mock_generate_report.return_value = {}
        
        # Capture logging output
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger()  # Get root logger
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        try:
            with patch('sys.argv', ['sfo', 'organize', '--verbose', '--config', 'test.json']):
                try:
                    main()
                except SystemExit:
                    pass  # main() calls sys.exit() which raises SystemExit
        finally:
            logger.removeHandler(handler)
        
        # Verify that the functions were called
        mock_load_config.assert_called_once()
        mock_organize_with_safety.assert_called_once()
        mock_generate_report.assert_called_once_with([])
        mock_print_report.assert_called_once_with({})
        
        # Check that verbose output shows config organization details
        log_output = log_stream.getvalue()
        self.assertIn("Verbose mode enabled", log_output)
        self.assertIn("Organization method: custom rules from test.json", log_output)
        self.assertIn("Ignore patterns: ['*.tmp']", log_output)

if __name__ == '__main__':
    unittest.main()