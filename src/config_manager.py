"""
Configuration Manager Module
Handles export and import of configuration settings.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Optional


class ConfigManager:
    """Manages configuration export and import."""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory for configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
    
    def export_config(self, config_data: Dict, file_path: str, 
                     format: str = 'json') -> bool:
        """
        Export configuration to a file.
        
        Args:
            config_data: Dictionary with configuration data
            file_path: Path to export file
            format: Export format ('json' or 'yaml')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            export_path = Path(file_path)
            
            if format.lower() == 'json':
                with open(export_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
            elif format.lower() == 'yaml':
                with open(export_path, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return True
        except Exception as e:
            print(f"Error exporting configuration: {e}")
            return False
    
    def import_config(self, file_path: str) -> Optional[Dict]:
        """
        Import configuration from a file.
        
        Args:
            file_path: Path to import file
            
        Returns:
            Dictionary with configuration data or None if failed
        """
        try:
            import_path = Path(file_path)
            
            if not import_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
            if import_path.suffix.lower() == '.json':
                with open(import_path, 'r') as f:
                    return json.load(f)
            elif import_path.suffix.lower() in ['.yaml', '.yml']:
                with open(import_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {import_path.suffix}")
        
        except Exception as e:
            print(f"Error importing configuration: {e}")
            return None
    
    def export_categories(self, categories: Dict, file_path: str) -> bool:
        """
        Export category definitions.
        
        Args:
            categories: Dictionary of category definitions
            file_path: Path to export file
            
        Returns:
            True if successful
        """
        config_data = {
            'version': '2.0',
            'categories': categories,
            'exported_at': str(Path(file_path).stat().st_mtime) if Path(file_path).exists() else None
        }
        return self.export_config(config_data, file_path, format='yaml')
    
    def import_categories(self, file_path: str) -> Optional[Dict]:
        """
        Import category definitions.
        
        Args:
            file_path: Path to import file
            
        Returns:
            Dictionary of category definitions or None if failed
        """
        config_data = self.import_config(file_path)
        if config_data:
            return config_data.get('categories', config_data)
        return None
    
    def create_default_config(self) -> Dict:
        """
        Create a default configuration template.
        
        Returns:
            Dictionary with default configuration structure
        """
        return {
            'version': '2.0',
            'categories': {
                'documents': {
                    'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                    'keywords': ['document', 'report', 'letter', 'memo'],
                    'mime_types': ['application/pdf', 'application/msword']
                },
                'images': {
                    'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                    'keywords': ['image', 'photo', 'picture', 'screenshot'],
                    'mime_types': ['image/jpeg', 'image/png', 'image/gif']
                }
            },
            'filters': {
                'min_size_bytes': None,
                'max_size_bytes': None,
                'exclude_patterns': []
            },
            'organization': {
                'strategy': 'category',
                'subcategorize': True,
                'preserve_structure': True
            }
        }

