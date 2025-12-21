"""
Main Application Entry Point
AI-Based Directory Management System
"""

import argparse
import sys
from pathlib import Path
from tqdm import tqdm

# Add src to path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from file_analyzer import FileAnalyzer
from ai_categorizer import AICategorizer
from directory_organizer import DirectoryOrganizer
from duplicate_detector import DuplicateDetector
from file_filter import FileFilter
from file_statistics import Statistics


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
    parser.add_argument(
        '--min-size',
        type=int,
        help='Minimum file size in bytes to include'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        help='Maximum file size in bytes to include'
    )
    parser.add_argument(
        '--exclude-ext',
        nargs='+',
        help='File extensions to exclude (e.g., .tmp .bak)'
    )
    parser.add_argument(
        '--find-duplicates',
        action='store_true',
        help='Find and report duplicate files'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Generate detailed statistics report'
    )
    parser.add_argument(
        '--cloud-upload',
        type=str,
        choices=['googledrive', 'dropbox', 'onedrive'],
        help='Upload organized files to cloud storage (googledrive, dropbox, onedrive)'
    )
    parser.add_argument(
        '--cloud-path',
        type=str,
        help='Base path in cloud storage for uploads (e.g., /OrganizedFiles)'
    )
    parser.add_argument(
        '--cloud-credentials',
        type=str,
        help='Path to cloud storage credentials file'
    )
    parser.add_argument(
        '--organize-then-upload',
        action='store_true',
        default=True,
        help='Organize files locally first, then upload (default: True)'
    )
    
    args = parser.parse_args()
    
    # Validate paths
    source_path = Path(args.source).resolve()
    target_path = Path(args.target).resolve()
    
    # Check if source and target are the same
    if source_path == target_path:
        print("Error: Source and target directories cannot be the same!")
        sys.exit(1)
    
    # Check if source is a subdirectory of target
    try:
        source_path.relative_to(target_path)
        print("Error: Source directory cannot be inside target directory!")
        sys.exit(1)
    except ValueError:
        pass  # Good, source is not inside target
    
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
        
        # Apply filters if specified
        if args.min_size or args.max_size or args.exclude_ext:
            print("Applying filters...")
            file_filter = FileFilter()
            
            if args.min_size or args.max_size:
                file_filter.add_filter(file_filter.filter_by_size(
                    min_size=args.min_size, max_size=args.max_size))
            
            if args.exclude_ext:
                file_filter.add_filter(file_filter.filter_by_extension(
                    args.exclude_ext, exclude=True))
            
            files_info = file_filter.apply_filters(files_info)
            print(f"After filtering: {len(files_info)} files")
            print()
        
        # Find duplicates if requested
        if args.find_duplicates:
            print("Finding duplicate files...")
            duplicate_detector = DuplicateDetector()
            duplicates = duplicate_detector.find_duplicates(files_info)
            summary = duplicate_detector.get_duplicate_summary(duplicates)
            
            print(f"Found {summary['duplicate_groups']} duplicate groups")
            print(f"Total duplicate files: {summary['total_duplicate_files']}")
            print(f"Wasted space: {summary['wasted_space_mb']} MB")
            print()
        
        # Generate statistics if requested
        if args.stats:
            print("Generating statistics...")
            stats_gen = Statistics()
            file_stats = stats_gen.generate_file_statistics(files_info)
            print(stats_gen.format_statistics_report(file_stats))
            print()
        
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
        
        # Generate organization statistics if requested
        if args.stats:
            stats_gen = Statistics()
            org_stats = stats_gen.generate_organization_statistics(stats, categorized)
            print("\nOrganization Statistics:")
            print(f"Success Rate: {org_stats['success_rate']}%")
            print(f"Error Rate: {org_stats['error_rate']}%")
            print()
        
        if args.dry_run:
            print("\nRun without --dry-run to execute the organization.")
        else:
            print("\nOrganization completed successfully!")
            print(f"Log file saved in: logs/")
            
            # Cloud storage upload if requested
            if args.cloud_upload:
                print("\n" + "=" * 60)
                print("Cloud Storage Upload")
                print("=" * 60)
                
                try:
                    cloud_manager = CloudStorageManager()
                    remote_path = args.cloud_path or '/OrganizedFiles'
                    
                    print(f"Uploading to {args.cloud_upload}...")
                    upload_stats = cloud_manager.organize_and_upload(
                        source_dir=args.source,
                        cloud_provider=args.cloud_upload,
                        remote_base_path=remote_path,
                        organize_first=args.organize_then_upload,
                        target_dir=args.target if args.organize_then_upload else None,
                        credentials_path=args.cloud_credentials
                    )
                    
                    print(f"\nUpload Summary:")
                    print(f"  Files uploaded: {upload_stats['uploaded']}")
                    print(f"  Files failed: {upload_stats['failed']}")
                    print(f"  Total files: {upload_stats['total_files']}")
                    print(f"\nFiles uploaded to: {remote_path}")
                    
                except Exception as e:
                    print(f"\nError uploading to cloud storage: {e}")
                    print("Make sure you have:")
                    print("  1. Installed cloud storage libraries (pip install -r requirements.txt)")
                    print("  2. Set up credentials/authentication")
                    print("  3. Provided correct credentials path if needed")
        
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

