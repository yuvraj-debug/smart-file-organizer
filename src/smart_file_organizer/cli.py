import argparse
import sys
from . import __version__

def main():
    """Main entry point for the Smart File Organizer CLI."""
    parser = argparse.ArgumentParser(
        description="Smart File Organizer - Organize your files intelligently"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Smart File Organizer v{__version__}"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["organize", "undo", "config"],
        help="Sub-command to run"
    )
    
    # If no command is provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    if args.command == "organize":
        print("Organize command called")
        # TODO: Implement organize logic
    elif args.command == "undo":
        print("Undo command called")
        # TODO: Implement undo logic
    elif args.command == "config":
        print("Config command called")
        # TODO: Implement config logic
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()