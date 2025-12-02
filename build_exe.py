"""
Build script to create Windows executable using PyInstaller
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_exe():
    """Build the executable file."""
    
    print("=" * 60)
    print("Building Windows Executable")
    print("=" * 60)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # PyInstaller options
    # Note: Use semicolon (;) for Windows path separator in --add-data
    config_path = project_root / "config"
    src_path = project_root / "src"
    
    options = [
        str(src_path / 'gui_main.py'),  # Main script
        '--name=DirectoryManagementSystem',  # Name of executable
        '--onefile',  # Create a single executable file
        '--windowed',  # No console window (GUI only)
        f'--add-data={config_path}{os.pathsep}config',  # Include config directory
        '--paths=' + str(src_path),  # Add src to Python path
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=file_analyzer',
        '--hidden-import=ai_categorizer',
        '--hidden-import=directory_organizer',
        '--collect-all=magic',  # Include python-magic
        '--collect-all=yaml',  # Include yaml
        '--noconfirm',  # Overwrite output without asking
        '--clean',  # Clean cache before building
    ]
    
    # Change to src directory for imports
    os.chdir(project_root)
    
    print("Starting build process...")
    print("This may take several minutes...")
    print()
    
    try:
        PyInstaller.__main__.run(options)
        print()
        print("=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print(f"Executable location: {project_root / 'dist' / 'DirectoryManagementSystem.exe'}")
        print()
        print("You can now distribute the .exe file from the 'dist' folder.")
    except Exception as e:
        print(f"Error during build: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()

