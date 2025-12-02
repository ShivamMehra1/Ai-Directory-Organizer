# Project Report: AI-Based Directory Management System

**Course Code:** CSE 316  
**Course Title:** Operating Systems  
**Term:** 25261  
**Max Marks:** 30

---

## 1. Project Overview

### Problem Statement
Build an AI-based directory management system that categorizes and organizes files efficiently.

### Objectives
- Automatically analyze files in directories and extract relevant metadata
- Intelligently categorize files using AI and rule-based techniques
- Organize files into structured directory hierarchies automatically
- Provide a user-friendly interface for configuration and execution
- Support multiple file types and organization strategies

### Scope
The system processes files in a source directory, analyzes their content and metadata, categorizes them using intelligent algorithms, and organizes them into appropriate folder structures. The system supports:
- Multiple file types (documents, images, videos, code, etc.)
- Custom categorization rules
- Multiple organization strategies
- Dry-run mode for preview
- Comprehensive logging

### Expected Outcomes
- A fully functional file organization system
- Automatic categorization with high accuracy
- Efficient directory management
- Detailed operation logs and reports
- Extensible architecture for future enhancements

---

## 2. Module-Wise Breakdown

### Module 1: File Analyzer
**Purpose:** Extract and analyze file metadata, content, and characteristics.

**Key Responsibilities:**
- Recursively scan directories
- Extract file metadata (size, dates, permissions)
- Detect file types using extensions and MIME types
- Analyze content of text-based files
- Generate feature vectors for categorization

**Core Functions:**
- `scan_directory()`: Recursively scan and collect file information
- `extract_metadata()`: Extract comprehensive file metadata
- `detect_mime_type()`: Identify file MIME type
- `analyze_content()`: Analyze text file content for keywords
- `get_file_type_category()`: Get general file type category

**Technologies Used:**
- Python `pathlib` for path operations
- `python-magic` for MIME type detection
- `os` module for file system operations

---

### Module 2: AI Categorizer
**Purpose:** Intelligently categorize files using rule-based and AI techniques.

**Key Responsibilities:**
- Load and apply categorization rules
- Process file features from File Analyzer
- Assign categories based on multiple criteria
- Calculate confidence scores
- Support custom category definitions

**Core Functions:**
- `categorize_file()`: Determine category for a single file
- `categorize_files()`: Process multiple files
- `_load_categories()`: Load category definitions from config
- `get_category_confidence()`: Get confidence score for a category

**Categorization Rules (Priority Order):**
1. **Extension-based** (Priority 1, Weight: 0.4)
   - Match file extension to predefined categories
   
2. **MIME Type-based** (Priority 2, Weight: 0.3)
   - Use MIME type for accurate file identification
   
3. **Content-based** (Priority 3, Weight: 0.1 per match)
   - Analyze file content for keywords
   - Detect programming code patterns
   
4. **Filename-based** (Priority 4, Weight: 0.2)
   - Extract keywords from filename

**Supported Categories:**
- Documents (PDF, DOCX, TXT, etc.)
- Images (JPG, PNG, GIF, etc.)
- Videos (MP4, AVI, MKV, etc.)
- Audio (MP3, WAV, FLAC, etc.)
- Code (PY, JS, JAVA, CPP, etc.)
- Archives (ZIP, RAR, 7Z, etc.)
- Spreadsheets (XLSX, CSV, etc.)
- Presentations (PPT, PPTX, etc.)

---

### Module 3: Directory Organizer
**Purpose:** Organize files into structured directory hierarchies.

**Key Responsibilities:**
- Create directory structures based on categories
- Move files to appropriate locations
- Handle file conflicts and duplicates
- Maintain operation logs
- Support dry-run mode

**Core Functions:**
- `create_directory_structure()`: Create folders for categories
- `organize_files()`: Move files to organized locations
- `_move_file()`: Move individual file with conflict handling
- `_handle_conflicts()`: Resolve naming conflicts
- `dry_run_preview()`: Preview changes without execution
- `get_organization_summary()`: Generate operation statistics

**Organization Strategies:**
- **Category-based**: Organize by file category
- **Date-based**: Organize by modification date (YYYY-MM)

