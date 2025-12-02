"""
Module 1: File Analyzer
Extracts file metadata, analyzes content, and identifies file types.
"""

import os
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import magic


class FileAnalyzer:
    """Analyzes files and extracts metadata for categorization."""
    
    def __init__(self):
        self.supported_text_extensions = {'.txt', '.py', '.js', '.java', '.cpp', 
                                         '.c', '.html', '.css', '.md', '.json', 
                                         '.xml', '.csv', '.log'}
        
    def scan_directory(self, directory_path: str, recursive: bool = True) -> List[Dict]:
        """
        Scan a directory and collect file information.
        
        Args:
            directory_path: Path to the directory to scan
            recursive: Whether to scan subdirectories recursively
            
        Returns:
            List of file information dictionaries
        """
        files_info = []
        path = Path(directory_path).resolve()
        source_root = path
        
        if not path.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                try:
                    file_info = self.extract_metadata(str(file_path))
                    # Store relative path from source root to preserve folder structure
                    try:
                        relative_path = file_path.relative_to(source_root)
                        file_info['relative_path'] = str(relative_path.parent) if relative_path.parent != Path('.') else ''
                        file_info['source_root'] = str(source_root)
                    except ValueError:
                        # If relative path calculation fails, use empty
                        file_info['relative_path'] = ''
                        file_info['source_root'] = str(source_root)
                    files_info.append(file_info)
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
                    continue
        
        return files_info
    
    def extract_metadata(self, file_path: str) -> Dict:
        """
        Extract metadata from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat_info = path.stat()
        
        metadata = {
            'path': str(path.absolute()),
            'name': path.name,
            'extension': path.suffix.lower(),
            'size': stat_info.st_size,
            'size_mb': round(stat_info.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            'is_readable': os.access(file_path, os.R_OK),
            'is_writable': os.access(file_path, os.W_OK),
        }
        
        # Detect MIME type
        metadata['mime_type'] = self.detect_mime_type(file_path)
        
        # Analyze content for text files
        if path.suffix.lower() in self.supported_text_extensions:
            metadata['content_preview'] = self.analyze_content(file_path)
        
        return metadata
    
    def detect_mime_type(self, file_path: str) -> Optional[str]:
        """
        Detect MIME type of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            MIME type string or None
        """
        try:
            # Try python-magic first (more accurate)
            mime = magic.Magic(mime=True)
            return mime.from_file(file_path)
        except:
            # Fallback to mimetypes
            mime_type, _ = mimetypes.guess_type(file_path)
            return mime_type
    
    def analyze_content(self, file_path: str, max_chars: int = 500) -> Optional[Dict]:
        """
        Analyze content of text-based files.
        
        Args:
            file_path: Path to the file
            max_chars: Maximum characters to read for preview
            
        Returns:
            Dictionary with content analysis or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_chars)
                
            analysis = {
                'preview': content[:max_chars],
                'length': len(content),
                'line_count': content.count('\n') + 1,
                'has_code_keywords': self._has_code_keywords(content),
            }
            
            return analysis
        except Exception as e:
            return None
    
    def _has_code_keywords(self, content: str) -> bool:
        """Check if content contains programming keywords."""
        code_keywords = ['def ', 'function', 'class ', 'import ', 'public ', 
                        'private ', 'void ', 'int ', 'return ', 'if ', 'else ']
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in code_keywords)
    
    def get_file_type_category(self, file_path: str) -> str:
        """
        Get general file type category based on extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            General category name
        """
        extension = Path(file_path).suffix.lower()
        
        type_map = {
            'documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'},
            'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'},
            'videos': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'},
            'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'},
            'archives': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'},
            'code': {'.py', '.js', '.java', '.cpp', '.c', '.html', '.css', 
                    '.php', '.rb', '.go', '.rs', '.swift'},
            'spreadsheets': {'.xls', '.xlsx', '.csv', '.ods'},
            'presentations': {'.ppt', '.pptx', '.odp'},
        }
        
        for category, extensions in type_map.items():
            if extension in extensions:
                return category
        
        return 'other'

