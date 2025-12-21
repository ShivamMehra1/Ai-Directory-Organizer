# Quick Fix: Enable Google Drive API

## Problem
You're seeing this error:
```
Google Drive API has not been used in project [PROJECT_ID] before or it is disabled.
```

## Solution: Enable Google Drive API

### Step 1: Open Google Cloud Console
Go to: https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=193783738211

**Or manually:**
1. Go to https://console.cloud.google.com/
2. Select your project (or create one)
3. Navigate to "APIs & Services" > "Library"
4. Search for "Google Drive API"
5. Click on it

### Step 2: Enable the API
1. Click the **"ENABLE"** button
2. Wait for the API to be enabled (usually takes a few seconds)

### Step 3: Wait for Propagation
- After enabling, wait **2-3 minutes** for the changes to propagate
- This is important! The API won't work immediately

### Step 4: Try Again
- Go back to the application
- Try uploading again
- It should work now!

## Verification

To verify the API is enabled:
1. Go to: https://console.cloud.google.com/apis/dashboard?project=193783738211
2. Look for "Google Drive API" in the list
3. It should show "Enabled" status

## Common Issues

### "API still not working after enabling"
- Wait longer (up to 5 minutes)
- Make sure you're using the correct project
- Check that you clicked "ENABLE" (not just viewed the page)

### "Can't find the API"
- Make sure you're in the correct Google Cloud project
- The project ID should match: 193783738211
- Try searching for "Drive API" instead of "Google Drive API"

### "Permission denied"
- Make sure you're the project owner or have "Editor" role
- Check that billing is enabled (if required)

## Still Having Issues?

1. Check the project ID matches your credentials file
2. Verify OAuth consent screen is configured
3. Make sure your email is added as a test user
4. See `GOOGLE_DRIVE_SETUP.md` for complete setup guide

---

**Quick Link:** https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=193783738211