**Conflict Resolution:**
- Automatic renaming with numeric suffix (file_1.ext, file_2.ext)
- Skip option for duplicate files
- Comprehensive error handling

---

## 3. Functionalities

### Core Functionalities

1. **Directory Scanning**
   - Recursive directory traversal
   - Configurable scan depth
   - Progress tracking for large directories
   - Skip system/hidden files option

2. **File Analysis**
   - Metadata extraction (size, dates, permissions)
   - MIME type detection
   - Content analysis for text files
   - File type identification

3. **Intelligent Categorization**
   - Multi-rule categorization system
   - Confidence scoring
   - Custom category support
   - High accuracy for common file types

4. **File Organization**
   - Automatic directory creation
   - File movement with metadata preservation
   - Conflict resolution
   - Multiple organization strategies

5. **Configuration Management**
   - YAML-based category definitions
   - Custom rule configuration
   - Flexible organization settings

6. **Logging and Reporting**
   - Detailed operation logs
   - Statistics and summaries
   - Error reporting
   - Timestamped log files

### Advanced Functionalities

7. **Dry-Run Mode**
   - Preview changes before execution
   - Validate organization plan
   - Detect potential conflicts

8. **Progress Tracking**
   - Real-time progress bars
   - File count statistics
   - Category distribution

9. **Error Handling**
   - Graceful error recovery
   - Detailed error messages
   - Operation continuation on errors

---

## 4. Technology Used

### Programming Languages
- **Python 3.8+**
  - Cross-platform compatibility
  - Rich standard library
  - Excellent file handling capabilities
  - Strong ecosystem for AI/ML

### Libraries and Tools

**Core Libraries:**
- `os`, `shutil` - File system operations
- `pathlib` - Modern path handling (Python 3.4+)
- `json`, `yaml` - Configuration management
- `logging` - Operation logging
- `datetime` - Date/time operations
- `mimetypes` - MIME type detection

**Third-Party Libraries:**
- `python-magic` / `python-magic-bin` - Advanced file type detection
- `Pillow` - Image metadata extraction (optional)
- `tqdm` - Progress bars for user feedback
- `pyyaml` - YAML configuration file parsing

**Optional AI/ML Libraries:**
- `scikit-learn` - Machine learning capabilities (for future ML-based categorization)
- `nltk` - Natural language processing (for advanced text analysis)

### Other Tools
- **GitHub** - Version control and revision tracking
- **VS Code / PyCharm** - Integrated Development Environment
- **Markdown** - Documentation format
- **Draw.io / Lucidchart** - Flow diagram creation

---

## 5. Flow Diagram

See `FLOW_DIAGRAM.md` for detailed flow diagrams including:
- System flow diagram
- Module interaction diagram
- Categorization flow
- Organization flow

### High-Level Flow Summary:

```
START
  ↓
Parse Arguments
  ↓
Module 1: File Analyzer
  ├─ Scan Directory
  ├─ Extract Metadata
  └─ Analyze Content
  ↓
Module 2: AI Categorizer
  ├─ Load Rules
  ├─ Apply Categorization
  └─ Calculate Confidence
  ↓
Module 3: Directory Organizer
  ├─ Create Structure
  ├─ Move Files
  └─ Log Operations
  ↓
Display Summary
  ↓
END
```

---

## 6. Revision Tracking on GitHub

### Repository Information
**Repository Name:** ai-directory-management-system  
**GitHub Link:** [To be added after repository creation]

### Revision History

**Commit 1: Initial Project Setup**
- Created project structure
- Added README.md and requirements.txt
- Set up .gitignore

**Commit 2: Module 1 - File Analyzer Implementation**
- Implemented directory scanning
- Added metadata extraction
- File type detection functionality

**Commit 3: Module 2 - AI Categorizer Implementation**
- Rule-based categorization system
- Category definitions
- Confidence scoring

**Commit 4: Module 3 - Directory Organizer Implementation**
- Directory structure creation
- File movement with conflict resolution
- Logging system

**Commit 5: Main Application Integration**
- Integrated all three modules
- Command-line interface
- Error handling

