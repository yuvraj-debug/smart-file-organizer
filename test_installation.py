#!/usr/bin/env python3
"""Test script to verify the installation works correctly."""

import subprocess
import sys
from pathlib import Path

def test_installation():
    """Test that the package can be installed and the CLI works."""
    try:
        # Test that we can import the package
        import smart_file_organizer
        print(f"✓ Successfully imported smart_file_organizer v{smart_file_organizer.__version__}")
        
        # Test that we can import the modules
        from smart_file_organizer import organizer, rules, safety, utils
        print("✓ Successfully imported all modules")
        
        # Test that the CLI module can be imported
        from smart_file_organizer.cli import main
        print("✓ Successfully imported CLI module")
        
        print("\n✓ All installation tests passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_cli_help():
    """Test that the CLI help works."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "smart_file_organizer.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        if result.returncode == 0 and "Smart File Organizer" in result.stdout:
            print("✓ CLI help test passed")
            return True
        else:
            print(f"✗ CLI help test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ CLI help test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Smart File Organizer installation...\n")
    
    success = test_installation()
    success &= test_cli_help()
    
    if success:
        print("\n🎉 All tests passed! The installation is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the installation.")
        sys.exit(1)