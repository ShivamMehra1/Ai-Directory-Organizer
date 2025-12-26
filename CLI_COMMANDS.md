# CLI Commands Reference
## AI-Based Directory Management System - Version 3.0

Complete guide to using the Command Line Interface (CLI) for the Directory Management System.

---

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Required Arguments](#required-arguments)
3. [Optional Arguments](#optional-arguments)
4. [Organization Strategies](#organization-strategies)
5. [File Filtering](#file-filtering)
6. [Duplicate Detection](#duplicate-detection)
7. [Statistics](#statistics)
8. [Cloud Storage Upload](#cloud-storage-upload)
9. [Configuration Files](#configuration-files)
10. [Command Examples](#command-examples)
11. [Error Handling](#error-handling)
12. [Tips & Best Practices](#tips--best-practices)

---

## Basic Usage

### Command Syntax

```bash
python src/main.py --source <source_dir> --target <target_dir> [OPTIONS]
```

### Quick Start Example

```bash
python src/main.py --source ./Downloads --target ./Organized
```

This command will:
- Scan the `Downloads` directory
- Categorize all files
- Organize them into `Organized` directory
- Preserve original folder structure

---

## Required Arguments

### `--source` (Required)

**Description:** Source directory to organize

**Usage:**
```bash
--source <directory_path>
```

**Examples:**
```bash
# Windows
--source C:\Users\Username\Downloads

# Linux/Mac
--source /home/username/Downloads

# Relative path
--source ./Downloads
```

**Notes:**
- Directory must exist
- Can be absolute or relative path
- Will scan recursively by default

---

### `--target` (Required)

**Description:** Target directory for organized files

**Usage:**
```bash
--target <directory_path>
```

**Examples:**
```bash
# Windows
--target C:\Users\Username\OrganizedFiles

# Linux/Mac
--target /home/username/OrganizedFiles

# Relative path
--target ./Organized
```

**Notes:**
- Directory will be created if it doesn't exist
- Cannot be the same as source directory
- Source directory cannot be inside target directory

---

## Optional Arguments

### `--dry-run`

**Description:** Preview changes without executing (files are copied, originals preserved)

**Usage:**
```bash
--dry-run
```

**Example:**
```bash
python src/main.py --source ./Downloads --target ./Organized --dry-run
```

**Output:**
- Shows what would be organized
- Files are copied (not moved)
- Original files remain untouched
- Useful for testing before actual organization

---

### `--recursive`

**Description:** Scan directories recursively (default: True)

**Usage:**
```bash
--recursive          # Scan subdirectories (default)
--no-recursive       # Only scan top-level directory
```

**Example:**
```bash
# Scan only top-level files
python src/main.py --source ./Downloads --target ./Organized --no-recursive
```

**Note:** By default, scanning is recursive. Use `--no-recursive` to disable.

---

### `--config`

**Description:** Path to custom categories configuration file (YAML format)

**Usage:**
```bash
--config <config_file_path>
```

**Example:**
```bash
python src/main.py --source ./Downloads --target ./Organized --config config/custom_categories.yaml
```

**Config File Format:**
```yaml
custom_category:
  extensions: ['.ext1', '.ext2']
  keywords: ['keyword1', 'keyword2']
  mime_types: ['application/custom']
```

**Default:** Uses built-in categories if not specified

---

### `--strategy`

**Description:** Organization strategy

**Options:**
- `category` - Organize by file category (default)
- `date` - Organize by creation/modification date

**Usage:**
```bash
--strategy category    # Organize by category (documents, images, etc.)
--strategy date        # Organize by date (YYYY-MM-DD folders)
```

**Example:**
```bash
# Organize by date
python src/main.py --source ./Downloads --target ./Organized --strategy date
```

**Default:** `category`

---

## File Filtering

### `--min-size`

**Description:** Minimum file size in bytes to include

**Usage:**
```bash
--min-size <size_in_bytes>
```

**Examples:**
```bash
# Only files larger than 1MB (1048576 bytes)
python src/main.py --source ./Downloads --target ./Organized --min-size 1048576

# Only files larger than 100KB (102400 bytes)
python src/main.py --source ./Downloads --target ./Organized --min-size 102400
```

**Size Conversions:**
- 1 KB = 1024 bytes
- 1 MB = 1024 KB = 1,048,576 bytes
- 1 GB = 1024 MB = 1,073,741,824 bytes

---

### `--max-size`

**Description:** Maximum file size in bytes to include

**Usage:**
```bash
--max-size <size_in_bytes>
```

**Example:**
```bash
# Only files smaller than 10MB
python src/main.py --source ./Downloads --target ./Organized --max-size 10485760
```

**Combined with `--min-size`:**
```bash
# Files between 1MB and 10MB
python src/main.py --source ./Downloads --target ./Organized --min-size 1048576 --max-size 10485760
```

---

### `--exclude-ext`

**Description:** File extensions to exclude

**Usage:**
```bash
--exclude-ext <extension1> <extension2> ...
```

**Example:**
```bash
# Exclude temporary and backup files
python src/main.py --source ./Downloads --target ./Organized --exclude-ext .tmp .bak .log

# Exclude system files
python src/main.py --source ./Downloads --target ./Organized --exclude-ext .DS_Store .Thumbs.db
```

**Notes:**
- Include the dot (`.`) before extension
- Can specify multiple extensions
- Case-insensitive matching

---

## Duplicate Detection

### `--find-duplicates`

**Description:** Find and report duplicate files

**Usage:**
```bash
--find-duplicates
```

**Example:**
```bash
python src/main.py --source ./Downloads --target ./Organized --find-duplicates
```

**Output:**
```
Finding duplicate files...
Found 5 duplicate groups
Total duplicate files: 12
Wasted space: 45.2 MB
```

**How it works:**
1. Groups files by size (only same-size files can be duplicates)
2. Calculates hash (MD5) for files with same size
3. Files with identical hash are duplicates

**Note:** Duplicate detection runs before organization, so you can see duplicates in the source directory.

---

## Statistics

### `--stats`

**Description:** Generate detailed statistics report

**Usage:**
```bash
--stats
```

**Example:**
```bash
python src/main.py --source ./Downloads --target ./Organized --stats
```

**Statistics Include:**
- Total files and directories
- Total size (bytes, KB, MB, GB)
- File type distribution
- Category distribution
- Extension statistics
- Organization success/error rates

**Example Output:**
```
Generating statistics...
Total files: 150
Total size: 2.5 GB
Categories:
  - documents: 45 files
  - images: 60 files
  - videos: 30 files
  - other: 15 files
```

---

## Cloud Storage Upload

### `--cloud-upload`

**Description:** Upload organized files to cloud storage

**Options:**
- `googledrive` - Google Drive
- `dropbox` - Dropbox
- `onedrive` - OneDrive

**Usage:**
```bash
--cloud-upload <provider>
```

**Example:**
```bash
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive
```

---

### `--cloud-path`

**Description:** Base path in cloud storage for uploads

**Usage:**
```bash
--cloud-path <remote_path>
```

**Examples:**
```bash
# Upload to /OrganizedFiles in Google Drive
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --cloud-path /OrganizedFiles

# Upload to /MyFiles/Organized in Dropbox
python src/main.py --source ./Downloads --target ./Organized --cloud-upload dropbox --cloud-path /MyFiles/Organized
```

**Default:** `/OrganizedFiles` if not specified

**Notes:**
- Path should start with `/`
- Folders will be created automatically
- Organized folder structure is preserved in cloud

---

### `--cloud-credentials`

**Description:** Path to cloud storage credentials file

**Usage:**
```bash
--cloud-credentials <credentials_file_path>
```

**Examples:**
```bash
# Google Drive (credentials.json)
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --cloud-credentials credentials.json

# Dropbox (token.txt)
python src/main.py --source ./Downloads --target ./Organized --cloud-upload dropbox --cloud-credentials token.txt
```

**Credentials File Types:**
- **Google Drive:** `credentials.json` (OAuth 2.0 client credentials)
- **Dropbox:** Text file with access token
- **OneDrive:** Uses device code flow (no file needed)

**Setup Guides:**
- See `docs/cloud/` folder for detailed setup instructions

---

### `--organize-then-upload`

**Description:** Organize files locally first, then upload (default: True)

**Usage:**
```bash
--organize-then-upload    # Organize locally, then upload (default)
--no-organize-then-upload # Upload directly from source (organize in cloud)
```

**Example:**
```bash
# Organize locally first, then upload organized structure
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --organize-then-upload

# Upload directly from source (organize in cloud)
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --no-organize-then-upload
```

**Default:** `True` (organize locally first)

**Note:** When `--organize-then-upload` is used, the organized files in `--target` directory are uploaded to cloud, preserving the organized structure.

---

## Configuration Files

### Custom Categories Configuration

Create a YAML file to define custom categories:

**File:** `config/custom_categories.yaml`

```yaml
my_documents:
  extensions: ['.mydoc', '.custom']
  keywords: ['myfile', 'custom']
  mime_types: ['application/custom']

my_images:
  extensions: ['.raw', '.cr2']
  keywords: ['photo', 'image']
  mime_types: ['image/raw']
```

**Usage:**
```bash
python src/main.py --source ./Downloads --target ./Organized --config config/custom_categories.yaml
```

---

## Command Examples

### Example 1: Basic Organization

```bash
python src/main.py --source ./Downloads --target ./Organized
```

**What it does:**
- Scans `Downloads` directory recursively
- Categorizes all files
- Organizes into `Organized` directory
- Preserves folder structure

---

### Example 2: Preview Before Organizing

```bash
python src/main.py --source ./Downloads --target ./Organized --dry-run
```

**What it does:**
- Shows what would be organized
- Copies files (originals remain)
- Safe to test before actual organization

---

### Example 3: Filter Large Files Only

```bash
python src/main.py --source ./Downloads --target ./Organized --min-size 10485760
```

**What it does:**
- Only organizes files larger than 10MB
- Skips smaller files

---

### Example 4: Exclude Temporary Files

```bash
python src/main.py --source ./Downloads --target ./Organized --exclude-ext .tmp .bak .log
```

**What it does:**
- Organizes all files except `.tmp`, `.bak`, and `.log` files

---

### Example 5: Find Duplicates

```bash
python src/main.py --source ./Downloads --target ./Organized --find-duplicates
```

**What it does:**
- Finds duplicate files in source directory
- Reports duplicate groups and wasted space
- Organizes files (including duplicates)

---

### Example 6: Generate Statistics

```bash
python src/main.py --source ./Downloads --target ./Organized --stats
```

**What it does:**
- Organizes files
- Generates detailed statistics report
- Shows file distribution, sizes, categories

---

### Example 7: Organize and Upload to Google Drive

```bash
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --cloud-credentials credentials.json --cloud-path /MyOrganizedFiles
```

**What it does:**
1. Organizes files locally into `Organized` directory
2. Uploads organized structure to Google Drive at `/MyOrganizedFiles`
3. Preserves folder hierarchy in cloud

**Prerequisites:**
- Google Drive API credentials file (`credentials.json`)
- Google Drive API enabled in Google Cloud Console
- OAuth 2.0 authentication completed

---

### Example 8: Upload to Dropbox

```bash
python src/main.py --source ./Downloads --target ./Organized --cloud-upload dropbox --cloud-credentials token.txt --cloud-path /OrganizedFiles
```

**What it does:**
- Organizes files locally
- Uploads to Dropbox at `/OrganizedFiles`

**Prerequisites:**
- Dropbox access token in `token.txt`

---

### Example 9: Complete Workflow with All Features

```bash
python src/main.py \
  --source ./Downloads \
  --target ./Organized \
  --min-size 102400 \
  --max-size 104857600 \
  --exclude-ext .tmp .bak \
  --find-duplicates \
  --stats \
  --cloud-upload googledrive \
  --cloud-credentials credentials.json \
  --cloud-path /OrganizedFiles
```

**What it does:**
1. Filters files (100KB - 100MB, excludes .tmp and .bak)
2. Finds duplicates
3. Generates statistics
4. Organizes files
5. Uploads to Google Drive

---

### Example 10: Organize by Date

```bash
python src/main.py --source ./Downloads --target ./Organized --strategy date
```

**What it does:**
- Organizes files by creation/modification date
- Creates folders like `2024-01-15/`, `2024-01-16/`, etc.

---

## Error Handling

### Common Errors and Solutions

#### Error: "Source and target directories cannot be the same!"

**Solution:**
```bash
# Use different directories
python src/main.py --source ./Downloads --target ./Organized
```

---

#### Error: "Source directory cannot be inside target directory!"

**Solution:**
```bash
# Use a different target directory outside source
python src/main.py --source ./Downloads --target ./Organized
# NOT: --target ./Downloads/Organized
```

---

#### Error: "Directory does not exist"

**Solution:**
```bash
# Check if source directory exists
# Use absolute path or correct relative path
python src/main.py --source /path/to/existing/directory --target ./Organized
```

---

#### Error: "Error uploading to cloud storage"

**Possible Causes:**
1. Cloud libraries not installed
2. Invalid credentials
3. API not enabled (Google Drive)
4. Network issues

**Solutions:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Check credentials file path
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --cloud-credentials ./credentials.json

# 3. For Google Drive: Enable API in Google Cloud Console
# See docs/cloud/ENABLE_DRIVE_API.md

# 4. Check network connection
```

---

## Tips & Best Practices

### 1. Always Use `--dry-run` First

```bash
# Test before organizing
python src/main.py --source ./Downloads --target ./Organized --dry-run
```

**Why:** See what will happen without making changes

---

### 2. Use Filters to Reduce Processing Time

```bash
# Only process large files
python src/main.py --source ./Downloads --target ./Organized --min-size 1048576
```

**Why:** Faster processing, less disk I/O

---

### 3. Exclude Unnecessary Files

```bash
# Skip temporary and system files
python src/main.py --source ./Downloads --target ./Organized --exclude-ext .tmp .bak .DS_Store .Thumbs.db
```

**Why:** Cleaner organization, faster processing

---

### 4. Generate Statistics for Analysis

```bash
# Get detailed insights
python src/main.py --source ./Downloads --target ./Organized --stats
```

**Why:** Understand your file distribution before organizing

---

### 5. Find Duplicates Before Organizing

```bash
# Identify duplicates first
python src/main.py --source ./Downloads --target ./Organized --find-duplicates
```

**Why:** Know what duplicates exist, save storage space

---

### 6. Use Custom Categories for Special Files

```bash
# Define custom categories
python src/main.py --source ./Downloads --target ./Organized --config config/custom_categories.yaml
```

**Why:** Better categorization for your specific file types

---

### 7. Organize Locally Before Cloud Upload

```bash
# Organize first, then upload (default behavior)
python src/main.py --source ./Downloads --target ./Organized --cloud-upload googledrive --organize-then-upload
```

**Why:** 
- Verify organization locally first
- Faster upload (organized structure)
- Easier to troubleshoot

---

### 8. Use Absolute Paths for Reliability

```bash
# Windows
python src/main.py --source C:\Users\Username\Downloads --target C:\Users\Username\Organized

# Linux/Mac
python src/main.py --source /home/username/Downloads --target /home/username/Organized
```

**Why:** Avoids path resolution issues

---

### 9. Combine Multiple Options

```bash
# Comprehensive organization
python src/main.py \
  --source ./Downloads \
  --target ./Organized \
  --min-size 102400 \
  --exclude-ext .tmp .bak \
  --find-duplicates \
  --stats \
  --dry-run
```

**Why:** Get complete analysis before organizing

---

### 10. Check Logs for Details

After organization, check the log files in `logs/` directory for:
- Detailed operation logs
- Error messages
- File operation history

---

## Command Reference Summary

### Quick Reference Table

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--source` | string | ✅ Yes | Source directory to organize |
| `--target` | string | ✅ Yes | Target directory for organized files |
| `--dry-run` | flag | ❌ No | Preview changes without executing |
| `--recursive` | flag | ❌ No | Scan recursively (default: True) |
| `--config` | string | ❌ No | Custom categories config file |
| `--strategy` | choice | ❌ No | Organization strategy (category/date) |
| `--min-size` | integer | ❌ No | Minimum file size in bytes |
| `--max-size` | integer | ❌ No | Maximum file size in bytes |
| `--exclude-ext` | list | ❌ No | Extensions to exclude |
| `--find-duplicates` | flag | ❌ No | Find and report duplicates |
| `--stats` | flag | ❌ No | Generate statistics report |
| `--cloud-upload` | choice | ❌ No | Cloud provider (googledrive/dropbox/onedrive) |
| `--cloud-path` | string | ❌ No | Base path in cloud storage |
| `--cloud-credentials` | string | ❌ No | Path to credentials file |
| `--organize-then-upload` | flag | ❌ No | Organize locally first (default: True) |

---

## Getting Help

### Display Help

```bash
python src/main.py --help
```

**Output:** Shows all available arguments and descriptions

---

### Version Information

Check the version in `src/__init__.py`:
```python
__version__ = "3.0.0"
```

---

## Additional Resources

- **GUI Guide:** Use `python src/gui_main.py` for graphical interface
- **Cloud Setup:** See `docs/cloud/` folder for cloud storage setup
- **Configuration:** See `config/categories.yaml` for category definitions
- **Documentation:** See `README.md` for project overview

---

**End of CLI Commands Reference**