**Commit 6: Testing and Documentation**
- Unit tests for modules
- Flow diagrams
- Documentation updates

**Commit 7: Final Polish and Report**
- Project report
- Code cleanup
- Final documentation

*Note: Actual GitHub commits will be made during development with detailed commit messages.*

---

## 7. Conclusion and Future Scope

### Conclusion
The AI-Based Directory Management System successfully implements an intelligent file organization solution. The system effectively:
- Analyzes files using comprehensive metadata extraction
- Categorizes files with high accuracy using multi-rule approach
- Organizes files into structured hierarchies automatically
- Provides flexible configuration and logging capabilities

The modular architecture ensures maintainability and extensibility. The system handles various file types and provides robust error handling and conflict resolution.

### Future Scope

1. **Machine Learning Integration**
   - Train ML models for improved categorization accuracy
   - Learn from user corrections
   - Adaptive categorization based on usage patterns

2. **Advanced Organization Strategies**
   - Organize by project/topic using content analysis
   - Date-based sub-categorization (year/month/day)
   - Size-based organization
   - Custom user-defined rules

3. **User Interface**
   - Graphical User Interface (GUI) using Tkinter or PyQt
   - Web-based interface
   - Real-time preview of organization

4. **Performance Enhancements**
   - Parallel file processing for large directories
   - Caching of file metadata
   - Incremental organization (only new/modified files)

5. **Additional Features**
   - File deduplication
   - Archive extraction and organization
   - Cloud storage integration
   - Scheduled automatic organization
   - Undo/rollback functionality with history

6. **Security Features**
   - File integrity verification
   - Backup before organization
   - Permission checking
   - Secure file handling

7. **Analytics and Reporting**
   - Detailed statistics dashboard
   - Category distribution charts
   - Organization history
   - Performance metrics

---

## 8. References

1. Python Software Foundation. (2023). *Python 3.11 Documentation*. https://docs.python.org/3/

2. Python `pathlib` Module Documentation. https://docs.python.org/3/library/pathlib.html

3. Python `shutil` Module Documentation. https://docs.python.org/3/library/shutil.html

4. python-magic Library. https://github.com/ahupp/python-magic

5. PyYAML Documentation. https://pyyaml.org/

6. tqdm Progress Bar Library. https://github.com/tqdm/tqdm

7. Scikit-learn Documentation. https://scikit-learn.org/stable/

8. GitHub Documentation. https://docs.github.com/

9. Operating Systems Concepts (Textbook references as applicable)

10. File System Management Best Practices

---

## Appendix

### A. AI-Generated Project Elaboration/Breakdown Report

See `AI_Project_Breakdown.md` for the complete AI-generated project breakdown including:
- Detailed project overview
- Module-wise breakdown with examples
- Functionalities list
- Technology recommendations
- Execution plan
- Implementation strategy

### B. Problem Statement

**Original Problem Statement:**
"Build an AI-based directory management system that categorizes and organizes files efficiently."

**Detailed Requirements:**
- The system should automatically analyze files in a directory
- Categorize files using AI and intelligent techniques
- Organize files into appropriate folder structures
- Support multiple file types
- Provide configuration options
- Include logging and reporting capabilities

### C. Solution/Code

The complete source code is available in the `src/` directory:

- `src/file_analyzer.py` - Module 1: File Analyzer (Lines: ~200)
- `src/ai_categorizer.py` - Module 2: AI Categorizer (Lines: ~250)
- `src/directory_organizer.py` - Module 3: Directory Organizer (Lines: ~300)
- `src/main.py` - Main application entry point (Lines: ~100)

**Total Lines of Code:** ~850 lines

**Key Code Features:**
- Object-oriented design
- Comprehensive error handling
- Detailed logging
- Modular architecture
- Configurable behavior
- Dry-run support

**Usage Example:**
```bash
# Dry run (preview)
python src/main.py --source ./test_files --target ./organized --dry-run

# Actual organization
python src/main.py --source ./test_files --target ./organized

# With custom config
python src/main.py --source ./test_files --target ./organized --config config/custom.yaml

# Date-based organization
python src/main.py --source ./test_files --target ./organized --strategy date
```

---

**End of Report**

