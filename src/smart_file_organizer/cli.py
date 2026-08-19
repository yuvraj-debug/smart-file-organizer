import argparse
import sys
import os
from pathlib import Path
from . import __version__
from .organizer import organize_files_by_extension, organize_files_by_date
from .rules import organize_files_with_rules
from .safety import organize_with_safety, generate_report, print_report, OperationLogger
from .utils import load_config

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
    
    # Organize command arguments
    parser.add_argument(
        "--by-date",
        choices=["created", "modified"],
        help="Organize by file date (created or modified)"
    )
    parser.add_argument(
        "--date-format",
        choices=["year", "month", "day"],
        default="month",
        help="Date folder structure (default: month)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to custom rules JSON file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Increase output verbosity"
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Files or directories to ignore (can specify multiple)"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Directory to organize (default: current directory)"
    )
    
    # If no command is provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    if args.command == "organize":
        # Load configuration
        config = load_config(args.config)
        
        # Prepare ignore patterns
        ignore_patterns = config.get("ignore", []) + args.ignore
        
        # Set up logging level
        if args.verbose:
            import logging
            logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
            logging.info(f"Verbose mode enabled. Organizing directory: {args.directory}")
            if args.by_date:
                logging.info(f"Organization method: by date ({args.by_date}), format: {args.date_format}")
            elif args.config:
                logging.info(f"Organization method: custom rules from {args.config}")
            else:
                logging.info("Organization method: by file extension")
            if ignore_patterns:
                logging.info(f"Ignore patterns: {ignore_patterns}")
            if args.dry_run:
                logging.info("DRY RUN mode: No changes will be made")
        
        # Choose organization method
        if args.by_date:
            organize_func = organize_files_by_date
            organize_args = (args.by_date, args.date_format)
            organize_kwargs = {}
        elif args.config:
            organize_func = organize_files_with_rules
            organize_args = (config.get("categories", {}),)
            organize_kwargs = {"ignore_patterns": ignore_patterns}
        else:
            organize_func = organize_files_by_extension
            organize_args = (config.get("categories", {}),)
            organize_kwargs = {"ignore_patterns": ignore_patterns}
        
        # Run organization with safety features
        operations, operation_id = organize_with_safety(
            args.directory,
            organize_func,
            *organize_args,
            dry_run=args.dry_run,
            enable_undo=True,
            **organize_kwargs
        )
        
        # Generate and print report
        if not args.dry_run:
            report = generate_report(operations)
            print_report(report)
        else:
            print("DRY RUN: No changes were made.")
            if operations:
                report = generate_report(operations)
                print_report(report)
    
    elif args.command == "undo":
        if undo_last_operation():
            print("Last operation undone successfully.")
        else:
            print("Could not undo last operation.")
            sys.exit(1)
    
    elif args.command == "config":
        print("Config management not yet implemented.")
        # TODO: Implement config command
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()