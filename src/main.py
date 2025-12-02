"""
Main Application Entry Point
AI-Based Directory Management System
"""

import argparse
import sys
from pathlib import Path
from tqdm import tqdm

from file_analyzer import FileAnalyzer
from ai_categorizer import AICategorizer
from directory_organizer import DirectoryOrganizer


def main():
    """Main application function."""
    parser = argparse.ArgumentParser(
        description='AI-Based Directory Management System'
    )
    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='Source directory to organize'
    )
    parser.add_argument(
        '--target',
        type=str,
        required=True,
        help='Target directory for organized files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without executing'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        default=True,
        help='Scan directories recursively (default: True)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom categories configuration file'
    )
    parser.add_argument(
        '--strategy',
        type=str,
        choices=['category', 'date'],
        default='category',
        help='Organization strategy (default: category)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AI-Based Directory Management System")
    print("=" * 60)
    print(f"Source: {args.source}")
    print(f"Target: {args.target}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)
    print()
    
    try:
        # Module 1: File Analyzer
        print("Step 1: Analyzing files...")
        analyzer = FileAnalyzer()
        files_info = analyzer.scan_directory(args.source, recursive=args.recursive)
        print(f"Found {len(files_info)} files")
        print()
        
        if not files_info:
            print("No files found to organize.")
            return
        
        # Module 2: AI Categorizer
        print("Step 2: Categorizing files...")
        categorizer = AICategorizer(config_path=args.config)
        
        with tqdm(total=len(files_info), desc="Categorizing") as pbar:
            categorized = categorizer.categorize_files(files_info)
            pbar.update(len(files_info))
        
        print(f"Categorized into {len(categorized)} categories:")
        for category, files in categorized.items():
            print(f"  - {category}: {len(files)} files")
        print()
        
        # Module 3: Directory Organizer
        print("Step 3: Organizing files...")
        organizer = DirectoryOrganizer(args.target, dry_run=args.dry_run, subcategorize=True)
        
        if args.dry_run:
            print("DRY RUN MODE - Preview only (files will be copied, originals preserved)")
            print()
        
        stats = organizer.organize_files(categorized, organization_strategy=args.strategy, 
                                         subcategorize=True, preserve_structure=True)
        
        # Print summary
        print(organizer.get_organization_summary(stats))
        
        if args.dry_run:
            print("\nRun without --dry-run to execute the organization.")
        else:
            print("\nOrganization completed successfully!")
            print(f"Log file saved in: logs/")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

