"""
File Filter Module
Provides filtering capabilities for files based on various criteria.
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Set


class FileFilter:
    """Filters files based on various criteria."""
    
    def __init__(self):
        """Initialize file filter."""
        self.filters = []
    
    def add_filter(self, filter_func: Callable[[Dict], bool]):
        """
        Add a custom filter function.
        
        Args:
            filter_func: Function that takes file_info dict and returns True to include
        """
        self.filters.append(filter_func)
    
    def filter_by_size(self, min_size: Optional[int] = None, 
                      max_size: Optional[int] = None) -> Callable:
        """
        Create a size filter.
        
        Args:
            min_size: Minimum file size in bytes (None for no minimum)
            max_size: Maximum file size in bytes (None for no maximum)
            
        Returns:
            Filter function
        """
        def size_filter(file_info: Dict) -> bool:
            size = file_info.get('size', 0)
            if min_size is not None and size < min_size:
                return False
            if max_size is not None and size > max_size:
                return False
            return True
        
        return size_filter
    
    def filter_by_extension(self, extensions: List[str], 
                           exclude: bool = False) -> Callable:
        """
        Create an extension filter.
        
        Args:
            extensions: List of extensions (with or without dot)
            exclude: If True, exclude these extensions; if False, include only these
            
        Returns:
            Filter function
        """
        # Normalize extensions (ensure they start with dot)
        normalized_exts = {ext if ext.startswith('.') else f'.{ext}' 
                          for ext in extensions}
        normalized_exts = {ext.lower() for ext in normalized_exts}
        
        def extension_filter(file_info: Dict) -> bool:
            file_ext = file_info.get('extension', '').lower()
            if exclude:
                return file_ext not in normalized_exts
            else:
                return file_ext in normalized_exts
        
        return extension_filter
    
    def filter_by_date(self, min_date: Optional[datetime] = None,
                      max_date: Optional[datetime] = None,
                      date_field: str = 'modified') -> Callable:
        """
        Create a date filter.
        
        Args:
            min_date: Minimum date (None for no minimum)
            max_date: Maximum date (None for no maximum)
            date_field: Field to use ('created' or 'modified')
            
        Returns:
            Filter function
        """
        def date_filter(file_info: Dict) -> bool:
            date_str = file_info.get(date_field)
            if not date_str:
                return False
            
            try:
                file_date = datetime.fromisoformat(date_str)
                
                if min_date and file_date < min_date:
                    return False
                if max_date and file_date > max_date:
                    return False
                return True
            except (ValueError, TypeError):
                return False
        
        return date_filter
    
    def filter_by_name_pattern(self, pattern: str, 
                              case_sensitive: bool = False) -> Callable:
        """
        Create a filename pattern filter using regex.
        
        Args:
            pattern: Regular expression pattern
            case_sensitive: Whether pattern matching is case sensitive
            
        Returns:
            Filter function
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        
        def pattern_filter(file_info: Dict) -> bool:
            filename = file_info.get('name', '')
            return bool(regex.search(filename))
        
        return pattern_filter
    
    def filter_by_exclude_patterns(self, patterns: List[str],
                                  case_sensitive: bool = False) -> Callable:
        """
        Create an exclude pattern filter.
        
        Args:
            patterns: List of regex patterns to exclude
            case_sensitive: Whether pattern matching is case sensitive
            
        Returns:
            Filter function
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        regexes = [re.compile(pattern, flags) for pattern in patterns]
        
        def exclude_filter(file_info: Dict) -> bool:
            filename = file_info.get('name', '')
            path = file_info.get('path', '')
            
            # Check filename
            for regex in regexes:
                if regex.search(filename):
                    return False
            
            # Check full path
            for regex in regexes:
                if regex.search(path):
                    return False
            
            return True
        
        return exclude_filter
    
    def filter_by_category(self, categories: List[str],
                          exclude: bool = False) -> Callable:
        """
        Create a category filter.
        
        Args:
            categories: List of category names
            exclude: If True, exclude these categories; if False, include only these
            
        Returns:
            Filter function
        """
        category_set = set(categories)
        
        def category_filter(file_info: Dict) -> bool:
            file_category = file_info.get('category', 'other')
            if exclude:
                return file_category not in category_set
            else:
                return file_category in category_set
        
        return category_filter
    
    def apply_filters(self, files_info: List[Dict]) -> List[Dict]:
        """
        Apply all registered filters to a list of files.
        
        Args:
            files_info: List of file metadata dictionaries
            
        Returns:
            Filtered list of file info dictionaries
        """
        filtered = files_info
        
        for filter_func in self.filters:
            filtered = [f for f in filtered if filter_func(f)]
        
        return filtered
    
    def clear_filters(self):
        """Clear all registered filters."""
        self.filters = []

