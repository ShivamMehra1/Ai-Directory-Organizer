# Linux Usage Guide - AI Directory Organizer v2.0

Complete guide for using the AI Directory Organizer on Linux systems.

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Command Reference](#command-reference)
4. [Advanced Features](#advanced-features)
5. [GUI Usage](#gui-usage)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### Prerequisites

```bash
# Check Python version (requires 3.8+)
python3 --version

# Install pip if not available
sudo apt-get update
sudo apt-get install python3-pip  # Debian/Ubuntu
# OR
sudo yum install python3-pip      # CentOS/RHEL
# OR
sudo dnf install python3-pip      # Fedora
```

### Install Dependencies

```bash
# Navigate to project directory
cd /path/to/Ai-Directory-Organizer-main/version2

# Install Python dependencies
pip3 install -r requirements.txt

# For systems without python-magic, install system libraries
sudo apt-get install libmagic1 python3-magic  # Debian/Ubuntu
# OR
sudo yum install file-devel python3-magic      # CentOS/RHEL
```

### Verify Installation

```bash
# Test the installation
python3 src/main.py --help

# Test GUI (if X11 is available)
python3 src/gui_main.py
```

---

## 💻 Basic Usage

### Quick Start

```bash
# Basic organization (dry-run first to preview)
python3 src/main.py --source /home/user/documents --target /home/user/organized --dry-run

# Execute organization
python3 src/main.py --source /home/user/documents --target /home/user/organized
```

### Make Scripts Executable (Optional)

```bash
# Make main script executable
chmod +x src/main.py
chmod +x src/gui_main.py

# Create aliases (add to ~/.bashrc or ~/.zshrc)
alias organize='python3 /path/to/version2/src/main.py'
alias organize-gui='python3 /path/to/version2/src/gui_main.py'
```

---

## 📖 Command Reference

### Basic Commands

#### 1. Basic Organization

```bash
# Organize files by category (default)
python3 src/main.py --source /path/to/source --target /path/to/target

# Organize files by date
python3 src/main.py --source /path/to/source --target /path/to/target --strategy date
```

#### 2. Dry Run (Preview)

```bash
# Preview changes without executing
python3 src/main.py --source /path/to/source --target /path/to/target --dry-run
```

#### 3. Non-Recursive Scan

```bash
# Scan only top-level directory (not subdirectories)
python3 src/main.py --source /path/to/source --target /path/to/target --no-recursive
```

#### 4. Custom Configuration

```bash
# Use custom categories configuration
python3 src/main.py --source /path/to/source --target /path/to/target --config /path/to/custom_categories.yaml
```

---

## 🎯 Advanced Features

### File Filtering

#### Filter by File Size

```bash
# Include only files larger than 1MB (1048576 bytes)
python3 src/main.py --source /path/to/source --target /path/to/target --min-size 1048576

# Include only files smaller than 100MB (104857600 bytes)
python3 src/main.py --source /path/to/source --target /path/to/target --max-size 104857600

# Combine min and max size
python3 src/main.py --source /path/to/source --target /path/to/target --min-size 1024 --max-size 10485760
```

#### Exclude File Extensions

```bash
# Exclude temporary files
python3 src/main.py --source /path/to/source --target /path/to/target --exclude-ext .tmp .bak .swp

# Exclude system files
python3 src/main.py --source /path/to/source --target /path/to/target --exclude-ext .DS_Store Thumbs.db .git
```

### Duplicate Detection

```bash
# Find and report duplicate files
python3 src/main.py --source /path/to/source --target /path/to/target --find-duplicates

# Combine with dry-run to just analyze
python3 src/main.py --source /path/to/source --target /path/to/target --dry-run --find-duplicates
```

### Statistics Generation

```bash
# Generate detailed statistics report
python3 src/main.py --source /path/to/source --target /path/to/target --stats

# Combine with dry-run for analysis only
python3 src/main.py --source /path/to/source --target /path/to/target --dry-run --stats
```

### Combining Multiple Options

```bash
# Full-featured command with all options
python3 src/main.py \
  --source /home/user/documents \
  --target /home/user/organized \
  --strategy category \
  --min-size 1024 \
  --max-size 104857600 \
  --exclude-ext .tmp .bak .log \
  --find-duplicates \
  --stats \
  --dry-run
```

---

## 🖥️ GUI Usage

### Launch GUI

```bash
# Basic GUI launch
python3 src/gui_main.py

# With X11 forwarding (for remote servers)
DISPLAY=:0 python3 src/gui_main.py

# Using Xvfb for headless systems (if needed)
xvfb-run python3 src/gui_main.py
```

### GUI Features

The GUI provides the same features as CLI with a graphical interface:
- Source/Target directory selection
- Organization strategy selection
- File filtering options
- Duplicate detection checkbox
- Statistics checkbox
- Undo functionality
- Real-time log output

---

## 📝 Examples

### Example 1: Organize Downloads Folder

```bash
# Organize downloads by category
python3 src/main.py \
  --source ~/Downloads \
  --target ~/Downloads_Organized \
  --exclude-ext .tmp .crdownload \
  --stats
```

### Example 2: Clean Up Large Files

```bash
# Find and organize files larger than 50MB
python3 src/main.py \
  --source /home/user/storage \
  --target /home/user/storage_organized \
  --min-size 52428800 \
  --strategy date \
  --find-duplicates
```

### Example 3: Organize Photos by Date

```bash
# Organize photos by modification date
python3 src/main.py \
  --source ~/Pictures \
  --target ~/Pictures_Organized \
  --strategy date \
  --exclude-ext .tmp .bak \
  --stats
```

### Example 4: Preview Before Organizing

```bash
# Always preview first!
python3 src/main.py \
  --source /path/to/source \
  --target /path/to/target \
  --dry-run \
  --find-duplicates \
  --stats

# If satisfied, run without --dry-run
python3 src/main.py \
  --source /path/to/source \
  --target /path/to/target \
  --find-duplicates \
  --stats
```

### Example 5: Organize Code Projects

```bash
# Organize code files, excluding build artifacts
python3 src/main.py \
  --source ~/projects \
  --target ~/projects_organized \
  --exclude-ext .pyc .pyo __pycache__ .o .so .a \
  --stats
```

### Example 6: Find Duplicates Only (No Organization)

```bash
# Just find duplicates without organizing
python3 src/main.py \
  --source /path/to/source \
  --target /tmp/dummy \
  --dry-run \
  --find-duplicates
```

---

## 🔧 Advanced Usage

### Using with Cron (Scheduled Tasks)

```bash
# Edit crontab
crontab -e

# Add line to organize downloads daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/version2/src/main.py --source /home/user/Downloads --target /home/user/Downloads_Organized >> /var/log/organizer.log 2>&1
```

### Using in Scripts

```bash
#!/bin/bash
# organize_files.sh

SOURCE_DIR="$1"
TARGET_DIR="$2"

if [ -z "$SOURCE_DIR" ] || [ -z "$TARGET_DIR" ]; then
    echo "Usage: $0 <source_dir> <target_dir>"
    exit 1
fi

# Preview first
python3 /path/to/version2/src/main.py \
  --source "$SOURCE_DIR" \
  --target "$TARGET_DIR" \
  --dry-run \
  --stats

read -p "Proceed with organization? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 /path/to/version2/src/main.py \
      --source "$SOURCE_DIR" \
      --target "$TARGET_DIR" \
      --stats
fi
```

### Using with Systemd (Service)

Create `/etc/systemd/system/file-organizer.service`:

```ini
[Unit]
Description=File Organizer Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/version2/src/main.py --source /home/user/Downloads --target /home/user/Downloads_Organized
User=yourusername
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and run:
```bash
sudo systemctl enable file-organizer.service
sudo systemctl start file-organizer.service
```

---

## 📊 Command Options Summary

| Option | Description | Example |
|--------|-------------|---------|
| `--source` | Source directory (required) | `--source /home/user/files` |
| `--target` | Target directory (required) | `--target /home/user/organized` |
| `--dry-run` | Preview without executing | `--dry-run` |
| `--strategy` | Organization strategy | `--strategy category` or `--strategy date` |
| `--recursive` | Scan recursively (default: True) | `--recursive` |
| `--no-recursive` | Don't scan subdirectories | `--no-recursive` |
| `--config` | Custom config file | `--config /path/to/config.yaml` |
| `--min-size` | Minimum file size (bytes) | `--min-size 1024` |
| `--max-size` | Maximum file size (bytes) | `--max-size 10485760` |
| `--exclude-ext` | Exclude extensions | `--exclude-ext .tmp .bak` |
| `--find-duplicates` | Find duplicate files | `--find-duplicates` |
| `--stats` | Generate statistics | `--stats` |
| `--help` | Show help message | `--help` |

---

## 🐧 Linux-Specific Tips

### Permissions

```bash
# If you get permission errors, check file permissions
ls -la /path/to/source
ls -la /path/to/target

# Fix permissions if needed
chmod -R 755 /path/to/source
chmod -R 755 /path/to/target
```

### Symbolic Links

```bash
# The organizer follows symbolic links by default
# To exclude them, you may need to filter them manually
```

### Large Directories

```bash
# For very large directories, use nohup to run in background
nohup python3 src/main.py --source /large/dir --target /organized --stats > organizer.log 2>&1 &

# Check progress
tail -f organizer.log
```

### Disk Space

```bash
# Check available disk space before organizing
df -h /path/to/target

# Monitor disk usage during organization
watch -n 1 df -h /path/to/target
```

---

## 🔍 Troubleshooting

### Issue: "python-magic not found"

```bash
# Install system library
sudo apt-get install libmagic1 python3-magic  # Debian/Ubuntu
sudo yum install file-devel python3-magic      # CentOS/RHEL

# The application will fallback to mimetypes if magic is unavailable
```

### Issue: "Permission denied"

```bash
# Check and fix permissions
sudo chown -R $USER:$USER /path/to/directory
chmod -R 755 /path/to/directory
```

### Issue: "Module not found"

```bash
# Reinstall dependencies
pip3 install -r requirements.txt --user

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: GUI doesn't open

```bash
# Check if X11 is available
echo $DISPLAY

# For remote servers, use X11 forwarding
ssh -X user@server
python3 src/gui_main.py

# Or use VNC/Xvfb
```

### Issue: Slow performance

```bash
# Use filtering to reduce files processed
python3 src/main.py --source /path --target /path --min-size 1024

# Process in smaller batches
# Organize subdirectories separately
```

---

## 📚 Additional Resources

### Log Files

```bash
# View organization logs
ls -la logs/
tail -f logs/organization_*.log

# View undo history
ls -la undo_history/
cat undo_history/history.json
```

### Configuration Files

```bash
# Edit categories configuration
nano config/categories.yaml

# Export configuration
python3 -c "from src.config_manager import ConfigManager; cm = ConfigManager(); print(cm.create_default_config())"
```

### Performance Monitoring

```bash
# Monitor CPU and memory usage
top -p $(pgrep -f "main.py")

# Monitor disk I/O
iostat -x 1
```

---

## 🎓 Best Practices

1. **Always use `--dry-run` first** to preview changes
2. **Check disk space** before organizing large directories
3. **Backup important files** before first-time organization
4. **Use `--stats`** to understand your file collection
5. **Use `--find-duplicates`** regularly to save space
6. **Filter files** to avoid processing unnecessary files
7. **Monitor logs** for errors and warnings
8. **Test on small directories** before processing large ones

---

## 🚀 Quick Reference Card

```bash
# Most common commands:

# Preview organization
python3 src/main.py --source DIR --target DIR --dry-run --stats

# Organize with duplicates check
python3 src/main.py --source DIR --target DIR --find-duplicates --stats

# Organize large files only
python3 src/main.py --source DIR --target DIR --min-size 10485760

# Organize excluding temp files
python3 src/main.py --source DIR --target DIR --exclude-ext .tmp .bak .swp

# Full featured command
python3 src/main.py --source DIR --target DIR --strategy category --min-size 1024 --max-size 104857600 --exclude-ext .tmp .bak --find-duplicates --stats
```

---

## 📞 Getting Help

```bash
# Show all available options
python3 src/main.py --help

# Check version
python3 -c "from src import __version__; print(__version__)"

# Test installation
python3 src/main.py --source /tmp --target /tmp --dry-run
```

---

**Happy Organizing on Linux! 🐧**

