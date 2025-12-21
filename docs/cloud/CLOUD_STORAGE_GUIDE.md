# Cloud Storage Integration Guide

Complete guide for using cloud storage integration with AI Directory Organizer v2.0.

---

## 📋 Overview

The cloud storage integration allows you to:
1. **Organize files locally** on your machine
2. **Upload organized files** to cloud storage (Google Drive, Dropbox, OneDrive)
3. **Automate the process** - organize and upload in one command

---

## 🚀 Quick Start

### Basic Usage

```bash
# Organize and upload to Google Drive
python3 src/main.py --source ~/Documents --target ~/Organized --cloud-upload googledrive --cloud-path /MyFiles

# Organize and upload to Dropbox
python3 src/main.py --source ~/Downloads --target ~/Organized --cloud-upload dropbox --cloud-path /Organized

# Organize and upload to OneDrive
python3 src/main.py --source ~/Pictures --target ~/Organized --cloud-upload onedrive --cloud-path /Photos
```

---

## 📦 Installation

### Install Cloud Storage Libraries

```bash
# Install all cloud storage dependencies
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib dropbox msal requests

# Or install from requirements.txt (includes cloud libraries)
pip install -r requirements.txt
```

---

## 🔐 Authentication Setup

### Google Drive Setup

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Drive API

2. **Create OAuth Credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app"
   - Download credentials JSON file

3. **Use Credentials:**
   ```bash
   python3 src/main.py --source ~/Documents --target ~/Organized \
     --cloud-upload googledrive \
     --cloud-credentials /path/to/credentials.json \
     --cloud-path /MyFiles
   ```

4. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type (unless you have Google Workspace)
   - Fill in app information:
     - App name: "AI Directory Organizer" (or your choice)
     - User support email: Your email
     - Developer contact: Your email
   - Add scopes: Click "Add or Remove Scopes"
     - Search for "drive.file" and add it
   - Add test users (IMPORTANT for testing):
     - Click "Add Users"
     - Add your Google account email (the one you'll use to authenticate)
     - Click "Add"
   - Click "Save and Continue" through all steps

5. **First Time Authentication:**
   - On first run, browser will open for authentication
   - You may see "Access blocked" if you're not a test user
   - **Solution**: Add your email as a test user in OAuth consent screen
   - Grant permissions
   - Token will be saved as `token.json` for future use

**⚠️ Important Note:**
- During testing, only approved test users can access the app
- If you see "Access blocked" error, add your email as a test user
- For production use, you'll need to submit for Google verification

### Dropbox Setup

**Option 1: Access Token (Recommended)**
```bash
# Get access token from Dropbox App Console
# https://www.dropbox.com/developers/apps

# Set as environment variable
export DROPBOX_ACCESS_TOKEN="your_access_token_here"

# Or save to file
echo "your_access_token_here" > dropbox_token.txt

# Use in command
python3 src/main.py --source ~/Documents --target ~/Organized \
  --cloud-upload dropbox \
  --cloud-credentials dropbox_token.txt \
  --cloud-path /Organized
```

**Option 2: Create Dropbox App**
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Create new app
3. Generate access token
4. Use token in credentials file

### OneDrive Setup

1. **Register Azure App:**
   - Go to [Azure Portal](https://portal.azure.com/)
   - Register new application
   - Add "Files.ReadWrite.All" permission
   - Note Client ID

2. **Set Environment Variables:**
   ```bash
   export ONEDRIVE_CLIENT_ID="your_client_id"
   export ONEDRIVE_CLIENT_SECRET="your_client_secret"  # If using confidential client
   ```

3. **Use in Command:**
   ```bash
   python3 src/main.py --source ~/Documents --target ~/Organized \
     --cloud-upload onedrive \
     --cloud-path /MyFiles
   ```

4. **First Time Authentication:**
   - Device code flow will be used
   - Visit URL and enter code shown
   - Token will be saved for future use

---

## 💻 Command Line Usage

### Basic Cloud Upload

```bash
# Organize and upload to cloud
python3 src/main.py \
  --source /path/to/source \
  --target /path/to/organized \
  --cloud-upload googledrive \
  --cloud-path /OrganizedFiles
```

### With Filtering

```bash
# Organize large files and upload
python3 src/main.py \
  --source ~/Documents \
  --target ~/Organized \
  --min-size 1048576 \
  --exclude-ext .tmp .bak \
  --cloud-upload dropbox \
  --cloud-path /LargeFiles
```

### With Statistics

```bash
# Organize, get stats, and upload
python3 src/main.py \
  --source ~/Pictures \
  --target ~/Organized \
  --stats \
  --find-duplicates \
  --cloud-upload onedrive \
  --cloud-path /Photos \
  --cloud-credentials credentials.json
```

### Dry Run with Cloud Preview

```bash
# Preview organization (cloud upload won't happen in dry-run)
python3 src/main.py \
  --source ~/Documents \
  --target ~/Organized \
  --dry-run \
  --cloud-upload googledrive \
  --cloud-path /MyFiles
```

---

## 🖥️ GUI Usage

### Using Cloud Storage in GUI

1. **Launch GUI:**
   ```bash
   python3 src/gui_main.py
   ```

2. **Enable Cloud Upload:**
   - Check "Upload to Cloud Storage" checkbox
   - Select provider (Google Drive, Dropbox, OneDrive)
   - Enter cloud path (e.g., `/MyFiles`)
   - Browse and select credentials file (if needed)

3. **Organize and Upload:**
   - Select source and target directories
   - Configure other options as needed
   - Click "Start Organization"
   - Files will be organized locally first, then uploaded

---

## 📝 Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--cloud-upload` | Cloud provider to use | `--cloud-upload googledrive` |
| `--cloud-path` | Base path in cloud storage | `--cloud-path /MyFiles` |
| `--cloud-credentials` | Path to credentials file | `--cloud-credentials creds.json` |
| `--organize-then-upload` | Organize first, then upload (default) | `--organize-then-upload` |

---

## 🔧 Advanced Usage

### Upload Without Organizing

```bash
# Upload existing organized folder
python3 src/main.py \
  --source ~/AlreadyOrganized \
  --target ~/AlreadyOrganized \
  --cloud-upload googledrive \
  --cloud-path /Backup \
  --no-organize-then-upload
```

### Custom Cloud Path Structure

```bash
# Organize by date and upload to dated folders
python3 src/main.py \
  --source ~/Documents \
  --target ~/Organized \
  --strategy date \
  --cloud-upload dropbox \
  --cloud-path /Documents/$(date +%Y-%m)
```

### Batch Upload Script

```bash
#!/bin/bash
# upload_to_cloud.sh

SOURCE="$1"
CLOUD_PROVIDER="$2"
CLOUD_PATH="$3"

python3 src/main.py \
  --source "$SOURCE" \
  --target /tmp/organized_$$ \
  --cloud-upload "$CLOUD_PROVIDER" \
  --cloud-path "$CLOUD_PATH" \
  --cloud-credentials ~/.cloud_credentials.json \
  --stats

# Cleanup
rm -rf /tmp/organized_$$
```

---

## 🐛 Troubleshooting

### Issue: "Google Drive libraries not installed"

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Issue: "Dropbox library not installed"

```bash
pip install dropbox
```

### Issue: "OneDrive libraries not installed"

```bash
pip install msal requests
```

### Issue: Authentication Fails

**Google Drive:**
- Check credentials file path
- Ensure OAuth consent screen is configured
- Verify API is enabled

### Issue: "Access blocked" or "Error 403: access_denied"

**Problem:** Your Google account is not added as a test user.

**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "OAuth consent screen"
3. Scroll down to "Test users" section
4. Click "Add Users"
5. Enter your Google account email (the one you're using to authenticate)
6. Click "Add"
7. Try authenticating again

**Note:** During testing phase, only test users can access the app. For production, you'll need to submit for Google verification.

**Dropbox:**
- Verify access token is valid
- Check token hasn't expired
- Ensure app has correct permissions

**OneDrive:**
- Verify Client ID is correct
- Check Azure app permissions
- Ensure device code flow completes

### Issue: Upload Fails

- Check internet connection
- Verify cloud storage quota not exceeded
- Check file permissions
- Review error messages in log

### Issue: Large Files Fail to Upload

- Cloud providers have file size limits:
  - Google Drive: 5TB per file
  - Dropbox: 350GB per file (Pro)
  - OneDrive: 250GB per file
- Large files use chunked upload automatically

---

## 📊 Upload Progress

The system provides progress updates during upload:

```
Uploading to googledrive...
File 1/100: document1.pdf
File 2/100: image1.jpg
...
Upload Summary:
  Files uploaded: 98
  Files failed: 2
  Total files: 100
```

---

## 🔒 Security Best Practices

1. **Credentials Storage:**
   - Never commit credentials to version control
   - Use environment variables when possible
   - Store credentials in secure location
   - Use `.gitignore` for credential files

2. **Token Management:**
   - Tokens are saved locally after first auth
   - Keep token files secure
   - Revoke tokens if compromised

3. **Permissions:**
   - Use minimum required permissions
   - Review app permissions regularly
   - Use separate credentials for different purposes

---

## 📚 Examples

### Example 1: Backup Documents to Google Drive

```bash
python3 src/main.py \
  --source ~/Documents \
  --target ~/Documents_Backup \
  --cloud-upload googledrive \
  --cloud-path /Backups/Documents \
  --cloud-credentials ~/.google_credentials.json \
  --stats
```

### Example 2: Organize Photos and Upload to Dropbox

```bash
python3 src/main.py \
  --source ~/Pictures \
  --target ~/Pictures_Organized \
  --strategy date \
  --exclude-ext .tmp .bak \
  --cloud-upload dropbox \
  --cloud-path /Photos \
  --find-duplicates \
  --stats
```

### Example 3: Organize Large Files to OneDrive

```bash
python3 src/main.py \
  --source ~/Storage \
  --target ~/Storage_Organized \
  --min-size 104857600 \
  --cloud-upload onedrive \
  --cloud-path /LargeFiles \
  --stats
```

---

## 🎯 Tips

1. **Always test with dry-run first:**
   ```bash
   --dry-run --cloud-upload googledrive
   ```

2. **Use statistics to understand upload:**
   ```bash
   --stats --cloud-upload dropbox
   ```

3. **Filter before uploading to save time:**
   ```bash
   --exclude-ext .tmp .bak --cloud-upload onedrive
   ```

4. **Monitor upload progress in logs:**
   ```bash
   tail -f logs/organization_*.log
   ```

5. **Use organized target as source for upload:**
   - Organize first, then upload separately if needed

---

## 📞 Support

For issues with cloud storage integration:
1. Check authentication setup
2. Verify credentials are valid
3. Review error messages in logs
4. Test with small directory first
5. Check cloud storage service status

---

**Happy Cloud Organizing! ☁️**

