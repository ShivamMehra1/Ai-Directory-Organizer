"""
GUI Version of AI-Based Directory Management System
Built with tkinter for Windows
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
from pathlib import Path
import os

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
from undo_manager import UndoManager
from cloud_storage import CloudStorageManager
from cloud_auth_helper import CloudAuthHelper


class DirectoryManagementGUI:
    """GUI Application for Directory Management System."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Directory Management System")
        self.root.geometry("900x850")
        self.root.resizable(True, True)
        
        # Variables
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()
        self.strategy = tk.StringVar(value="category")
        self.dry_run = tk.BooleanVar(value=True)
        self.is_running = False
        self.find_duplicates = tk.BooleanVar(value=False)
        self.show_stats = tk.BooleanVar(value=False)
        self.min_size = tk.StringVar()
        self.max_size = tk.StringVar()
        self.exclude_patterns = tk.StringVar()
        self.cloud_provider = tk.StringVar(value="")
        self.cloud_path = tk.StringVar(value="/OrganizedFiles")
        self.cloud_credentials = tk.StringVar()
        self.upload_to_cloud = tk.BooleanVar(value=False)
        
        # Initialize managers
        self.undo_manager = UndoManager()
        self.cloud_manager = CloudStorageManager()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="AI-Based Directory Management System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Source directory
        ttk.Label(main_frame, text="Source Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.source_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=1, column=2, pady=5)
        
        # Target directory
        ttk.Label(main_frame, text="Target Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.target_path, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_target).grid(row=2, column=2, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Organization strategy
        ttk.Label(options_frame, text="Organization Strategy:").grid(row=0, column=0, sticky=tk.W, pady=5)
        strategy_combo = ttk.Combobox(options_frame, textvariable=self.strategy, 
                                      values=["category", "date"], state="readonly", width=20)
        strategy_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Dry run checkbox
        ttk.Checkbutton(options_frame, text="Dry Run (Preview Only)", 
                       variable=self.dry_run).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Additional options
        ttk.Checkbutton(options_frame, text="Find Duplicates", 
                       variable=self.find_duplicates).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_frame, text="Show Statistics", 
                       variable=self.show_stats).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Filtering options
        filter_frame = ttk.LabelFrame(main_frame, text="File Filters (Optional)", padding="10")
        filter_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(filter_frame, text="Min Size (bytes):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(filter_frame, textvariable=self.min_size, width=15).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Max Size (bytes):").grid(row=0, column=2, sticky=tk.W, padx=(10, 0), pady=2)
        ttk.Entry(filter_frame, textvariable=self.max_size, width=15).grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Exclude Patterns (comma-separated):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(filter_frame, textvariable=self.exclude_patterns, width=40).grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Cloud storage options
        cloud_frame = ttk.LabelFrame(main_frame, text="Cloud Storage Upload (Optional)", padding="10")
        cloud_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(cloud_frame, text="Upload to Cloud Storage", 
                       variable=self.upload_to_cloud).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        ttk.Label(cloud_frame, text="Provider:").grid(row=1, column=0, sticky=tk.W, pady=2)
        cloud_combo = ttk.Combobox(cloud_frame, textvariable=self.cloud_provider, 
                                  values=["", "googledrive", "dropbox", "onedrive"], 
                                  state="readonly", width=20)
        cloud_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(cloud_frame, text="Cloud Path:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(cloud_frame, textvariable=self.cloud_path, width=30).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(cloud_frame, text="Credentials File:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(cloud_frame, textvariable=self.cloud_credentials, width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Button(cloud_frame, text="Browse", command=self.browse_credentials).grid(row=3, column=2, padx=5, pady=2)
        
        # Setup helper buttons
        help_frame = ttk.Frame(cloud_frame)
        help_frame.grid(row=4, column=0, columnspan=3, pady=5, sticky=tk.W)
        
        ttk.Button(help_frame, text="📖 Setup Guide", command=self.show_setup_guide, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Button(help_frame, text="🔍 Validate Credentials", command=self.validate_credentials, width=20).pack(side=tk.LEFT, padx=2)
        ttk.Button(help_frame, text="🌐 Open Console", command=self.open_cloud_console, width=18).pack(side=tk.LEFT, padx=2)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Organization", 
                                       command=self.start_organization, width=20)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                      command=self.stop_organization, state=tk.DISABLED, width=20)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Undo", command=self.undo_operation, width=15).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_source(self):
        """Browse for source directory."""
        directory = filedialog.askdirectory(title="Select Source Directory")
        if directory:
            self.source_path.set(directory)
            self.log("Source directory selected: " + directory)
    
    def browse_target(self):
        """Browse for target directory."""
        directory = filedialog.askdirectory(title="Select Target Directory")
        if directory:
            self.target_path.set(directory)
            self.log("Target directory selected: " + directory)
    
    def browse_credentials(self):
        """Browse for cloud storage credentials file."""
        provider = self.cloud_provider.get()
        
        if provider == "googledrive":
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        elif provider == "dropbox":
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        else:
            filetypes = [("All files", "*.*")]
        
        filename = filedialog.askopenfilename(
            title="Select Credentials File",
            filetypes=filetypes
        )
        if filename:
            self.cloud_credentials.set(filename)
            self.log("Credentials file selected: " + filename)
            
            # Auto-validate if Google Drive
            if provider == "googledrive":
                self.validate_credentials()
    
    def show_setup_guide(self):
        """Show setup guide for selected cloud provider."""
        provider = self.cloud_provider.get()
        
        if not provider:
            messagebox.showinfo("Setup Guide", "Please select a cloud provider first.")
            return
        
        helper = CloudAuthHelper()
        
        if provider == "googledrive":
            guide = helper.get_google_drive_setup_guide()
            # Get user email if possible
            import getpass
            username = getpass.getuser()
            guide = guide.format(email=f"{username}@gmail.com (or your email)")
        elif provider == "dropbox":
            guide = helper.get_dropbox_setup_guide()
        else:
            guide = "Setup guide for this provider coming soon."
        
        # Show in a new window
        guide_window = tk.Toplevel(self.root)
        guide_window.title(f"{provider.title()} Setup Guide")
        guide_window.geometry("700x500")
        
        text_widget = scrolledtext.ScrolledText(guide_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, guide)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(guide_window, text="Open Setup Page", 
                  command=lambda: helper.open_google_cloud_console("credentials") if provider == "googledrive" else None).pack(pady=5)
        ttk.Button(guide_window, text="Close", command=guide_window.destroy).pack(pady=5)
    
    def validate_credentials(self):
        """Validate credentials file."""
        provider = self.cloud_provider.get()
        creds_path = self.cloud_credentials.get()
        
        if not provider:
            messagebox.showwarning("Validation", "Please select a cloud provider first.")
            return
        
        if not creds_path:
            messagebox.showwarning("Validation", "Please select a credentials file first.")
            return
        
        if provider == "googledrive":
            helper = CloudAuthHelper()
            result = helper.validate_google_credentials(creds_path)
            
            if result['valid']:
                info_msg = "✅ Credentials file is valid!\n\n"
                if result['info']:
                    info_msg += "File contains:\n"
                    for key, value in result['info'].items():
                        info_msg += f"  • {key}: {value}\n"
                messagebox.showinfo("Validation Success", info_msg)
            else:
                error_msg = "❌ Credentials file has issues:\n\n"
                for error in result['errors']:
                    error_msg += f"• {error}\n"
                if result['warnings']:
                    error_msg += "\nWarnings:\n"
                    for warning in result['warnings']:
                        error_msg += f"• {warning}\n"
                messagebox.showerror("Validation Failed", error_msg)
        else:
            # Basic file existence check for other providers
            if os.path.exists(creds_path):
                messagebox.showinfo("Validation", f"✅ Credentials file found: {creds_path}")
            else:
                messagebox.showerror("Validation", f"❌ File not found: {creds_path}")
    
    def open_cloud_console(self):
        """Open cloud provider console in browser."""
        provider = self.cloud_provider.get()
        
        if not provider:
            messagebox.showinfo("Open Console", "Please select a cloud provider first.")
            return
        
        helper = CloudAuthHelper()
        
        if provider == "googledrive":
            # Ask which page to open
            choice = messagebox.askyesno(
                "Open Google Cloud Console",
                "Open OAuth Consent Screen (to add test users)?\n\n"
                "Click 'Yes' for Consent Screen\n"
                "Click 'No' for Credentials page"
            )
            page = "consent" if choice else "credentials"
            helper.open_google_cloud_console(page)
            self.log(f"Opened Google Cloud Console: {page}")
        elif provider == "dropbox":
            import webbrowser
            webbrowser.open("https://www.dropbox.com/developers/apps")
            self.log("Opened Dropbox App Console")
        else:
            messagebox.showinfo("Info", "Console link for this provider coming soon.")
    
    def log(self, message):
        """Add message to log."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log output."""
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, message, color="black"):
        """Update status label."""
        self.status_label.config(text=message, foreground=color)
    
    def start_organization(self):
        """Start the organization process in a separate thread."""
        if not self.source_path.get() or not self.target_path.get():
            messagebox.showerror("Error", "Please select both source and target directories!")
            return
        
        source = Path(self.source_path.get()).resolve()
        target = Path(self.target_path.get()).resolve()
        
        if not source.exists():
            messagebox.showerror("Error", "Source directory does not exist!")
            return
        
        if source == target:
            messagebox.showerror("Error", "Source and target directories cannot be the same!")
            return
        
        # Check if source is inside target
        try:
            source.relative_to(target)
            messagebox.showerror("Error", "Source directory cannot be inside target directory!")
            return
        except ValueError:
            pass  # Good, source is not inside target
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        self.update_status("Running...", "blue")
        self.clear_log()
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.run_organization, daemon=True)
        thread.start()
    
    def stop_organization(self):
        """Stop the organization process."""
        self.is_running = False
        self.update_status("Stopped", "orange")
        self.progress.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("\n[STOPPED] Organization process stopped by user.")
    
    def run_organization(self):
        """Run the organization process."""
        try:
            source = self.source_path.get()
            target = self.target_path.get()
            strategy = self.strategy.get()
            dry_run = self.dry_run.get()
            
            self.log("=" * 60)
            self.log("AI-Based Directory Management System")
            self.log("=" * 60)
            self.log(f"Source: {source}")
            self.log(f"Target: {target}")
            self.log(f"Strategy: {strategy}")
            self.log(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
            self.log("=" * 60)
            self.log("")
            
            if not self.is_running:
                return
            
            # Step 1: File Analyzer
            self.log("Step 1: Analyzing files...")
            self.update_status("Analyzing files...", "blue")
            analyzer = FileAnalyzer()
            files_info = analyzer.scan_directory(source, recursive=True)
            self.log(f"Found {len(files_info)} files")
            self.log("")
            
            if not files_info:
                self.log("No files found to organize.")
                self.finish_organization("No files found", "orange")
                return
            
            # Apply filters if specified
            min_size = self.min_size.get().strip()
            max_size = self.max_size.get().strip()
            exclude_patterns = self.exclude_patterns.get().strip()
            
            if min_size or max_size or exclude_patterns:
                self.log("Applying filters...")
                file_filter = FileFilter()
                
                if min_size or max_size:
                    min_val = int(min_size) if min_size else None
                    max_val = int(max_size) if max_size else None
                    file_filter.add_filter(file_filter.filter_by_size(min_val, max_val))
                    self.log(f"Size filter: {min_val or 0} - {max_val or 'unlimited'} bytes")
                
                if exclude_patterns:
                    patterns = [p.strip() for p in exclude_patterns.split(',')]
                    file_filter.add_filter(file_filter.filter_by_exclude_patterns(patterns))
                    self.log(f"Exclude patterns: {', '.join(patterns)}")
                
                files_info = file_filter.apply_filters(files_info)
                self.log(f"After filtering: {len(files_info)} files")
                self.log("")
            
            # Find duplicates if requested
            if self.find_duplicates.get():
                self.log("Finding duplicate files...")
                self.update_status("Finding duplicates...", "blue")
                duplicate_detector = DuplicateDetector()
                duplicates = duplicate_detector.find_duplicates(files_info)
                summary = duplicate_detector.get_duplicate_summary(duplicates)
                
                self.log(f"Found {summary['duplicate_groups']} duplicate groups")
                self.log(f"Total duplicate files: {summary['total_duplicate_files']}")
                self.log(f"Wasted space: {summary['wasted_space_mb']} MB")
                self.log("")
            
            # Generate statistics if requested
            if self.show_stats.get():
                self.log("Generating statistics...")
                stats_gen = Statistics()
                file_stats = stats_gen.generate_file_statistics(files_info)
                self.log(stats_gen.format_statistics_report(file_stats))
                self.log("")
            
            if not self.is_running:
                return
            
            # Step 2: AI Categorizer
            self.log("Step 2: Categorizing files...")
            self.update_status("Categorizing files...", "blue")
            categorizer = AICategorizer()
            categorized = categorizer.categorize_files(files_info)
            
            self.log(f"Categorized into {len(categorized)} categories:")
            for category, files in categorized.items():
                self.log(f"  - {category}: {len(files)} files")
            self.log("")
            
            if not self.is_running:
                return
            
            # Step 3: Directory Organizer
            self.log("Step 3: Organizing files...")
            self.update_status("Organizing files...", "blue")
            
            if dry_run:
                self.log("DRY RUN MODE - Preview only (files will be copied, originals preserved)")
                self.log("")
            
            organizer = DirectoryOrganizer(target, dry_run=dry_run, subcategorize=True, preserve_structure=True)
            stats = organizer.organize_files(categorized, organization_strategy=strategy, 
                                           subcategorize=True, preserve_structure=True)
            
            # Record operation for undo (only if not dry run)
            if not dry_run:
                operations = stats.get('operations', [])
                self.undo_manager.record_operation('organize', operations)
            
            # Display summary
            self.log("")
            self.log("Organization Summary:")
            self.log("=" * 60)
            self.log(f"Total Files: {stats['total_files']}")
            self.log(f"Successfully Copied: {stats['moved']} (originals preserved)")
            self.log(f"Skipped: {stats['skipped']}")
            self.log(f"Errors: {stats['errors']}")
            self.log("=" * 60)
            
            # Verify files in target directory
            if not dry_run:
                import os
                target_file_count = 0
                for root, dirs, files in os.walk(target):
                    target_file_count += len(files)
                self.log(f"\nVerification: Found {target_file_count} files in target directory: {target}")
                if target_file_count == 0:
                    self.log("⚠️ WARNING: Target directory is empty! Files may not have been copied.")
            
            # Generate organization statistics if requested
            if self.show_stats.get():
                stats_gen = Statistics()
                org_stats = stats_gen.generate_organization_statistics(stats, categorized)
                self.log("\nOrganization Statistics:")
                self.log(f"Success Rate: {org_stats['success_rate']}%")
                self.log(f"Error Rate: {org_stats['error_rate']}%")
                self.log("")
            
            if dry_run:
                self.log("\nRun without Dry Run to execute the organization.")
                self.finish_organization("Preview completed", "blue")
            else:
                self.log("\nOrganization completed successfully!")
                self.log(f"Log file saved in: logs/")
                
                # Cloud storage upload if requested
                if self.upload_to_cloud.get() and self.cloud_provider.get():
                    self.log("\n" + "=" * 60)
                    self.log("Cloud Storage Upload")
                    self.log("=" * 60)
                    self.update_status("Uploading to cloud...", "blue")
                    
                    try:
                        remote_path = self.cloud_path.get() or "/OrganizedFiles"
                        credentials = self.cloud_credentials.get().strip() if self.cloud_credentials.get() else None
                        
                        # Validate credentials for Google Drive
                        if self.cloud_provider.get() == 'googledrive':
                            if not credentials:
                                raise ValueError(
                                    "Google Drive requires credentials file.\n"
                                    "Please select a credentials JSON file from Google Cloud Console."
                                )
                            if not os.path.exists(credentials):
                                raise FileNotFoundError(f"Credentials file not found: {credentials}")
                        
                        self.log(f"Uploading to {self.cloud_provider.get()}...")
                        if credentials:
                            self.log(f"Using credentials: {credentials}")
                        
                        # Verify target directory has files before uploading
                        import os
                        target_file_count = 0
                        for root, dirs, files in os.walk(target):
                            target_file_count += len(files)
                        
                        self.log(f"\nPre-upload verification:")
                        self.log(f"  Target directory: {target}")
                        self.log(f"  Files found: {target_file_count}")
                        
                        if target_file_count == 0:
                            raise ValueError(
                                f"No files found in target directory: {target}\n\n"
                                f"This might happen if:\n"
                                f"1. Dry run mode was used (files weren't actually copied)\n"
                                f"2. All files were skipped due to conflicts\n"
                                f"3. Organization failed silently\n\n"
                                f"Please check the organization summary above."
                            )
                        
                        # Files are already organized to target directory, so upload from there
                        upload_stats = self.cloud_manager.organize_and_upload(
                            source_dir=target,  # Upload from already-organized directory
                            cloud_provider=self.cloud_provider.get(),
                            remote_base_path=remote_path,
                            organize_first=False,  # Skip organization, files already organized
                            target_dir=None,
                            credentials_path=credentials,
                            log_callback=self.log  # Pass GUI log function
                        )
                        
                        self.log(f"\nUpload Summary:")
                        self.log(f"  Files uploaded: {upload_stats['uploaded']}")
                        self.log(f"  Files failed: {upload_stats['failed']}")
                        self.log(f"  Total files: {upload_stats['total_files']}")
                        self.log(f"\nFiles uploaded to: {remote_path}")
                        
                        # Show errors if any
                        if upload_stats.get('errors'):
                            self.log(f"\nUpload Errors (first 10):")
                            for error in upload_stats['errors'][:10]:
                                self.log(f"  - {error}")
                            if len(upload_stats['errors']) > 10:
                                self.log(f"  ... and {len(upload_stats['errors']) - 10} more errors")
                        
                        self.finish_organization("Upload completed!", "green")
                        messagebox.showinfo("Success", 
                                          f"Files organized and uploaded successfully!\n"
                                          f"Uploaded: {upload_stats['uploaded']} files")
                    except Exception as e:
                        error_msg = str(e)
                        self.log(f"\nError uploading to cloud storage: {error_msg}")
                        self.finish_organization("Upload failed", "red")
                        
                        # Provide helpful error message
                        if "API has not been used" in error_msg or "is disabled" in error_msg or "accessNotConfigured" in error_msg:
                            # Extract project ID if possible
                            import re
                            project_id = None
                            match = re.search(r'project[^\d]*(\d+)', error_msg)
                            if match:
                                project_id = match.group(1)
                            
                            api_url = "https://console.developers.google.com/apis/api/drive.googleapis.com/overview"
                            if project_id:
                                api_url += f"?project={project_id}"
                            
                            help_text = (
                                f"❌ Google Drive API Not Enabled\n\n"
                                f"The Google Drive API is not enabled in your Google Cloud project.\n\n"
                                f"QUICK FIX:\n"
                                f"1. Click this link: {api_url}\n"
                                f"2. Click the 'ENABLE' button\n"
                                f"3. Wait 2-3 minutes for changes to propagate\n"
                                f"4. Try uploading again\n\n"
                                f"See GOOGLE_DRIVE_SETUP.md for detailed instructions."
                            )
                        elif "credentials" in error_msg.lower() or "authentication" in error_msg.lower():
                            if "403" in error_msg or "access_denied" in error_msg.lower() or "verification" in error_msg.lower():
                                help_text = (
                                    f"Google Drive Access Blocked (Error 403)\n\n"
                                    f"Your email is not in the test users list.\n\n"
                                    f"QUICK FIX:\n"
                                    f"1. Go to: https://console.cloud.google.com/apis/credentials/consent\n"
                                    f"2. Scroll to 'Test users' section\n"
                                    f"3. Click 'Add Users'\n"
                                    f"4. Add your email: {os.getenv('USERNAME', 'your-email@gmail.com')}\n"
                                    f"5. Click 'Add'\n"
                                    f"6. Try again!\n\n"
                                    f"See QUICK_FIX_403_ERROR.md for detailed instructions."
                                )
                            else:
                                help_text = (
                                    f"Authentication Error:\n{error_msg}\n\n"
                                    "For Google Drive:\n"
                                    "1. Go to https://console.cloud.google.com/\n"
                                    "2. Create project and enable Google Drive API\n"
                                    "3. Create OAuth 2.0 credentials (Desktop app)\n"
                                    "4. Download JSON and select it in credentials field\n"
                                    "5. Add your email as test user in OAuth consent screen\n\n"
                                    "For Dropbox:\n"
                                    "1. Get access token from Dropbox App Console\n"
                                    "2. Save to file and select it\n\n"
                                    "For OneDrive:\n"
                                    "1. Register app in Azure Portal\n"
                                    "2. Set ONEDRIVE_CLIENT_ID environment variable"
                                )
                        else:
                            help_text = (
                                f"Error uploading to cloud:\n{error_msg}\n\n"
                                "Make sure you have:\n"
                                "1. Installed cloud libraries (pip install -r requirements.txt)\n"
                                "2. Set up authentication\n"
                                "3. Provided correct credentials file"
                            )
                        
                        messagebox.showerror("Upload Error", help_text)
                else:
                    self.finish_organization("Organization completed!", "green")
                    messagebox.showinfo("Success", "Files organized successfully!")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log(error_msg)
            self.log("")
            import traceback
            self.log(traceback.format_exc())
            self.finish_organization("Error occurred", "red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def finish_organization(self, message, color):
        """Finish the organization process."""
        self.is_running = False
        self.progress.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status(message, color)
    
    def undo_operation(self):
        """Undo the last organization operation."""
        if not self.undo_manager.can_undo():
            messagebox.showinfo("Info", "No operations to undo.")
            return
        
        result = messagebox.askyesno("Confirm Undo", 
                                    "Are you sure you want to undo the last operation?")
        if result:
            undo_result = self.undo_manager.undo()
            if undo_result:
                self.log(f"Undone {undo_result['undone']} files")
                messagebox.showinfo("Success", f"Undo completed: {undo_result['undone']} files removed")
            else:
                messagebox.showerror("Error", "Failed to undo operation.")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = DirectoryManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

