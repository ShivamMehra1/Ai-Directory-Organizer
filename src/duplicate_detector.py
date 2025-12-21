"""
Duplicate File Detector Module
Detects duplicate files using hash comparison and file size.
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class DuplicateDetector:
    """Detects duplicate files in a directory."""
    
    def __init__(self, chunk_size: int = 8192):
        """
        Initialize duplicate detector.
        
        Args:
            chunk_size: Size of chunks to read when hashing files (default: 8KB)
        """
        self.chunk_size = chunk_size
        self.hash_cache = {}
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = 'md5') -> str:
        """
        Calculate hash of a file.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use ('md5', 'sha1', 'sha256')
            
        Returns:
            Hexadecimal hash string
        """
        if file_path in self.hash_cache:
            return self.hash_cache[file_path]
        
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(self.chunk_size):
                    hash_obj.update(chunk)
            
            hash_value = hash_obj.hexdigest()
            self.hash_cache[file_path] = hash_value
            return hash_value
        except (IOError, OSError) as e:
            raise Exception(f"Error reading file {file_path}: {e}")
    
    def find_duplicates_by_size(self, files_info: List[Dict]) -> Dict[int, List[Dict]]:
        """
        Group files by size to find potential duplicates.
        
        Args:
            files_info: List of file metadata dictionaries
            
        Returns:
            Dictionary mapping file sizes to lists of file info
        """
        size_groups = defaultdict(list)
        
        for file_info in files_info:
            size = file_info.get('size', 0)
            if size > 0:  # Skip empty files
                size_groups[size].append(file_info)
        
        # Filter out sizes with only one file (no duplicates)
        return {size: files for size, files in size_groups.items() if len(files) > 1}
    
    def find_duplicates_by_hash(self, files_info: List[Dict], 
                               algorithm: str = 'md5') -> Dict[str, List[Dict]]:
        """
        Find duplicate files by comparing hashes.
        
        Args:
            files_info: List of file metadata dictionaries
            algorithm: Hash algorithm to use
            
        Returns:
            Dictionary mapping hashes to lists of duplicate file info
        """
        # First, group by size (faster initial filter)
        size_groups = self.find_duplicates_by_size(files_info)
        
        hash_groups = defaultdict(list)
        
        for size, files in size_groups.items():
            for file_info in files:
                file_path = Path(file_info['path'])
                try:
                    file_hash = self.calculate_file_hash(file_path, algorithm)
                    hash_groups[file_hash].append(file_info)
                except Exception as e:
                    # Skip files that can't be hashed
                    continue
        
        # Filter out hashes with only one file (no duplicates)
        return {file_hash: files for file_hash, files in hash_groups.items() if len(files) > 1}
    
    def find_duplicates(self, files_info: List[Dict], 
                       use_hash: bool = True) -> Dict[str, List[Dict]]:
        """
        Find duplicate files.
        
        Args:
            files_info: List of file metadata dictionaries
            use_hash: Whether to use hash comparison (more accurate but slower)
            
        Returns:
            Dictionary mapping identifiers to lists of duplicate file info
        """
        if use_hash:
            return self.find_duplicates_by_hash(files_info)
        else:
            return self.find_duplicates_by_size(files_info)
    
    def get_duplicate_summary(self, duplicates: Dict[str, List[Dict]]) -> Dict:
        """
        Generate summary of duplicate files.
        
        Args:
            duplicates: Dictionary of duplicate files
            
        Returns:
            Summary dictionary with statistics
        """
        total_duplicate_groups = len(duplicates)
        total_duplicate_files = sum(len(files) for files in duplicates.values())
        total_wasted_space = 0
        
        for files in duplicates.values():
            if files:
                # Calculate wasted space (all but one copy)
                file_size = files[0].get('size', 0)
                wasted = file_size * (len(files) - 1)
                total_wasted_space += wasted
        
        return {
            'duplicate_groups': total_duplicate_groups,
            'total_duplicate_files': total_duplicate_files,
            'wasted_space_bytes': total_wasted_space,
            'wasted_space_mb': round(total_wasted_space / (1024 * 1024), 2),
            'duplicates': duplicates
        }

