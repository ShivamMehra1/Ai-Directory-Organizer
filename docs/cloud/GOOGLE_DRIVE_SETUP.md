# Google Drive Setup Guide - Step by Step

Complete guide to set up Google Drive integration and fix "Access blocked" errors.

---

## 🚨 Common Error: "Access blocked" or "Error 403: access_denied"

If you see this error, it means your Google account is not added as a test user. Follow the steps below to fix it.

---

## 📋 Complete Setup Steps

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter project name: "AI Directory Organizer" (or your choice)
5. Click "Create"
6. Wait for project creation, then select it

### Step 2: Enable Google Drive API

1. In the left sidebar, go to "APIs & Services" > "Library"
2. Search for "Google Drive API"
3. Click on "Google Drive API"
4. Click "Enable"
5. Wait for API to be enabled

### Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose user type:
   - **External** (for personal use or testing)
   - **Internal** (only if you have Google Workspace)
3. Click "Create"

#### Fill in App Information:

- **App name**: "AI Directory Organizer" (or your choice)
- **User support email**: Your email address
- **App logo**: (Optional) Upload a logo
- **Application home page**: (Optional) Your website
- **Authorized domains**: (Optional) Leave blank for testing
- **Developer contact information**: Your email address

4. Click "Save and Continue"

#### Add Scopes:

1. Click "Add or Remove Scopes"
2. In the filter box, search for "drive.file"
3. Check the box next to "https://www.googleapis.com/auth/drive.file"
4. Click "Update"
5. Click "Save and Continue"

#### Add Test Users (IMPORTANT!):

1. Scroll down to "Test users" section
2. Click "Add Users"
3. Enter your Google account email address (the one you'll use to authenticate)
   - Example: `yourname@gmail.com`
4. Click "Add"
5. You should see your email in the test users list

**⚠️ CRITICAL:** Without adding test users, you'll get "Access blocked" error!

6. Click "Save and Continue"
7. Review the summary and click "Back to Dashboard"

### Step 4: Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure consent screen (you already did this)
4. Application type: Select **"Desktop app"**
5. Name: "AI Directory Organizer Desktop" (or your choice)
6. Click "Create"
7. A dialog will appear with your credentials
8. Click "Download JSON"
9. Save the file somewhere safe (e.g., `credentials.json`)

**Important:** Keep this file secure! Don't share it publicly.

### Step 5: Use in Application

#### In GUI:
1. Launch the application
2. Check "Upload to Cloud Storage"
3. Select "googledrive" from Provider dropdown
4. Click "Browse" next to "Credentials File"
5. Select the downloaded `credentials.json` file
6. Enter Cloud Path (e.g., `/MyFiles`)
7. Click "Start Organization"

#### In CLI:
```bash
python3 src/main.py \
  --source ~/Documents \
  --target ~/Organized \
  --cloud-upload googledrive \
  --cloud-credentials /path/to/credentials.json \
  --cloud-path /MyFiles
```

### Step 6: First Authentication

1. When you run the application, a browser window will open
2. Sign in with your Google account (the one you added as test user)
3. You'll see a warning: "Google hasn't verified this app"
   - This is normal for testing apps
   - Click "Advanced"
   - Click "Go to AI Directory Organizer (unsafe)" or similar
4. Review permissions and click "Allow"
5. Authentication complete!
6. A token file (`token.json`) will be saved for future use

---

## 🔧 Troubleshooting

### Error: "Access blocked: AI file organiser has not completed the Google verification process"

**Cause:** Your email is not in the test users list.

**Solution:**
1. Go to [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
2. Scroll to "Test users"
3. Click "Add Users"
4. Add your Google account email
5. Click "Add"
6. Try authenticating again

### Error: "Invalid credentials"

**Cause:** Wrong credentials file or file corrupted.

**Solution:**
1. Make sure you downloaded the JSON file (not just copied the text)
2. Verify the file contains `client_id` and `client_secret`
3. Re-download credentials from Google Cloud Console if needed

### Error: "API not enabled"

**Cause:** Google Drive API is not enabled.

**Solution:**
1. Go to [API Library](https://console.cloud.google.com/apis/library)
2. Search for "Google Drive API"
3. Click "Enable"

### Error: "OAuth consent screen not configured"

**Cause:** OAuth consent screen setup is incomplete.

**Solution:**
1. Go to [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
2. Complete all required fields
3. Add at least one test user
4. Save all changes

---

## 📝 Quick Checklist

Before using Google Drive integration, make sure:

- [ ] Google Cloud project created
- [ ] Google Drive API enabled
- [ ] OAuth consent screen configured
- [ ] **Test users added (your email)**
- [ ] OAuth credentials created (Desktop app)
- [ ] Credentials JSON file downloaded
- [ ] Credentials file selected in application

---

## 🎯 For Production Use

If you want to make the app available to others:

1. **Complete OAuth Consent Screen:**
   - Fill in all required information
   - Add privacy policy URL
   - Add terms of service URL

2. **Submit for Verification:**
   - Go to OAuth consent screen
   - Click "Publish App"
   - Fill out verification form
   - Submit for Google review

3. **Note:** Verification can take several days to weeks

For personal use or testing, test users are sufficient.

---

## 🔒 Security Notes

1. **Never commit credentials.json to version control**
2. **Add credentials.json to .gitignore**
3. **Keep token.json secure** (it's auto-generated)
4. **Don't share credentials with others**
5. **Revoke credentials if compromised**

---

## 📚 Additional Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [OAuth Consent Screen Guide](https://support.google.com/cloud/answer/10311615)

---

**Need Help?** Check the error message in the application - it now provides specific guidance for common issues!

