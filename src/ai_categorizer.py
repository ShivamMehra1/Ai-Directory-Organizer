"""
Module 2: AI Categorizer
Categorizes files using rule-based and ML techniques.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class AICategorizer:
    """Categorizes files using AI and rule-based methods."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.categories = self._load_categories(config_path)
        self.rules = self._load_rules()
    
    def _load_categories(self, config_path: Optional[str]) -> Dict:
        """Load category definitions from config file."""
        default_categories = {
            'documents': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'keywords': ['document', 'report', 'letter', 'memo'],
                'mime_types': ['application/pdf', 'application/msword']
            },
            'images': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'keywords': ['image', 'photo', 'picture', 'screenshot'],
                'mime_types': ['image/jpeg', 'image/png', 'image/gif']
            },
            'videos': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                'keywords': ['video', 'movie', 'clip', 'recording'],
                'mime_types': ['video/mp4', 'video/avi', 'video/x-msvideo']
            },
            'audio': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
                'keywords': ['audio', 'music', 'song', 'sound'],
                'mime_types': ['audio/mpeg', 'audio/wav', 'audio/flac']
            },
            'code': {
                'extensions': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', 
                              '.php', '.rb', '.go', '.rs', '.swift', '.ts'],
                'keywords': ['code', 'program', 'script', 'function', 'class'],
                'mime_types': ['text/x-python', 'text/javascript', 'text/x-java']
            },
            'archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'keywords': ['archive', 'compressed', 'zip'],
                'mime_types': ['application/zip', 'application/x-rar']
            },
            'spreadsheets': {
                'extensions': ['.xls', '.xlsx', '.csv', '.ods'],
                'keywords': ['spreadsheet', 'excel', 'data', 'table'],
                'mime_types': ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
            },
            'presentations': {
                'extensions': ['.ppt', '.pptx', '.odp'],
                'keywords': ['presentation', 'slides', 'powerpoint'],
                'mime_types': ['application/vnd.ms-powerpoint']
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    custom_categories = yaml.safe_load(f)
                    if custom_categories:
                        default_categories.update(custom_categories)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_categories
    
    def _load_rules(self) -> List[Dict]:
        """Load categorization rules."""
        return [
            {'type': 'extension', 'priority': 1},
            {'type': 'mime_type', 'priority': 2},
            {'type': 'content', 'priority': 3},
            {'type': 'filename', 'priority': 4},
        ]
    
    def categorize_file(self, file_info: Dict) -> Dict:
        """
        Categorize a file based on its metadata.
        
        Args:
            file_info: File metadata dictionary from FileAnalyzer
            
        Returns:
            Dictionary with category and confidence score
        """
        scores = {}
        
        # Rule 1: Extension-based categorization
        extension = file_info.get('extension', '')
        for category, config in self.categories.items():
            if extension in config.get('extensions', []):
                scores[category] = scores.get(category, 0) + 0.4
        
        # Rule 2: MIME type-based categorization
        mime_type = file_info.get('mime_type', '')
        if mime_type:
            for category, config in self.categories.items():
                if mime_type in config.get('mime_types', []):
                    scores[category] = scores.get(category, 0) + 0.3
        
        # Rule 3: Content-based categorization
        content_preview = file_info.get('content_preview', {})
        if content_preview:
            preview_text = content_preview.get('preview', '').lower()
            filename = file_info.get('name', '').lower()
            combined_text = preview_text + ' ' + filename
            
            for category, config in self.categories.items():
                keywords = config.get('keywords', [])
                matches = sum(1 for keyword in keywords if keyword in combined_text)
                if matches > 0:
                    scores[category] = scores.get(category, 0) + (matches * 0.1)
        
        # Rule 4: Filename-based categorization
        filename = file_info.get('name', '').lower()
        for category, config in self.categories.items():
            keywords = config.get('keywords', [])
            for keyword in keywords:
                if keyword in filename:
                    scores[category] = scores.get(category, 0) + 0.2
                    break
        
        # Rule 5: Code detection
        if content_preview and content_preview.get('has_code_keywords', False):
            scores['code'] = scores.get('code', 0) + 0.3
        
        # Determine best category
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            confidence = min(best_category[1], 1.0)  # Cap at 1.0
            category = best_category[0]
        else:
            category = 'other'
            confidence = 0.0
        
        return {
            'category': category,
            'confidence': round(confidence, 2),
            'all_scores': scores
        }
    
    def categorize_files(self, files_info: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorize multiple files.
        
        Args:
            files_info: List of file metadata dictionaries
            
        Returns:
            Dictionary mapping categories to lists of file info
        """
        categorized = {}
        
        for file_info in files_info:
            result = self.categorize_file(file_info)
            category = result['category']
            
            if category not in categorized:
                categorized[category] = []
            
            file_info['category'] = category
            file_info['confidence'] = result['confidence']
            categorized[category].append(file_info)
        
        return categorized
    
    def get_category_confidence(self, file_info: Dict, category: str) -> float:
        """
        Get confidence score for a specific category.
        
        Args:
            file_info: File metadata dictionary
            category: Category name
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        result = self.categorize_file(file_info)
        if result['category'] == category:
            return result['confidence']
        return result['all_scores'].get(category, 0.0)

