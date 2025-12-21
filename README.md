# AI-Based Directory Management System - Version 2.0

An intelligent file organization system that automatically categorizes and organizes files efficiently using AI and rule-based techniques.

## 🆕 Version 2.0 - What's New

### Bug Fixes
- ✅ Fixed magic library import error handling for Windows compatibility
- ✅ Fixed import path issues in main.py
- ✅ Added path validation to prevent source=target directory errors
- ✅ Improved error handling throughout the application

### New Features
- 🔍 **Duplicate File Detection**: Find and report duplicate files with wasted space calculation
- 🎯 **Advanced File Filtering**: Filter by size, extension, date, name patterns, and exclude patterns
- ↩️ **Undo Functionality**: Undo last organization operation
- 📊 **Statistics Dashboard**: Comprehensive statistics and analytics
- ⚙️ **Configuration Export/Import**: Save and load custom configurations
- 🎨 **Enhanced GUI**: Improved interface with filtering options and better progress tracking

## 🎯 Project Overview

This system automatically analyzes files in a directory, categorizes them using AI and rule-based methods, and organizes them into a structured folder hierarchy while **preserving original folder structure** and **keeping original files intact**.

## ✨ Key Features

- **📁 Folder Structure Preservation**: Maintains original folder structure from source
- **📋 Automatic File Analysis**: Scans directories and extracts file metadata
- **🤖 AI-Powered Categorization**: Intelligently categorizes files based on content, type, and metadata
- **🗂️ Smart Organization**: Organizes files into category → file type subdirectories
- **💾 Original Files Preserved**: Copies files instead of moving (originals remain untouched)
- **🎨 GUI Interface**: User-friendly graphical interface (Windows .exe available)
- **⚙️ Configurable Rules**: Custom categorization and organization rules
- **👀 Dry-Run Mode**: Preview changes before applying them
- **📊 Comprehensive Logging**: Track all operations with detailed logs
- **🔍 Duplicate Detection**: Find duplicate files and calculate wasted space
- **🎯 Advanced Filtering**: Filter files by size, extension, date, patterns
- **↩️ Undo Support**: Undo last organization operation
- **📈 Statistics & Analytics**: Detailed statistics and reports
- **💾 Config Export/Import**: Save and load custom configurations

## 📂 Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── file_analyzer.py      # Module 1: File Analysis
│   ├── ai_categorizer.py     # Module 2: AI Categorization
│   ├── directory_organizer.py # Module 3: Directory Organization
│   ├── duplicate_detector.py # Module 4: Duplicate Detection (NEW)
│   ├── file_filter.py        # Module 5: File Filtering (NEW)
│   ├── undo_manager.py       # Module 6: Undo Manager (NEW)
│   ├── statistics.py         # Module 7: Statistics (NEW)
│   ├── config_manager.py     # Module 8: Config Manager (NEW)
│   ├── main.py               # CLI application entry point
│   └── gui_main.py          # GUI application entry point
├── config/
│   └── categories.yaml       # Category definitions
├── tests/                    # Unit tests
├── requirements.txt          # Python dependencies
├── build_exe.py             # Script to build Windows .exe
├── create_installer.bat     # Automated build script
├── README.md                # This file
├── PROJECT_REPORT.md        # Complete project report
└── .gitignore
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows 7/8/10/11 (for .exe version)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python src/main.py --help
```

## 💻 Usage

### Command Line Interface

**Basic Usage:**
```bash
python src/main.py --source <source_directory> --target <target_directory>
```

**With Dry-Run (Preview):**
```bash
python src/main.py --source ./test_files --target ./organized --dry-run
```

**With Date-Based Organization:**
```bash
python src/main.py --source ./test_files --target ./organized --strategy date
```

**Options:**
- `--source`: Source directory containing files to organize (required)
- `--target`: Target directory for organized files (required)
- `--dry-run`: Preview changes without executing (recommended first)
- `--strategy`: Organization strategy (`category` or `date`)
- `--config`: Path to custom categories configuration file
- `--recursive`: Scan subdirectories recursively (default: True)
- `--min-size`: Minimum file size in bytes to include
- `--max-size`: Maximum file size in bytes to include
- `--exclude-ext`: File extensions to exclude (e.g., `.tmp .bak`)
- `--find-duplicates`: Find and report duplicate files
- `--stats`: Generate detailed statistics report

### Graphical User Interface (GUI)

**Run GUI directly:**
```bash
python src/gui_main.py
```

**Or build Windows .exe:**
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Or use automated script
create_installer.bat
```

The executable will be in `dist/DirectoryManagementSystem.exe`

## 📁 How Organization Works

### Folder Structure Preservation

The system preserves your original folder structure and organizes files within each folder:

**Source:**
```
source/
├── folder1/
│   ├── image.jpg
│   ├── script.py
│   └── document.pdf
└── folder2/
    ├── photo.png
    └── app.js
```

