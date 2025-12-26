# Step-by-Step User Guide
## AI-Based Directory Management System - CLI Edition

**Welcome!** This guide will walk you through using the Directory Management System via Command Line Interface (CLI) from start to finish.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Your First Organization](#your-first-organization)
3. [Understanding the Basics](#understanding-the-basics)
4. [Common Tasks](#common-tasks)
5. [Advanced Features](#advanced-features)
6. [Cloud Storage Setup](#cloud-storage-setup)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference](#quick-reference)

---

## Getting Started

### Step 1: Check Python Installation

First, make sure Python is installed on your computer.

**Windows:**
1. Open Command Prompt (Press `Win + R`, type `cmd`, press Enter)
2. Type: `py --version`
3. You should see something like: `Python 3.8.0` or higher

**If Python is not installed:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

### Step 2: Navigate to Project Folder

Open Command Prompt (Windows) or Terminal (Mac/Linux) and navigate to the project folder:

**Windows:**
```cmd
cd C:\Users\harry\OneDrive\Desktop\Ai-Directory-Organizer-main\version2
```

**Mac/Linux:**
```bash
cd ~/Desktop/Ai-Directory-Organizer-main/version2
```

### Step 3: Install Dependencies (First Time Only)

If this is your first time using the project, install required libraries:

**Windows:**
```cmd
py -m pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m pip install -r requirements.txt
```

**What this does:** Installs all necessary libraries for the project to work.

**Expected output:**
```
Collecting pyyaml...
Installing collected packages...
Successfully installed...
```

---

## Your First Organization

### Let's Organize Your Downloads Folder!

This is the simplest way to use the system. Follow these steps:

### Step 1: Choose Your Folders

**Source Folder:** Where your messy files are (e.g., Downloads)  
**Target Folder:** Where organized files will go (e.g., OrganizedFiles)

### Step 2: Run the Command

**Windows:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\OrganizedFiles"
```

**Mac/Linux:**
```bash
python3 src/main.py --source ~/Downloads --target ~/OrganizedFiles
```

**Replace `YourName` with your actual username!**

### Step 3: Watch It Work!

You'll see output like this:

```
============================================================
AI-Based Directory Management System
============================================================
Source: C:\Users\YourName\Downloads
Target: C:\Users\YourName\OrganizedFiles
Mode: LIVE
============================================================

Step 1: Analyzing files...
Found 150 files

Step 2: Categorizing files...
Categorizing: 100%|████████████| 150/150 [00:02<00:00, 75.00it/s]
Categorized into 5 categories:
  - documents: 45 files
  - images: 60 files
  - videos: 30 files
  - audio: 10 files
  - other: 5 files

Step 3: Organizing files...
Organization completed successfully!
```

### Step 4: Check Your Organized Files!

Open your target folder (`OrganizedFiles` in this example). You'll see:

```
OrganizedFiles/
├── documents/
│   ├── pdf/
│   │   └── report.pdf
│   └── docx/
│       └── letter.docx
├── images/
│   ├── jpg/
│   │   └── photo.jpg
│   └── png/
│       └── screenshot.png
└── videos/
    └── mp4/
        └── video.mp4
```

**🎉 Congratulations!** You've successfully organized your files!

---

## Understanding the Basics

### What Are Source and Target?

**Source (`--source`):**
- The folder with your messy, unorganized files
- **Example:** `C:\Users\YourName\Downloads`
- Files are **read** from here (not deleted!)

**Target (`--target`):**
- The folder where organized files will be placed
- **Example:** `C:\Users\YourName\OrganizedFiles`
- Files are **copied** here in organized folders
- Will be created automatically if it doesn't exist

**Important:** Your original files stay in the source folder! Files are copied, not moved.

### Using Relative Paths

Instead of typing full paths, you can use relative paths:

**If you're in the project folder:**
```cmd
py src/main.py --source ./Downloads --target ./Organized
```

**`./` means "current folder"**

### Using Quotes for Paths with Spaces

If your folder names have spaces, use quotes:

**✅ Correct:**
```cmd
py src/main.py --source "C:\Users\Your Name\My Downloads" --target "C:\Organized Files"
```

**❌ Wrong (will cause errors):**
```cmd
py src/main.py --source C:\Users\Your Name\My Downloads --target C:\Organized Files
```

---

## Common Tasks

### Task 1: Preview Before Organizing (Dry Run)

**Why?** See what will happen without actually organizing files.

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --dry-run
```

**What happens:**
- Shows you what files will be organized
- Shows where they'll be placed
- **Doesn't actually move or copy files**
- Safe to test!

**When to use:**
- First time organizing a folder
- Want to see the plan before executing
- Testing different options

---

### Task 2: Organize Only Large Files

**Why?** Skip small files and only organize important large files.

**Example: Only organize files larger than 10MB**

**Step 1: Calculate size in bytes**
- 10 MB = 10 × 1024 × 1024 = 10,485,760 bytes

**Step 2: Run command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --min-size 10485760
```

**Size Reference:**
- 1 KB = 1,024 bytes
- 1 MB = 1,048,576 bytes
- 10 MB = 10,485,760 bytes
- 100 MB = 104,857,600 bytes
- 1 GB = 1,073,741,824 bytes

**Quick Size Calculator:**
```
For 5 MB:  5 × 1048576 = 5,242,880
For 50 MB: 50 × 1048576 = 52,428,800
For 500 MB: 500 × 1048576 = 524,288,000
```

---

### Task 3: Exclude Temporary Files

**Why?** Skip `.tmp`, `.bak`, `.log` files that you don't need.

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --exclude-ext .tmp .bak .log
```

**Common files to exclude:**
- `.tmp` - Temporary files
- `.bak` - Backup files
- `.log` - Log files
- `.DS_Store` - Mac system files
- `.Thumbs.db` - Windows thumbnail cache

**Example with multiple exclusions:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --exclude-ext .tmp .bak .log .DS_Store .Thumbs.db
```

---

### Task 4: Find Duplicate Files

**Why?** Identify duplicate files taking up space.

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --find-duplicates
```

**Output example:**
```
Finding duplicate files...
Found 5 duplicate groups
Total duplicate files: 12
Wasted space: 45.2 MB
```

**What this means:**
- **5 duplicate groups:** 5 sets of identical files
- **12 duplicate files:** Total files that are duplicates
- **45.2 MB wasted:** Space you could free up by deleting duplicates

**After finding duplicates:**
- Review the duplicate files
- Manually delete the ones you don't need
- Then organize the remaining files

---

### Task 5: Get Statistics Report

**Why?** Understand your files before organizing.

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --stats
```

**Output example:**
```
Generating statistics...
Total files: 150
Total size: 2.5 GB
Categories:
  - documents: 45 files (1.2 GB)
  - images: 60 files (800 MB)
  - videos: 30 files (500 MB)
  - audio: 10 files (50 MB)
  - other: 5 files (10 MB)
```

**Use statistics to:**
- See what types of files you have
- Plan your organization strategy
- Identify large files taking up space

---

### Task 6: Combine Multiple Options

**Why?** Use multiple features at once for better organization.

**Example: Organize large files, exclude temp files, find duplicates, and get stats**

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --min-size 1048576 --exclude-ext .tmp .bak --find-duplicates --stats
```

**What this does:**
1. ✅ Only processes files larger than 1MB
2. ✅ Skips `.tmp` and `.bak` files
3. ✅ Finds duplicate files
4. ✅ Generates statistics report
5. ✅ Organizes remaining files

---

## Advanced Features

### Feature 1: Organize by Date Instead of Category

**Default:** Files organized by category (documents, images, etc.)

**Alternative:** Organize by creation date

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --strategy date
```

**Result:**
```
Organized/
├── 2024-01-15/
│   └── file1.pdf
├── 2024-01-16/
│   └── photo.jpg
└── 2024-01-17/
    └── video.mp4
```

**When to use:**
- Want to see files by when they were created
- Organizing photos by date
- Archiving files by date

---

### Feature 2: Use Custom Categories

**Why?** Define your own file categories.

**Step 1: Create a YAML configuration file**

Create a file named `my_categories.yaml`:

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

**Step 2: Use the config file**

```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --config my_categories.yaml
```

**When to use:**
- Have special file types not in default categories
- Want custom organization rules
- Need specific categorization for your work

---

### Feature 3: Filter Files by Size Range

**Example: Only organize files between 1MB and 100MB**

**Command:**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --min-size 1048576 --max-size 104857600
```

**What this does:**
- ✅ Includes files larger than 1MB
- ✅ Includes files smaller than 100MB
- ❌ Skips files smaller than 1MB
- ❌ Skips files larger than 100MB

**Use cases:**
- Skip very small files (thumbnails, icons)
- Skip very large files (videos, archives) for separate handling

---

## Cloud Storage Setup

### Upload to Google Drive

**Step 1: Get Google Drive Credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Drive API
4. Create OAuth 2.0 credentials
5. Download as `credentials.json`
6. Place `credentials.json` in your project folder

**Step 2: First-Time Authentication**

When you run the upload command for the first time:
1. Browser will open automatically
2. Sign in to your Google account
3. Grant permissions
4. Token will be saved for future use

**Step 3: Upload Command**

```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --cloud-upload googledrive --cloud-credentials credentials.json --cloud-path /MyOrganizedFiles
```

**What happens:**
1. Organizes files locally first
2. Uploads organized structure to Google Drive
3. Creates folder structure: `/MyOrganizedFiles/documents/pdf/...`

**Troubleshooting:**
- **403 Error:** Add your email as a test user in Google Cloud Console
- **API Not Enabled:** Enable Google Drive API in Google Cloud Console
- See `docs/cloud/` folder for detailed guides

---

### Upload to Dropbox

**Step 1: Get Dropbox Access Token**

1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create a new app
3. Generate access token
4. Save token to a file (e.g., `dropbox_token.txt`)

**Step 2: Upload Command**

```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --cloud-upload dropbox --cloud-credentials dropbox_token.txt --cloud-path /OrganizedFiles
```

---

### Upload to OneDrive

**Step 1: Register App (One-Time)**

1. Go to [Azure Portal](https://portal.azure.com/)
2. Register a new application
3. Configure Microsoft Graph API permissions

**Step 2: Upload Command**

```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --cloud-upload onedrive --cloud-path /OrganizedFiles
```

**Note:** OneDrive uses device code flow - you'll get a code to enter in browser.

---

## Troubleshooting

### Problem 1: "Source and target directories cannot be the same!"

**Error Message:**
```
Error: Source and target directories cannot be the same!
```

**Solution:**
Use different folders for source and target.

**❌ Wrong:**
```cmd
py src/main.py --source "C:\Downloads" --target "C:\Downloads"
```

**✅ Correct:**
```cmd
py src/main.py --source "C:\Downloads" --target "C:\Organized"
```

---

### Problem 2: "Directory does not exist"

**Error Message:**
```
Error: Directory does not exist: C:\Users\YourName\Downloads
```

**Solution:**
1. Check if the folder path is correct
2. Use quotes if path has spaces
3. Use forward slashes or double backslashes on Windows

**Windows Path Examples:**
```cmd
# Use quotes
--source "C:\Users\Your Name\Downloads"

# Or use forward slashes
--source C:/Users/YourName/Downloads
```

---

### Problem 3: "py is not recognized"

**Error Message:**
```
'py' is not recognized as an internal or external command
```

**Solution 1: Use full Python path**
```cmd
C:\Python39\python.exe src/main.py --source "C:\Downloads" --target "C:\Organized"
```

**Solution 2: Use python instead**
```cmd
python src/main.py --source "C:\Downloads" --target "C:\Organized"
```

**Solution 3: Add Python to PATH**
1. Find Python installation (usually `C:\Python39\` or `C:\Users\YourName\AppData\Local\Programs\Python\`)
2. Add to System PATH environment variable

---

### Problem 4: "No module named 'yaml'"

**Error Message:**
```
ModuleNotFoundError: No module named 'yaml'
```

**Solution:**
Install dependencies:
```cmd
py -m pip install -r requirements.txt
```

---

### Problem 5: Cloud Upload Fails

**Error Message:**
```
Error uploading to cloud storage: ...
```

**Common Causes & Solutions:**

1. **Libraries not installed:**
   ```cmd
   py -m pip install google-api-python-client google-auth-oauthlib dropbox msal requests
   ```

2. **Invalid credentials:**
   - Check credentials file path
   - Verify credentials file is correct format
   - Re-download credentials if needed

3. **API not enabled (Google Drive):**
   - Go to Google Cloud Console
   - Enable Google Drive API
   - See `docs/cloud/ENABLE_DRIVE_API.md`

4. **403 Error (Google Drive):**
   - Add your email as test user in Google Cloud Console
   - See `docs/cloud/QUICK_FIX_403_ERROR.md`

---

### Problem 6: Command Too Long

**If your command is very long, break it into multiple lines:**

**Windows (use `^`):**
```cmd
py src/main.py ^
  --source "C:\Users\YourName\Downloads" ^
  --target "C:\Users\YourName\Organized" ^
  --min-size 1048576 ^
  --exclude-ext .tmp .bak ^
  --find-duplicates
```

**Mac/Linux (use `\`):**
```bash
python3 src/main.py \
  --source ~/Downloads \
  --target ~/Organized \
  --min-size 1048576 \
  --exclude-ext .tmp .bak \
  --find-duplicates
```

---

## Quick Reference

### Essential Commands

**Basic Organization:**
```cmd
py src/main.py --source "SOURCE_FOLDER" --target "TARGET_FOLDER"
```

**Preview First (Recommended):**
```cmd
py src/main.py --source "SOURCE_FOLDER" --target "TARGET_FOLDER" --dry-run
```

**With Statistics:**
```cmd
py src/main.py --source "SOURCE_FOLDER" --target "TARGET_FOLDER" --stats
```

**Find Duplicates:**
```cmd
py src/main.py --source "SOURCE_FOLDER" --target "TARGET_FOLDER" --find-duplicates
```

**Filter Large Files:**
```cmd
py src/main.py --source "SOURCE_FOLDER" --target "TARGET_FOLDER" --min-size 1048576
```

**Exclude Files:**
```cmd
py src/main.py --source "SOURCE_FOLDER" --target "TARGET_FOLDER" --exclude-ext .tmp .bak
```

### Size Reference

| Size | Bytes | Use Case |
|------|-------|----------|
| 100 KB | 102,400 | Small files |
| 1 MB | 1,048,576 | Medium files |
| 10 MB | 10,485,760 | Large files |
| 100 MB | 104,857,600 | Very large files |
| 1 GB | 1,073,741,824 | Huge files |

### Common File Extensions to Exclude

- `.tmp` - Temporary files
- `.bak` - Backup files
- `.log` - Log files
- `.DS_Store` - Mac system files
- `.Thumbs.db` - Windows thumbnails
- `.lnk` - Windows shortcuts

### Getting Help

**Display all options:**
```cmd
py src/main.py --help
```

**Check version:**
See `src/__init__.py` file

---

## Step-by-Step Workflow Examples

### Example 1: First-Time User Workflow

**Goal:** Organize Downloads folder safely

**Step 1: Preview**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --dry-run
```
Review the output to see what will happen.

**Step 2: Get Statistics**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --stats --dry-run
```
Understand your files.

**Step 3: Find Duplicates**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --find-duplicates --dry-run
```
Identify duplicates.

**Step 4: Organize (Remove --dry-run)**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized"
```
Actually organize the files.

---

### Example 2: Regular Maintenance Workflow

**Goal:** Organize new files in Downloads monthly

**Step 1: Organize with filters**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --exclude-ext .tmp .bak .log --min-size 102400
```

**What this does:**
- Skips temporary files
- Only organizes files larger than 100KB
- Fast and efficient

---

### Example 3: Complete Organization with Cloud Backup

**Goal:** Organize files and backup to cloud

**Step 1: Organize locally**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --stats --find-duplicates
```

**Step 2: Upload to cloud**
```cmd
py src/main.py --source "C:\Users\YourName\Downloads" --target "C:\Users\YourName\Organized" --cloud-upload googledrive --cloud-credentials credentials.json --cloud-path /Backup
```

---

## Tips for Success

### ✅ Do's

1. **Always use `--dry-run` first** - See what will happen
2. **Use quotes for paths with spaces** - Prevents errors
3. **Check statistics before organizing** - Understand your files
4. **Find duplicates first** - Save space
5. **Exclude unnecessary files** - Faster processing
6. **Start with small folders** - Test before large folders
7. **Keep backups** - Files are copied, but backups are good practice

### ❌ Don'ts

1. **Don't use same folder for source and target** - Will cause error
2. **Don't skip `--dry-run` on important folders** - Always preview first
3. **Don't forget quotes on paths with spaces** - Will cause errors
4. **Don't organize system folders** - Can cause issues
5. **Don't interrupt during organization** - Let it complete

---

## Next Steps

After mastering the basics:

1. **Read Technical Reference:** See `CLI_COMMANDS.md` for all options
2. **Try GUI Version:** Run `py src/gui_main.py` for graphical interface
3. **Set Up Cloud Storage:** Follow guides in `docs/cloud/` folder
4. **Customize Categories:** Create your own category definitions
5. **Automate:** Create batch scripts for regular organization

---

## Need More Help?

- **Technical Reference:** `CLI_COMMANDS.md` - Complete command reference
- **Cloud Setup:** `docs/cloud/` - Cloud storage guides
- **Project README:** `README.md` - Project overview
- **Viva Documentation:** `viva/` - Technical documentation

---

**Happy Organizing! 🎉**

---

**End of User Guide**

