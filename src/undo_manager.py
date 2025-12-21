"""
Undo Manager Module
Manages undo/redo operations for file organization.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class UndoManager:
    """Manages undo/redo operations for file organization."""
    
    def __init__(self, undo_dir: str = "undo_history"):
        """
        Initialize undo manager.
        
        Args:
            undo_dir: Directory to store undo history
        """
        self.undo_dir = Path(undo_dir)
        self.undo_dir.mkdir(exist_ok=True)
        self.history_file = self.undo_dir / "history.json"
        self.history = self._load_history()
        self.current_index = len(self.history) - 1
    
    def _load_history(self) -> List[Dict]:
        """Load undo history from disk."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_history(self):
        """Save undo history to disk."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save undo history: {e}")
    
    def record_operation(self, operation_type: str, operations: List[Dict],
                        timestamp: Optional[datetime] = None):
        """
        Record an organization operation for undo.
        
        Args:
            operation_type: Type of operation ('organize', 'delete', etc.)
            operations: List of operation dictionaries with source/destination
            timestamp: Operation timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        undo_entry = {
            'type': operation_type,
            'timestamp': timestamp.isoformat(),
            'operations': operations,
            'id': len(self.history)
        }
        
        # Remove any future history if we're not at the end
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        self.history.append(undo_entry)
        self.current_index = len(self.history) - 1
        self._save_history()
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.current_index >= 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.current_index < len(self.history) - 1
    
    def undo(self) -> Optional[Dict]:
        """
        Undo the last operation.
        
        Returns:
            Dictionary with undo result or None if no undo available
        """
        if not self.can_undo():
            return None
        
        entry = self.history[self.current_index]
        operations = entry['operations']
        undone = 0
        errors = 0
        
        for op in operations:
            if op['status'] == 'moved':
                # Reverse the operation: delete destination, restore if needed
                destination = Path(op.get('destination'))
                if destination and destination.exists():
                    try:
                        destination.unlink()
                        undone += 1
                    except Exception as e:
                        errors += 1
        
        self.current_index -= 1
        self._save_history()
        
        return {
            'success': True,
            'undone': undone,
            'errors': errors,
            'entry': entry
        }
    
    def redo(self) -> Optional[Dict]:
        """
        Redo the last undone operation.
        
        Returns:
            Dictionary with redo result or None if no redo available
        """
        if not self.can_redo():
            return None
        
        self.current_index += 1
        entry = self.history[self.current_index]
        
        # Note: Full redo would require re-running the organization
        # This is a simplified version
        return {
            'success': True,
            'message': 'Redo requires re-running organization',
            'entry': entry
        }
    
    def get_history_summary(self) -> Dict:
        """
        Get summary of undo history.
        
        Returns:
            Dictionary with history statistics
        """
        return {
            'total_operations': len(self.history),
            'current_index': self.current_index,
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo(),
            'recent_operations': self.history[-5:] if self.history else []
        }
    
    def clear_history(self):
        """Clear all undo history."""
        self.history = []
        self.current_index = -1
        self._save_history()

