"""
Module 3: Directory Organizer
Organizes files into structured directory hierarchies.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class DirectoryOrganizer:
    """Organizes files into structured directory hierarchies."""
    
    def __init__(self, target_path: str, dry_run: bool = False, subcategorize: bool = True, 
                 preserve_structure: bool = True):
        self.target_path = Path(target_path)
        self.dry_run = dry_run
        self.subcategorize = subcategorize
        self.preserve_structure = preserve_structure
        self.operations_log = []
        self.setup_logging()
        
        # Mapping of extensions to subdirectory names
        self.extension_to_subdir = self._create_extension_mapping()
        
        if not dry_run:
            self.target_path.mkdir(parents=True, exist_ok=True)
    
    def _create_extension_mapping(self) -> Dict[str, str]:
        """Create mapping of file extensions to subdirectory names."""
        return {
            # Documents
            '.pdf': 'pdf',
            '.doc': 'doc',
            '.docx': 'docx',
            '.txt': 'txt',
            '.rtf': 'rtf',
            '.odt': 'odt',
            '.xls': 'xls',
            '.xlsx': 'xlsx',
            '.ppt': 'ppt',
            '.pptx': 'pptx',
            '.csv': 'csv',
            '.ods': 'ods',
            '.odp': 'odp',
            
            # Images
            '.jpg': 'jpg',
            '.jpeg': 'jpeg',
            '.png': 'png',
            '.gif': 'gif',
            '.bmp': 'bmp',
            '.svg': 'svg',
            '.webp': 'webp',
            '.ico': 'ico',
            '.tiff': 'tiff',
            '.tif': 'tif',
            
            # Videos
            '.mp4': 'mp4',
            '.avi': 'avi',
            '.mkv': 'mkv',
            '.mov': 'mov',
            '.wmv': 'wmv',
            '.flv': 'flv',
            '.webm': 'webm',
            '.mpg': 'mpg',
            '.mpeg': 'mpeg',
            
            # Audio
            '.mp3': 'mp3',
            '.wav': 'wav',
            '.flac': 'flac',
            '.aac': 'aac',
            '.ogg': 'ogg',
            '.m4a': 'm4a',
            '.wma': 'wma',
            
            # Code
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.html': 'html',
            '.css': 'css',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.json': 'json',
            '.xml': 'xml',
            
            # Archives
            '.zip': 'zip',
            '.rar': 'rar',
            '.7z': '7z',
            '.tar': 'tar',
            '.gz': 'gz',
            '.bz2': 'bz2',
            '.xz': 'xz',
        }
    
    def setup_logging(self):
        """Setup logging for operations."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"organization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_directory_structure(self, categories: List[str]) -> Dict[str, Path]:
        """
        Create directory structure for categories.
        
        Args:
            categories: List of category names
            
        Returns:
            Dictionary mapping categories to their directory paths
        """
        category_paths = {}
        
        for category in categories:
            category_dir = self.target_path / category
            category_paths[category] = category_dir
            
            if not self.dry_run:
                category_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Created directory: {category_dir}")
            else:
                self.logger.info(f"[DRY RUN] Would create directory: {category_dir}")
        
        return category_paths
    
    def organize_files(self, file_category_map: Dict[str, List[Dict]], 
                      organization_strategy: str = 'category', subcategorize: bool = True,
                      preserve_structure: bool = True) -> Dict:
        """
        Organize files based on their categories.
        
        Args:
            file_category_map: Dictionary mapping categories to file info lists
            organization_strategy: Strategy for organization ('category', 'date', 'type', 'preserve')
            subcategorize: Whether to create subdirectories by file extension
            preserve_structure: Whether to preserve original folder structure
            
        Returns:
            Dictionary with organization statistics
        """
        # Update settings
        self.subcategorize = subcategorize
        self.preserve_structure = preserve_structure
        
        stats = {
            'total_files': 0,
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'operations': []
        }
        
        # If preserving structure, organize differently
        if self.preserve_structure and organization_strategy != 'date':
            return self._organize_with_structure(file_category_map, stats)
        
        category_paths = self.create_directory_structure(list(file_category_map.keys()))
        
        for category, files in file_category_map.items():
            target_dir = category_paths.get(category, self.target_path / category)
            
            for file_info in files:
                stats['total_files'] += 1
                source_path = Path(file_info['path'])
                
                try:
                    if organization_strategy == 'category':
                        destination = self._get_destination_path(source_path, target_dir, file_info)
                    elif organization_strategy == 'date':
                        # For date strategy, still use subcategorization if enabled
                        if self.subcategorize:
                            date_path = self._get_destination_by_date(source_path, target_dir, file_info)
                            # Add subdirectory based on extension
                            extension = source_path.suffix.lower()
                            subdir_name = self.extension_to_subdir.get(extension, 'other')
                            subdir = date_path.parent / subdir_name
                            if not self.dry_run:
                                subdir.mkdir(parents=True, exist_ok=True)
                            destination = subdir / source_path.name
                        else:
                            destination = self._get_destination_by_date(source_path, target_dir, file_info)
                    else:
                        destination = self._get_destination_path(source_path, target_dir, file_info)
                    
                    result = self._move_file(source_path, destination)
                    stats['operations'].append(result)
                    
                    if result['status'] == 'moved':
                        stats['moved'] += 1
                    elif result['status'] == 'skipped':
                        stats['skipped'] += 1
                    else:
                        stats['errors'] += 1
                        
                except Exception as e:
                    stats['errors'] += 1
                    self.logger.error(f"Error organizing {source_path}: {e}")
                    stats['operations'].append({
                        'source': str(source_path),
                        'destination': None,
                        'status': 'error',
                        'error': str(e)
                    })
        
        return stats
    
    def _organize_with_structure(self, file_category_map: Dict[str, List[Dict]], stats: Dict) -> Dict:
        """
        Organize files while preserving original folder structure.
        Structure: target/original_folder/category/subcategory/file
        """
        # Group files by their relative path (original folder structure)
        files_by_folder = {}
        
        for category, files in file_category_map.items():
            for file_info in files:
                relative_path = file_info.get('relative_path', '')
                if relative_path not in files_by_folder:
                    files_by_folder[relative_path] = {}
                if category not in files_by_folder[relative_path]:
                    files_by_folder[relative_path][category] = []
                files_by_folder[relative_path][category].append(file_info)
        
        # Organize each folder separately
        for folder_path, categories in files_by_folder.items():
            # Create base directory for this folder
            # Empty folder_path means files are in root of source
            if folder_path and folder_path.strip():
                folder_base = self.target_path / folder_path
            else:
                # Files in root go to a 'root' folder to distinguish from organized structure
                folder_base = self.target_path
            
            # Create category directories within this folder
            for category, files in categories.items():
                category_dir = folder_base / category
                
                for file_info in files:
                    stats['total_files'] += 1
                    source_path = Path(file_info['path'])
                    
                    try:
                        destination = self._get_destination_path(source_path, category_dir, file_info)
                        result = self._move_file(source_path, destination)
                        stats['operations'].append(result)
                        
                        if result['status'] == 'moved':
                            stats['moved'] += 1
                        elif result['status'] == 'skipped':
                            stats['skipped'] += 1
                        else:
                            stats['errors'] += 1
                            
                    except Exception as e:
                        stats['errors'] += 1
                        self.logger.error(f"Error organizing {source_path}: {e}")
                        stats['operations'].append({
                            'source': str(source_path),
                            'destination': None,
                            'status': 'error',
                            'error': str(e)
                        })
        
        return stats
    
    def _get_destination_path(self, source_path: Path, target_dir: Path, file_info: Dict = None) -> Path:
        """
        Get destination path for a file.
        Creates subdirectories based on file extension if subcategorize is enabled.
        """
        if self.subcategorize:
            extension = source_path.suffix.lower()
            subdir_name = self.extension_to_subdir.get(extension, 'other')
            subdir = target_dir / subdir_name
            
            if not self.dry_run:
                subdir.mkdir(parents=True, exist_ok=True)
            
            return subdir / source_path.name
        else:
            return target_dir / source_path.name
    
    def _get_destination_by_date(self, source_path: Path, target_dir: Path, 
                                 file_info: Dict) -> Path:
        """Get destination path organized by date."""
        try:
            modified_date = datetime.fromisoformat(file_info['modified'])
            date_dir = target_dir / modified_date.strftime('%Y-%m')
            if not self.dry_run:
                date_dir.mkdir(parents=True, exist_ok=True)
            return date_dir / source_path.name
        except:
            return target_dir / source_path.name
    
    def _move_file(self, source_path: Path, destination: Path) -> Dict:
        """
        Copy a file to destination with conflict resolution.
        Original file is preserved (not moved/deleted).
        
        Args:
            source_path: Source file path
            destination: Destination file path
            
        Returns:
            Dictionary with operation result
        """
        if not source_path.exists():
            return {
                'source': str(source_path),
                'destination': str(destination),
                'status': 'error',
                'error': 'Source file does not exist'
            }
        
        # Handle conflicts
        if destination.exists():
            destination = self._handle_conflicts(source_path, destination)
            if destination is None:
                return {
                    'source': str(source_path),
                    'destination': str(destination),
                    'status': 'skipped',
                    'reason': 'Conflict resolution resulted in skip'
                }
        
        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would copy: {source_path} -> {destination}")
            return {
                'source': str(source_path),
                'destination': str(destination),
                'status': 'dry_run'
            }
        
        try:
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file (preserve original) - copy2 preserves metadata
            shutil.copy2(str(source_path), str(destination))
            
            self.logger.info(f"Copied: {source_path} -> {destination} (original preserved)")
            return {
                'source': str(source_path),
                'destination': str(destination),
                'status': 'moved'  # Keep status as 'moved' for compatibility
            }
        except Exception as e:
            self.logger.error(f"Error copying {source_path}: {e}")
            return {
                'source': str(source_path),
                'destination': str(destination),
                'status': 'error',
                'error': str(e)
            }
    
    def _handle_conflicts(self, source_path: Path, destination: Path) -> Optional[Path]:
        """
        Handle file conflicts when destination already exists.
        
        Args:
            source_path: Source file path
            destination: Destination file path
            
        Returns:
            New destination path or None to skip
        """
        # Strategy: Add number suffix
        base_name = destination.stem
        extension = destination.suffix
        parent = destination.parent
        
        counter = 1
        while destination.exists():
            new_name = f"{base_name}_{counter}{extension}"
            destination = parent / new_name
            counter += 1
            
            # Prevent infinite loop
            if counter > 1000:
                self.logger.warning(f"Too many conflicts for {source_path}, skipping")
                return None
        
        return destination
    
    def dry_run_preview(self, file_category_map: Dict[str, List[Dict]]) -> Dict:
        """
        Preview organization without executing.
        
        Args:
            file_category_map: Dictionary mapping categories to file info lists
            
        Returns:
            Preview statistics
        """
        original_dry_run = self.dry_run
        self.dry_run = True
        
        preview = self.organize_files(file_category_map)
        
        self.dry_run = original_dry_run
        return preview
    
    def get_organization_summary(self, stats: Dict) -> str:
        """
        Generate a summary of organization operations.
        
        Args:
            stats: Statistics dictionary from organize_files
            
        Returns:
            Formatted summary string
        """
        summary = f"""
Organization Summary:
====================
Total Files: {stats['total_files']}
Successfully Copied: {stats['moved']} (originals preserved)
Skipped: {stats['skipped']}
Errors: {stats['errors']}
"""
        return summary

