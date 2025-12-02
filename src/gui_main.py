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


class DirectoryManagementGUI:
    """GUI Application for Directory Management System."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Directory Management System")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()
        self.strategy = tk.StringVar(value="category")
        self.dry_run = tk.BooleanVar(value=True)
        self.is_running = False
        
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
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Organization strategy
        ttk.Label(options_frame, text="Organization Strategy:").grid(row=0, column=0, sticky=tk.W, pady=5)
        strategy_combo = ttk.Combobox(options_frame, textvariable=self.strategy, 
                                      values=["category", "date"], state="readonly", width=20)
        strategy_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Dry run checkbox
        ttk.Checkbutton(options_frame, text="Dry Run (Preview Only)", 
                       variable=self.dry_run).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Organization", 
                                       command=self.start_organization, width=20)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                      command=self.stop_organization, state=tk.DISABLED, width=20)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log, width=20).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
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
        
        if not os.path.exists(self.source_path.get()):
            messagebox.showerror("Error", "Source directory does not exist!")
            return
        
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
            
            # Display summary
            self.log("")
            self.log("Organization Summary:")
            self.log("=" * 60)
            self.log(f"Total Files: {stats['total_files']}")
            self.log(f"Successfully Copied: {stats['moved']} (originals preserved)")
            self.log(f"Skipped: {stats['skipped']}")
            self.log(f"Errors: {stats['errors']}")
            self.log("=" * 60)
            
            if dry_run:
                self.log("\nRun without Dry Run to execute the organization.")
                self.finish_organization("Preview completed", "blue")
            else:
                self.log("\nOrganization completed successfully!")
                self.log(f"Log file saved in: logs/")
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


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = DirectoryManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

