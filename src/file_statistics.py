"""
Statistics Module
Provides statistics and analytics for file organization.
"""

from typing import Dict, List
from collections import defaultdict
from datetime import datetime


class Statistics:
    """Generates statistics and analytics for files."""
    
    @staticmethod
    def generate_file_statistics(files_info: List[Dict]) -> Dict:
        """
        Generate comprehensive statistics for a list of files.
        
        Args:
            files_info: List of file metadata dictionaries
            
        Returns:
            Dictionary with statistics
        """
        if not files_info:
            return {
                'total_files': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0,
                'categories': {},
                'extensions': {},
                'date_range': {}
            }
        
        total_size = sum(f.get('size', 0) for f in files_info)
        categories = defaultdict(int)
        extensions = defaultdict(int)
        sizes_by_category = defaultdict(int)
        dates = []
        
        for file_info in files_info:
            # Category statistics
            category = file_info.get('category', 'other')
            categories[category] += 1
            sizes_by_category[category] += file_info.get('size', 0)
            
            # Extension statistics
            ext = file_info.get('extension', 'no_extension')
            extensions[ext] += 1
            
            # Date statistics
            modified = file_info.get('modified')
            if modified:
                try:
                    dates.append(datetime.fromisoformat(modified))
                except (ValueError, TypeError):
                    pass
        
        # Date range
        date_range = {}
        if dates:
            date_range = {
                'oldest': min(dates).isoformat(),
                'newest': max(dates).isoformat(),
                'span_days': (max(dates) - min(dates)).days
            }
        
        return {
            'total_files': len(files_info),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_size_gb': round(total_size / (1024 * 1024 * 1024), 2),
            'average_size_bytes': round(total_size / len(files_info), 2) if files_info else 0,
            'categories': dict(categories),
            'category_sizes_mb': {k: round(v / (1024 * 1024), 2) 
                                for k, v in sizes_by_category.items()},
            'extensions': dict(extensions),
            'date_range': date_range,
            'top_categories': sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5],
            'top_extensions': sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    
    @staticmethod
    def generate_organization_statistics(stats: Dict, 
                                         categorized: Dict[str, List[Dict]]) -> Dict:
        """
        Generate statistics for organization operations.
        
        Args:
            stats: Organization statistics dictionary
            categorized: Dictionary of categorized files
            
        Returns:
            Dictionary with organization statistics
        """
        category_counts = {cat: len(files) for cat, files in categorized.items()}
        category_sizes = {}
        
        for category, files in categorized.items():
            total_size = sum(f.get('size', 0) for f in files)
            category_sizes[category] = {
                'count': len(files),
                'size_bytes': total_size,
                'size_mb': round(total_size / (1024 * 1024), 2)
            }
        
        return {
            'organization_stats': stats,
            'category_distribution': category_counts,
            'category_sizes': category_sizes,
            'success_rate': round((stats.get('moved', 0) / stats.get('total_files', 1)) * 100, 2) 
                           if stats.get('total_files', 0) > 0 else 0,
            'error_rate': round((stats.get('errors', 0) / stats.get('total_files', 1)) * 100, 2)
                         if stats.get('total_files', 0) > 0 else 0
        }
    
    @staticmethod
    def format_statistics_report(stats: Dict) -> str:
        """
        Format statistics as a readable report.
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("FILE STATISTICS REPORT")
        report.append("=" * 60)
        report.append("")
        
        report.append(f"Total Files: {stats.get('total_files', 0):,}")
        report.append(f"Total Size: {stats.get('total_size_mb', 0):.2f} MB "
                     f"({stats.get('total_size_gb', 0):.2f} GB)")
        report.append("")
        
        if stats.get('categories'):
            report.append("Category Distribution:")
            for category, count in sorted(stats['categories'].items(), 
                                       key=lambda x: x[1], reverse=True):
                size_mb = stats.get('category_sizes_mb', {}).get(category, 0)
                report.append(f"  {category:15s}: {count:5d} files ({size_mb:8.2f} MB)")
            report.append("")
        
        if stats.get('top_extensions'):
            report.append("Top Extensions:")
            for ext, count in stats['top_extensions'][:10]:
                report.append(f"  {ext or '(no extension)':15s}: {count:5d} files")
            report.append("")
        
        if stats.get('date_range'):
            dr = stats['date_range']
            report.append(f"Date Range: {dr.get('oldest', 'N/A')} to {dr.get('newest', 'N/A')}")
            report.append(f"Span: {dr.get('span_days', 0)} days")
            report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)