**Organized Output:**
```
organized_output/
├── folder1/
│   ├── images/
│   │   └── jpg/
│   │       └── image.jpg
│   ├── code/
│   │   └── python/
│   │       └── script.py
│   └── documents/
│       └── pdf/
│           └── document.pdf
└── folder2/
    ├── images/
    │   └── png/
    │       └── photo.png
    └── code/
        └── javascript/
            └── app.js
```

### File Categories

Files are organized into these categories:
- **Documents**: PDF, DOCX, TXT, RTF, etc.
- **Images**: JPG, PNG, GIF, SVG, etc.
- **Videos**: MP4, AVI, MKV, etc.
- **Audio**: MP3, WAV, FLAC, etc.
- **Code**: Python, JavaScript, Java, C++, etc.
- **Archives**: ZIP, RAR, 7Z, etc.
- **Spreadsheets**: XLSX, CSV, etc.
- **Presentations**: PPTX, PPT, etc.

### Important Notes

- ✅ **Original files are preserved** - Files are copied, not moved
- ✅ **Folder structure maintained** - Original folders preserved
- ✅ **Subcategorization** - Files organized by type within categories
- ✅ **Safe operation** - Use dry-run first to preview

## 🧪 Testing

Run unit tests:
```bash
python -m unittest discover tests
```

Or test individual modules:
```bash
python -m unittest tests.test_file_analyzer
python -m unittest tests.test_ai_categorizer
```

## 📦 Building Windows Executable

### Quick Build
```bash
create_installer.bat
```

### Manual Build
```bash
pip install pyinstaller
python build_exe.py
```

The executable will be created in `dist/DirectoryManagementSystem.exe`

**Note:** The .exe file is standalone (50-150 MB) and includes all dependencies. No Python installation needed on target computers.

## 📊 Modules

### Module 1: File Analyzer
- Recursively scans directories
- Extracts file metadata (size, dates, permissions)
- Detects file types using extensions and MIME types
- Analyzes content of text-based files
- Tracks relative paths for folder structure preservation
- **V2**: Improved Windows compatibility for MIME type detection

### Module 2: AI Categorizer
- Rule-based categorization system
- Multi-priority rule application (extension, MIME type, content, filename)
- Confidence scoring
- Custom category support via YAML configuration
- Supports 8+ file categories

### Module 3: Directory Organizer
- Preserves original folder structure
- Creates category and subcategory directories
- Copies files (preserves originals)
- Handles file conflicts with auto-renaming
- Comprehensive logging
- Dry-run mode support

### Module 4: Duplicate Detector (NEW in V2)
- Detects duplicate files using hash comparison
- Groups files by size for faster detection
- Calculates wasted space from duplicates
- Supports MD5, SHA1, SHA256 hashing algorithms

### Module 5: File Filter (NEW in V2)
- Filter by file size (min/max)
- Filter by file extension (include/exclude)
- Filter by date range (created/modified)
- Filter by filename patterns (regex)
- Filter by category
- Chain multiple filters together

### Module 6: Undo Manager (NEW in V2)
- Records all organization operations
- Undo last operation
- Redo support
- Persistent history storage

### Module 7: Statistics (NEW in V2)
- Comprehensive file statistics
- Category distribution analysis
- Extension statistics
- Date range analysis
- Organization success/error rates
- Formatted reports

### Module 8: Configuration Manager (NEW in V2)
- Export configuration to JSON/YAML
- Import configuration from files
- Default configuration templates

## 🔧 Configuration

Customize categories in `config/categories.yaml`:

```yaml
custom_category:
  extensions: ['.ext1', '.ext2']
  keywords: ['keyword1', 'keyword2']
  mime_types: ['mime/type1']
```

## 📝 Logging

All operations are logged in the `logs/` directory with timestamps. Logs include:
- Files processed
- Categories assigned
- Copy operations
- Errors and warnings
- Statistics

## 🛠️ Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**"PyInstaller not found" (for building .exe):**
```bash
pip install pyinstaller
```

**GUI doesn't open:**
- Test tkinter: `python -c "import tkinter; tkinter._test()"`
- Make sure Python is installed with tkinter support

**Build takes too long:**
- Normal! First build takes 5-10 minutes
- Subsequent builds are faster (2-5 minutes)

## 📄 Project Report

See `PROJECT_REPORT.md` for complete project documentation including:
- Detailed module breakdown
- Technology stack
- Flow diagrams
- Implementation details
- Future scope

## 📚 License

Educational Project - CSE 316 Operating Systems

## 👥 Credits

**Course:** CSE 316 - Operating Systems  
**Term:** 25261  
**Institution:** Lovely Professional University

---

## 🎯 Quick Start Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test with dry-run
python src/main.py --source ./test_files --target ./organized --dry-run

# 3. Organize files
python src/main.py --source ./test_files --target ./organized

# 4. Check organized output
# Files are copied to organized/ while originals remain in test_files/
```

**Happy Organizing! 🎉**
