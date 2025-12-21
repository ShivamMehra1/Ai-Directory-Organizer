# Simplified Cloud Storage Setup

Quick and easy guide to set up cloud storage integration.

---

## 🚀 Quick Start (Choose Your Provider)

### Option 1: Google Drive (Most Popular)

**Time: 5-10 minutes**

#### Step 1: Get Credentials (3 minutes)
1. Click **"🌐 Open Console"** button in the GUI
2. Or visit: https://console.cloud.google.com/apis/credentials
3. Click **"Create Credentials"** → **"OAuth client ID"**
4. Choose **"Desktop app"**
5. Click **"Download JSON"**
6. Save the file somewhere you can find it

#### Step 2: Add Test User (1 minute)
1. Click **"🌐 Open Console"** → Choose "Consent Screen"
2. Or visit: https://console.cloud.google.com/apis/credentials/consent
3. Scroll to **"Test users"**
4. Click **"Add Users"**
5. Add your email (the one you'll sign in with)
6. Click **"Add"**

#### Step 3: Use in App (1 minute)
1. In the GUI, check **"Upload to Cloud Storage"**
2. Select **"googledrive"** from Provider dropdown
3. Click **"Browse"** and select the downloaded JSON file
4. Click **"🔍 Validate Credentials"** to check it's correct
5. Enter Cloud Path (e.g., `/MyFiles`)
6. Click **"Start Organization"**
7. Browser opens → Sign in → Allow access → Done! ✅

**That's it!** The app will remember your authentication.

---

### Option 2: Dropbox (Easiest)

**Time: 3-5 minutes**

#### Step 1: Get Access Token (2 minutes)
1. Visit: https://www.dropbox.com/developers/apps
2. Click **"Create app"**
3. Choose:
   - **Scoped access**
   - **Full Dropbox**
   - App name: "AI Directory Organizer"
4. Click **"Create app"**
5. Go to **"Settings"** tab
6. Under **"OAuth 2"**, click **"Generate access token"**
7. **Copy the token** (you won't see it again!)

#### Step 2: Save Token (1 minute)
1. Create a text file: `dropbox_token.txt`
2. Paste the token into the file
3. Save it

#### Step 3: Use in App (1 minute)
1. In the GUI, check **"Upload to Cloud Storage"**
2. Select **"dropbox"** from Provider dropdown
3. Click **"Browse"** and select `dropbox_token.txt`
4. Enter Cloud Path (e.g., `/Organized`)
5. Click **"Start Organization"**
6. Done! ✅

---

### Option 3: OneDrive

**Time: 5-10 minutes**

1. Register app in Azure Portal
2. Set `ONEDRIVE_CLIENT_ID` environment variable
3. Use device code flow for authentication

*(See CLOUD_STORAGE_GUIDE.md for detailed OneDrive setup)*

---

## 🎯 GUI Helper Buttons

The GUI now includes helpful buttons to simplify setup:

### 📖 Setup Guide Button
- Click to see step-by-step instructions
- Opens in a popup window
- Provider-specific instructions

### 🔍 Validate Credentials Button
- Checks if your credentials file is valid
- Shows what's wrong if there are issues
- Only works for Google Drive currently

### 🌐 Open Console Button
- Opens the cloud provider's console in your browser
- For Google Drive: Opens credentials or consent screen
- For Dropbox: Opens app console

---

## 💡 Pro Tips

1. **Use the GUI buttons** - They guide you through the process
2. **Validate credentials first** - Catch errors before uploading
3. **Save credentials securely** - Don't share them
4. **Test with small folder first** - Make sure everything works
5. **Check the log output** - See what's happening

---

## ❓ Common Questions

**Q: Do I need to do this every time?**  
A: No! After first authentication, the app saves a token. You only need to set up once.

**Q: Can I use multiple cloud providers?**  
A: Yes, but one at a time. Select different provider for different runs.

**Q: Is my data safe?**  
A: Yes! The app only requests `drive.file` scope (Google Drive), which is minimal. Your credentials are stored locally.

**Q: What if I lose my credentials file?**  
A: Just download a new one from Google Cloud Console. The token file (`token.json`) will still work.

---

## 🆘 Still Need Help?

1. Click **"📖 Setup Guide"** in the GUI
2. Check `QUICK_FIX_403_ERROR.md` for 403 errors
3. Check `GOOGLE_DRIVE_SETUP.md` for detailed Google Drive setup
4. Check `CLOUD_STORAGE_GUIDE.md` for complete documentation

---

**The setup is now much simpler with the helper buttons! 🎉**

