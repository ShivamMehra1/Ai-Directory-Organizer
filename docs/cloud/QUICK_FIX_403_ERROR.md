# Quick Fix: Google Drive Error 403 - Access Denied

## 🚨 The Problem

You're seeing **"Error 403: access_denied"** when trying to authenticate with Google Drive.

**This happens because:** Your Google account is not in the test users list for your OAuth app.

---

## ✅ Quick Fix (2 Minutes)

### Step 1: Go to OAuth Consent Screen
1. Open: https://console.cloud.google.com/apis/credentials/consent
2. Make sure you're in the correct project (the one where you created credentials)

### Step 2: Add Your Email as Test User
1. Scroll down to the **"Test users"** section
2. Click **"Add Users"** button
3. Enter your Google account email (the one you're using to sign in)
   - Example: `harrybamotra007@gmail.com`
4. Click **"Add"**
5. You should see your email appear in the test users list

### Step 3: Try Again
1. Go back to the application
2. Try authenticating again
3. It should work now! ✅

---

## 📋 Visual Guide

```
Google Cloud Console
└── APIs & Services
    └── OAuth consent screen
        └── Scroll down
            └── Test users section
                └── Click "Add Users"
                    └── Enter your email
                        └── Click "Add"
```

---

## ⚠️ Important Notes

1. **Only test users can access** the app during testing phase
2. **Add each email** that will use the app
3. **Changes take effect immediately** - no need to wait
4. **For production**, you'll need to submit for Google verification

---

## 🔍 Verify It's Fixed

After adding your email:
1. The error should disappear
2. You'll see the permission screen
3. You can grant access to the app
4. Authentication will complete successfully

---

## 📞 Still Having Issues?

If you still get the error after adding your email:

1. **Check you're in the right project:**
   - Make sure the project dropdown shows your project
   - The one where you created the OAuth credentials

2. **Check the email matches:**
   - Use the exact same email you're signing in with
   - Check for typos

3. **Wait a few seconds:**
   - Sometimes changes take a moment to propagate

4. **Clear browser cache:**
   - Try in incognito/private window
   - Or clear cookies for accounts.google.com

---

## 🎯 Alternative: Use Different Cloud Provider

If Google Drive setup is too complex, you can use:

- **Dropbox** - Simpler setup, just needs access token
- **OneDrive** - Uses device code flow

See `CLOUD_STORAGE_GUIDE.md` for instructions.

---

**That's it! Add your email as a test user and you're good to go! 🚀**

