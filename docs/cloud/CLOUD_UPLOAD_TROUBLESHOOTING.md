# Cloud Upload Troubleshooting Guide

## 🔍 Common Upload Issues and Fixes

### Issue: "Files uploaded: 0, Files failed: X"

This usually means files are failing to upload. Here's how to diagnose and fix:

---

## 🐛 Common Causes

### 1. **Permission Issues**
**Symptoms:** All files fail to upload
**Fix:**
- Make sure you granted proper permissions during OAuth
- Check that the app has "drive.file" scope
- Re-authenticate if needed

### 2. **Quota Exceeded**
**Symptoms:** Files fail with "quota" error
**Fix:**
- Check your Google Drive storage quota
- Free up space in Google Drive
- Upgrade your storage plan if needed

### 3. **Folder Creation Failed**
**Symptoms:** Files fail, errors mention folders
**Fix:**
- Make sure you have permission to create folders
- Check the cloud path is valid (e.g., `/MyFiles` not `C:\MyFiles`)

### 4. **File Size Limits**
**Symptoms:** Large files fail
**Fix:**
- Google Drive: 5TB per file (usually not an issue)
- Check individual file sizes
- Very large files may need resumable uploads (already implemented)

### 5. **Network Issues**
**Symptoms:** Intermittent failures
**Fix:**
- Check internet connection
- Try again - uploads will retry
- Use stable network connection

---

## 🔧 Debugging Steps

### Step 1: Check Error Messages
Look at the error messages in the log. They will tell you:
- Permission errors
- Quota errors
- File not found errors
- Network errors

### Step 2: Test with Small Folder
Try uploading a small folder first (1-2 files) to verify setup works.

### Step 3: Check Authentication
Make sure:
- ✅ Credentials file is valid
- ✅ You're added as test user (for Google Drive)
- ✅ Authentication completed successfully

### Step 4: Verify File Access
Make sure:
- ✅ Files exist and are readable
- ✅ No file locks (close other programs using files)
- ✅ Sufficient disk space

---

## 🛠️ Quick Fixes

### Fix 1: Re-authenticate
```python
# Delete token.json and re-authenticate
# The app will prompt for new authentication
```

### Fix 2: Check Cloud Path
- Use forward slashes: `/MyFiles` not `\MyFiles`
- Don't use Windows paths: `/MyFiles` not `C:\MyFiles`
- Start with `/` for root-relative paths

### Fix 3: Verify Permissions
1. Go to Google Drive
2. Check if folder was created
3. Verify you can manually upload files there

### Fix 4: Check File Count
The discrepancy (135 failed vs 45 total) suggests:
- Files might be counted multiple times
- Or there's an issue with the counting logic
- Check the actual files in the organized directory

---

## 📊 Understanding Upload Stats

- **Total files**: Number of files found to upload
- **Uploaded**: Successfully uploaded files
- **Failed**: Files that failed to upload
- **Errors**: List of specific error messages

If "failed" > "total", it might indicate:
- Files are being processed multiple times
- Or there's a counting issue

---

## 🎯 Best Practices

1. **Test First**: Always test with a small folder
2. **Check Logs**: Review error messages carefully
3. **Verify Setup**: Make sure authentication is complete
4. **Check Quota**: Ensure you have storage space
5. **Stable Network**: Use reliable internet connection

---

## 💡 Still Not Working?

1. **Check the log output** - Error messages will guide you
2. **Try Dropbox instead** - Simpler setup, might work better
3. **Upload manually first** - Verify your Google Drive access works
4. **Check Google Drive directly** - See if files appear there

---

**The improved error handling will now show you exactly what's failing!**

