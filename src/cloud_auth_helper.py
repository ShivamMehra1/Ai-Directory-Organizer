"""
Cloud Authentication Helper
Simplifies the cloud storage authentication process with guided setup.
"""

import os
import json
import webbrowser
from pathlib import Path
from typing import Optional, Dict


class CloudAuthHelper:
    """Helper class to simplify cloud authentication setup."""
    
    @staticmethod
    def get_google_drive_setup_guide() -> str:
        """Get simplified Google Drive setup instructions."""
        return """
═══════════════════════════════════════════════════════════════
  GOOGLE DRIVE SETUP - SIMPLIFIED GUIDE
═══════════════════════════════════════════════════════════════

STEP 1: Create Credentials (5 minutes)
───────────────────────────────────────
1. Visit: https://console.cloud.google.com/apis/credentials
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop app"
4. Click "Download JSON"
5. Save the file (remember where!)

STEP 2: Add Yourself as Test User (1 minute)
──────────────────────────────────────────────
1. Visit: https://console.cloud.google.com/apis/credentials/consent
2. Scroll to "Test users"
3. Click "Add Users"
4. Add your email: {email}
5. Click "Add"

STEP 3: Use in Application
───────────────────────────
1. Select the downloaded JSON file in the app
2. Click "Start Organization"
3. Browser will open - sign in and allow access
4. Done! ✅

═══════════════════════════════════════════════════════════════
"""
    
    @staticmethod
    def validate_google_credentials(file_path: str) -> Dict:
        """
        Validate Google credentials file.
        
        Args:
            file_path: Path to credentials JSON file
            
        Returns:
            Dictionary with validation result
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        if not os.path.exists(file_path):
            result['errors'].append(f"File not found: {file_path}")
            return result
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check for required fields
            if 'installed' in data:
                creds = data['installed']
                if 'client_id' in creds:
                    result['info']['client_id'] = creds['client_id'][:20] + "..."
                else:
                    result['errors'].append("Missing 'client_id' in credentials")
                
                if 'client_secret' in creds:
                    result['info']['has_secret'] = True
                else:
                    result['errors'].append("Missing 'client_secret' in credentials")
                
                if 'project_id' in creds:
                    result['info']['project_id'] = creds['project_id']
                
                result['valid'] = len(result['errors']) == 0
            elif 'web' in data:
                result['warnings'].append("This appears to be a 'Web' credential. You need 'Desktop app' type.")
                result['errors'].append("Wrong credential type - use 'Desktop app' not 'Web application'")
            else:
                result['errors'].append("Invalid credentials format - missing 'installed' or 'web' section")
        
        except json.JSONDecodeError:
            result['errors'].append("Invalid JSON file")
        except Exception as e:
            result['errors'].append(f"Error reading file: {e}")
        
        return result
    
    @staticmethod
    def open_google_cloud_console(page: str = "credentials"):
        """Open Google Cloud Console in browser."""
        urls = {
            "credentials": "https://console.cloud.google.com/apis/credentials",
            "consent": "https://console.cloud.google.com/apis/credentials/consent",
            "library": "https://console.cloud.google.com/apis/library",
        }
        url = urls.get(page, urls["credentials"])
        webbrowser.open(url)
    
    @staticmethod
    def get_dropbox_setup_guide() -> str:
        """Get simplified Dropbox setup instructions."""
        return """
═══════════════════════════════════════════════════════════════
  DROPBOX SETUP - SIMPLIFIED GUIDE
═══════════════════════════════════════════════════════════════

OPTION 1: Quick Setup (Recommended)
────────────────────────────────────
1. Visit: https://www.dropbox.com/developers/apps
2. Click "Create app"
3. Choose:
   - Scoped access
   - Full Dropbox
   - App name: "AI Directory Organizer"
4. Click "Create app"
5. Go to "Permissions" tab
6. Check "files.content.write" and "files.content.read"
7. Go to "Settings" tab
8. Under "OAuth 2", click "Generate access token"
9. Copy the token
10. Save to a text file (e.g., dropbox_token.txt)
11. Select this file in the app

OPTION 2: Use Environment Variable
───────────────────────────────────
Set: DROPBOX_ACCESS_TOKEN="your_token_here"

═══════════════════════════════════════════════════════════════
"""
    
    @staticmethod
    def create_credentials_template(provider: str, output_path: str) -> bool:
        """
        Create a template/example credentials file.
        
        Args:
            provider: Cloud provider name
            output_path: Where to save template
            
        Returns:
            True if successful
        """
        templates = {
            "googledrive": {
                "installed": {
                    "client_id": "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com",
                    "project_id": "your-project-id",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "client_secret": "YOUR_CLIENT_SECRET_HERE",
                    "redirect_uris": ["http://localhost"]
                }
            },
            "dropbox": "YOUR_DROPBOX_ACCESS_TOKEN_HERE"
        }
        
        try:
            if provider == "googledrive":
                with open(output_path, 'w') as f:
                    json.dump(templates["googledrive"], f, indent=2)
            elif provider == "dropbox":
                with open(output_path, 'w') as f:
                    f.write(templates["dropbox"])
            else:
                return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def check_google_drive_prerequisites() -> Dict:
        """
        Check if Google Drive prerequisites are met.
        
        Returns:
            Dictionary with check results
        """
        checks = {
            'api_enabled': False,
            'oauth_configured': False,
            'test_users_added': False,
            'credentials_created': False,
            'messages': []
        }
        
        # These checks would require API access, so we provide guidance instead
        checks['messages'].append("To verify setup:")
        checks['messages'].append("1. Check API is enabled at: https://console.cloud.google.com/apis/library/drive")
        checks['messages'].append("2. Check OAuth consent screen at: https://console.cloud.google.com/apis/credentials/consent")
        checks['messages'].append("3. Verify test users are added")
        checks['messages'].append("4. Verify credentials are created")
        
        return checks

