"""
Cloud Storage Integration Module
Supports Google Drive, Dropbox, and OneDrive for organizing and uploading files.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Callable
from abc import ABC, abstractmethod


class CloudStorageProvider(ABC):
    """Base class for cloud storage providers."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize cloud storage provider.
        
        Args:
            credentials_path: Path to credentials/configuration file
        """
        self.credentials_path = credentials_path
        self.authenticated = False
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with cloud storage service.
        
        Returns:
            True if authentication successful
        """
        pass
    
    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str, 
                   progress_callback: Optional[Callable] = None) -> bool:
        """
        Upload a file to cloud storage.
        
        Args:
            local_path: Local file path
            remote_path: Remote file path in cloud
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if upload successful
        """
        pass
    
    @abstractmethod
    def upload_directory(self, local_dir: str, remote_base_path: str,
                        progress_callback: Optional[Callable] = None,
                        log_callback: Optional[Callable] = None) -> Dict:
        """
        Upload a directory to cloud storage.
        
        Args:
            local_dir: Local directory path
            remote_base_path: Base path in cloud storage
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with upload statistics
        """
        pass
    
    @abstractmethod
    def create_folder(self, folder_path: str) -> bool:
        """
        Create a folder in cloud storage.
        
        Args:
            folder_path: Path of folder to create
            
        Returns:
            True if folder created successfully
        """
        pass


class GoogleDriveProvider(CloudStorageProvider):
    """Google Drive integration."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        super().__init__(credentials_path)
        self.service = None
        self._folder_cache = {}  # Cache for folder IDs: {(name, parent_id): folder_id}
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            self.Credentials = Credentials
            self.InstalledAppFlow = InstalledAppFlow
            self.build = build
            self.MediaFileUpload = MediaFileUpload
            self.GOOGLE_DRIVE_AVAILABLE = True
        except ImportError:
            self.GOOGLE_DRIVE_AVAILABLE = False
    
    def authenticate(self) -> bool:
        """Authenticate with Google Drive."""
        if not self.GOOGLE_DRIVE_AVAILABLE:
            raise ImportError("Google Drive libraries not installed. Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        creds = None
        token_file = 'token.json'
        
        # Check for existing token
        if os.path.exists(token_file):
            try:
                creds = self.Credentials.from_authorized_user_file(token_file, SCOPES)
            except Exception:
                creds = None
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    from google.auth.transport.requests import Request
                    creds.refresh(Request())
                except Exception:
                    creds = None
            
            if not creds or not creds.valid:
                if not self.credentials_path:
                    raise ValueError(
                        "Google Drive credentials file required.\n\n"
                        "QUICK SETUP:\n"
                        "1. Click 'Setup Guide' button in GUI for step-by-step instructions\n"
                        "2. Or visit: https://console.cloud.google.com/apis/credentials\n"
                        "3. Create OAuth 2.0 credentials (Desktop app type)\n"
                        "4. Download JSON file and select it in the app\n\n"
                        "Don't forget to add your email as a test user!"
                    )
                
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        f"Please provide a valid path to your Google Cloud credentials JSON file.\n"
                        f"Download it from: https://console.cloud.google.com/apis/credentials"
                    )
                
                try:
                    flow = self.InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    error_msg = str(e)
                    if "default credentials" in error_msg.lower() or "adc" in error_msg.lower():
                        raise Exception(
                            f"Google Drive authentication failed.\n\n"
                            f"To fix this:\n"
                            f"1. Make sure you selected the credentials JSON file in the GUI\n"
                            f"2. The file should be downloaded from Google Cloud Console\n"
                            f"3. It should be a JSON file with 'client_id' and 'client_secret'\n\n"
                            f"Get credentials from: https://console.cloud.google.com/apis/credentials\n"
                            f"Original error: {error_msg}"
                        )
                    elif "access_denied" in error_msg.lower() or "403" in error_msg.lower() or "verification" in error_msg.lower():
                        raise Exception(
                            f"Google Drive Access Blocked (Error 403)\n\n"
                            f"This happens because your app is in testing mode.\n\n"
                            f"To fix:\n"
                            f"1. Go to https://console.cloud.google.com/apis/credentials/consent\n"
                            f"2. Scroll to 'Test users' section\n"
                            f"3. Click 'Add Users'\n"
                            f"4. Add your Google account email ({os.getenv('USER', 'your-email@gmail.com')})\n"
                            f"5. Click 'Add'\n"
                            f"6. Try authenticating again\n\n"
                            f"Note: Only test users can access the app during testing phase.\n"
                            f"For production, submit for Google verification."
                        )
                    else:
                        raise Exception(
                            f"Failed to authenticate with Google Drive: {error_msg}\n\n"
                            f"Make sure:\n"
                            f"1. The credentials file is valid JSON from Google Cloud Console\n"
                            f"2. OAuth consent screen is configured\n"
                            f"3. Google Drive API is enabled in your project\n"
                            f"4. Your email is added as a test user (if in testing mode)"
                        )
            
            # Save token for future use
            try:
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Warning: Could not save token file: {e}")
        
        self.service = self.build('drive', 'v3', credentials=creds)
        self.authenticated = True
        return True
    
    def create_folder(self, folder_path: str) -> bool:
        """Create folder in Google Drive."""
        if not self.authenticated:
            self.authenticate()
        
        folder_name = Path(folder_path).name
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        try:
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            return True
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False
    
    def upload_file(self, local_path: str, remote_path: str,
                   progress_callback: Optional[Callable] = None, parent_folder_id: Optional[str] = None) -> bool:
        """Upload file to Google Drive."""
        if not self.authenticated:
            self.authenticate()
        
        try:
            file_metadata = {'name': Path(remote_path).name}
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            
            media = self.MediaFileUpload(local_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            if progress_callback:
                progress_callback(100)
            
            return True
        except Exception as e:
            error_msg = str(e)
            # Re-raise exception with more context for better error reporting
            raise Exception(f"Failed to upload {Path(local_path).name}: {error_msg}")
    
    def _get_or_create_folder(self, folder_path: str, parent_id: Optional[str] = None, log_callback: Optional[Callable] = None) -> Optional[str]:
        """Get existing folder ID or create new folder in Google Drive."""
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        
        try:
            folder_name = Path(folder_path).name if '/' in folder_path or '\\' in folder_path else folder_path
            
            # Check cache first
            cache_key = (folder_name, parent_id)
            if cache_key in self._folder_cache:
                return self._folder_cache[cache_key]
            
            # Escape single quotes in folder name for query
            escaped_name = folder_name.replace("'", "\\'")
            
            # Search for existing folder
            query = f"name='{escaped_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            else:
                query += " and 'root' in parents"
            
            try:
                results = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id, name)'
                ).execute()
                
                items = results.get('files', [])
                if items:
                    folder_id = items[0]['id']
                    self._folder_cache[cache_key] = folder_id
                    return folder_id
            except Exception as search_error:
                # If search fails, try to create anyway
                error_msg = str(search_error)
                # Check for API not enabled error
                if 'accessNotConfigured' in error_msg or 'API has not been used' in error_msg or 'is disabled' in error_msg:
                    # Extract project ID if possible
                    project_id = None
                    if 'project' in error_msg.lower():
                        import re
                        match = re.search(r'project[^\d]*(\d+)', error_msg)
                        if match:
                            project_id = match.group(1)
                    
                    api_url = f"https://console.developers.google.com/apis/api/drive.googleapis.com/overview"
                    if project_id:
                        api_url += f"?project={project_id}"
                    
                    log(f"\n❌ CRITICAL ERROR: Google Drive API is not enabled!")
                    log(f"   The Google Drive API must be enabled in your Google Cloud project.")
                    log(f"   Enable it here: {api_url}")
                    log(f"   After enabling, wait 2-3 minutes for changes to propagate.")
                    log(f"   Then try again.\n")
                    # Don't try to create if API is disabled
                    return None
                elif 'invalid' not in error_msg.lower() and '400' not in error_msg:
                    log(f"Warning: Could not search for folder '{folder_name}': {error_msg}")
            
            # Create new folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            try:
                folder = self.service.files().create(body=file_metadata, fields='id').execute()
                folder_id = folder.get('id')
                if folder_id:
                    # Cache the result
                    self._folder_cache[cache_key] = folder_id
                    return folder_id
                else:
                    log(f"Error: Folder created but no ID returned for '{folder_name}'")
                    return None
            except Exception as create_error:
                error_msg = str(create_error)
                # Check for specific error types
                if 'accessNotConfigured' in error_msg or 'API has not been used' in error_msg or 'is disabled' in error_msg:
                    # Extract project ID if possible
                    project_id = None
                    if 'project' in error_msg.lower():
                        import re
                        match = re.search(r'project[^\d]*(\d+)', error_msg)
                        if match:
                            project_id = match.group(1)
                    
                    api_url = f"https://console.developers.google.com/apis/api/drive.googleapis.com/overview"
                    if project_id:
                        api_url += f"?project={project_id}"
                    
                    log(f"\n❌ CRITICAL ERROR: Google Drive API is not enabled!")
                    log(f"   The Google Drive API must be enabled in your Google Cloud project.")
                    log(f"   Enable it here: {api_url}")
                    log(f"   After enabling, wait 2-3 minutes for changes to propagate.")
                    log(f"   Then try again.\n")
                elif 'insufficientFilePermissions' in error_msg or ('403' in error_msg and 'accessNotConfigured' not in error_msg):
                    log(f"Error: Permission denied creating folder '{folder_name}'. Check Google Drive permissions.")
                elif 'quotaExceeded' in error_msg or 'storageQuotaExceeded' in error_msg:
                    log(f"Error: Google Drive quota exceeded. Cannot create folder '{folder_name}'.")
                elif 'invalid' in error_msg.lower() or '400' in error_msg:
                    log(f"Error: Invalid folder name '{folder_name}'. Google Drive may not allow this name or characters.")
                    log(f"  Try renaming the folder to remove special characters.")
                elif 'notFound' in error_msg.lower() or '404' in error_msg:
                    log(f"Error: Parent folder not found for '{folder_name}'. Check folder hierarchy.")
                else:
                    log(f"Error creating folder '{folder_name}': {error_msg}")
                return None
        except Exception as e:
            error_msg = str(e)
            log(f"Unexpected error creating folder '{folder_path}': {error_msg}")
            import traceback
            traceback.print_exc()
            return None
    
    def upload_directory(self, local_dir: str, remote_base_path: str,
                        progress_callback: Optional[Callable] = None,
                        log_callback: Optional[Callable] = None) -> Dict:
        """Upload directory to Google Drive with proper folder structure."""
        stats = {'uploaded': 0, 'failed': 0, 'total': 0, 'errors': []}
        
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        
        try:
            if not self.authenticated:
                self.authenticate()
            
            # Validate local directory
            if not os.path.exists(local_dir):
                stats['errors'].append(f"Local directory does not exist: {local_dir}")
                return stats
            
            if not os.path.isdir(local_dir):
                stats['errors'].append(f"Path is not a directory: {local_dir}")
                return stats
            
            # Create base folder structure
            base_folder_id = None
            if remote_base_path and remote_base_path != '/':
                # Create folder hierarchy
                path_parts = [p for p in remote_base_path.split('/') if p]
                current_parent = None
                for part in path_parts:
                    folder_id = self._get_or_create_folder(part, current_parent, log_callback)
                    if folder_id:
                        current_parent = folder_id
                    else:
                        error_msg = f"Failed to create folder: {part}"
                        stats['errors'].append(error_msg)
                        log(f"ERROR: {error_msg}")
                        # Don't return early - continue with root folder
                        base_folder_id = None
                        break
                base_folder_id = current_parent
        
            # Upload files maintaining directory structure
            log(f"Scanning directory: {local_dir}")
            dirs_found = 0
            files_found = 0
            
            # First, count all files to verify
            for root, dirs, files in os.walk(local_dir):
                files_found += len(files)
                dirs_found += len(dirs)
            
            log(f"Pre-scan: Found {files_found} files in {dirs_found} directories")
            
            if files_found == 0:
                error_msg = f"No files found in directory: {local_dir}"
                stats['errors'].append(error_msg)
                log(f"ERROR: {error_msg}")
                return stats
            
            # Step 1: Create all folder structure first
            log("Creating folder structure in Google Drive...")
            folder_map = {}  # Maps relative path (normalized) to folder ID
            folder_map['.'] = base_folder_id  # Root directory maps to base folder
            
            # First pass: Create all folders
            for root, dirs, files in os.walk(local_dir):
                rel_dir = os.path.relpath(root, local_dir)
                
                if rel_dir == '.':
                    # Root directory - already handled
                    continue
                
                # Normalize path for consistent matching
                normalized_path = rel_dir.replace('\\', '/')
                
                # Check if we already processed this path
                if normalized_path in folder_map:
                    continue
                
                # Build folder path parts
                path_parts = [p for p in normalized_path.split('/') if p]
                
                # Create folder hierarchy step by step
                current_parent = base_folder_id
                current_path_parts = []
                
                for part in path_parts:
                    current_path_parts.append(part)
                    current_path = '/'.join(current_path_parts)
                    
                    # Check if we already created this folder
                    if current_path in folder_map:
                        current_parent = folder_map[current_path]
                        continue
                    
                    # Create the folder
                    folder_id = self._get_or_create_folder(part, current_parent, log_callback)
                    if folder_id:
                        folder_map[current_path] = folder_id
                        current_parent = folder_id
                    else:
                        # Folder creation failed - use parent or root as fallback
                        log(f"WARNING: Failed to create folder '{part}' in path '{current_path}', using parent folder")
                        folder_map[current_path] = current_parent  # Use parent as fallback
                        # Continue with parent for remaining folders
                        break
            
            log(f"Created {len(folder_map)} folders in Google Drive")
            
            # Step 2: Upload files to their corresponding folders
            log("Uploading files to organized folders...")
            for root, dirs, files in os.walk(local_dir):
                # Get relative path from local_dir
                rel_dir = os.path.relpath(root, local_dir)
                
                # Get folder ID for this directory
                if rel_dir == '.':
                    current_folder_id = base_folder_id
                    folder_display_name = "base folder" if base_folder_id else "root"
                else:
                    # Normalize path for lookup
                    lookup_path = rel_dir.replace('\\', '/')
                    current_folder_id = folder_map.get(lookup_path, base_folder_id)
                    folder_display_name = rel_dir if current_folder_id else "root"
                    
                    if current_folder_id != base_folder_id and lookup_path not in folder_map:
                        log(f"WARNING: Folder not found for path '{lookup_path}', uploading to base folder")
                
                # Upload files in this directory
                for file in files:
                    stats['total'] += 1
                    local_file = os.path.join(root, file)
                    
                    # Show which folder file is being uploaded to
                    folder_name = folder_display_name
                    
                    if stats['total'] <= 5:  # Log first 5 files for debugging
                        log(f"  Processing file #{stats['total']}: {file} -> {folder_name}")
                    elif stats['total'] % 10 == 0:  # Log every 10th file
                        log(f"  Processing file #{stats['total']}/{files_found}...")
                    
                    try:
                        # Check if file exists and is readable
                        if not os.path.exists(local_file):
                            stats['failed'] += 1
                            stats['errors'].append(f"File not found: {local_file}")
                            continue
                        
                        if not os.access(local_file, os.R_OK):
                            stats['failed'] += 1
                            stats['errors'].append(f"File not readable: {local_file}")
                            continue
                        
                        # Upload the file
                        if self.upload_file(local_file, file, progress_callback, current_folder_id):
                            stats['uploaded'] += 1
                            if stats['uploaded'] <= 3:  # Log first 3 successful uploads
                                log(f"  ✓ Uploaded: {file}")
                        else:
                            stats['failed'] += 1
                            stats['errors'].append(f"Upload failed: {file} (check permissions/quota)")
                    except Exception as e:
                        stats['failed'] += 1
                        error_msg = str(e)
                        stats['errors'].append(f"Error uploading {file}: {error_msg}")
                        # Log first few errors for debugging
                        if len(stats['errors']) <= 5:
                            log(f"  ✗ Upload error for {file}: {error_msg}")
            
            log(f"\nUpload complete:")
            log(f"  Total files processed: {stats['total']}")
            log(f"  Successfully uploaded: {stats['uploaded']}")
            log(f"  Failed: {stats['failed']}")
            log(f"  Folders created: {len(folder_map)}")
            if stats['uploaded'] > 0:
                log(f"\n✓ Files uploaded to organized folder structure in Google Drive!")
            if stats['failed'] > 0:
                log(f"\n⚠ {stats['failed']} files failed to upload. Check errors above.")
            
        except Exception as e:
            error_msg = f"Critical error in upload_directory: {str(e)}"
            stats['errors'].append(error_msg)
            log(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
        
        return stats


class DropboxProvider(CloudStorageProvider):
    """Dropbox integration."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        super().__init__(credentials_path)
        self.client = None
        try:
            import dropbox
            self.dropbox = dropbox
            self.DROPBOX_AVAILABLE = True
        except ImportError:
            self.DROPBOX_AVAILABLE = False
    
    def authenticate(self) -> bool:
        """Authenticate with Dropbox."""
        if not self.DROPBOX_AVAILABLE:
            raise ImportError("Dropbox library not installed. Install with: pip install dropbox")
        
        if not self.credentials_path:
            # Try to get from environment or prompt
            access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
            if not access_token:
                raise ValueError("Dropbox access token required. Set DROPBOX_ACCESS_TOKEN or provide credentials_path")
        else:
            # Read token from file
            with open(self.credentials_path, 'r') as f:
                access_token = f.read().strip()
        
        self.client = self.dropbox.Dropbox(access_token)
        self.authenticated = True
        return True
    
    def create_folder(self, folder_path: str) -> bool:
        """Create folder in Dropbox."""
        if not self.authenticated:
            self.authenticate()
        
        try:
            self.client.files_create_folder_v2(folder_path)
            return True
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False
    
    def upload_file(self, local_path: str, remote_path: str,
                   progress_callback: Optional[Callable] = None) -> bool:
        """Upload file to Dropbox."""
        if not self.authenticated:
            self.authenticate()
        
        file_size = os.path.getsize(local_path)
        
        with open(local_path, 'rb') as f:
            if file_size <= 150 * 1024 * 1024:  # 150 MB
                # Simple upload
                self.client.files_upload(f.read(), remote_path)
            else:
                # Chunked upload for large files
                session_start_result = self.client.files_upload_session_start(f.read(4 * 1024 * 1024))
                cursor = self.dropbox.files.UploadSessionCursor(
                    session_id=session_start_result.session_id,
                    offset=f.tell()
                )
                
                while f.tell() < file_size:
                    chunk = f.read(4 * 1024 * 1024)
                    if len(chunk) == 0:
                        break
                    self.client.files_upload_session_append_v2(chunk, cursor)
                    cursor.offset = f.tell()
                
                self.client.files_upload_session_finish(b'', cursor, 
                                                       self.dropbox.files.CommitInfo(path=remote_path))
        
        if progress_callback:
            progress_callback(100)
        
        return True
    
    def upload_directory(self, local_dir: str, remote_base_path: str,
                        progress_callback: Optional[Callable] = None,
                        log_callback: Optional[Callable] = None) -> Dict:
        """Upload directory to Dropbox."""
        stats = {'uploaded': 0, 'failed': 0, 'total': 0}
        
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                stats['total'] += 1
                local_file = os.path.join(root, file)
                rel_path = os.path.relpath(local_file, local_dir)
                remote_file = os.path.join(remote_base_path, rel_path).replace('\\', '/')
                
                if self.upload_file(local_file, remote_file, progress_callback):
                    stats['uploaded'] += 1
                else:
                    stats['failed'] += 1
        
        return stats


class OneDriveProvider(CloudStorageProvider):
    """Microsoft OneDrive integration."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        super().__init__(credentials_path)
        self.client = None
        try:
            from msal import ConfidentialClientApplication, PublicClientApplication
            import requests
            self.msal = ConfidentialClientApplication
            self.PublicClientApplication = PublicClientApplication
            self.requests = requests
            self.ONEDRIVE_AVAILABLE = True
        except ImportError:
            self.ONEDRIVE_AVAILABLE = False
    
    def authenticate(self) -> bool:
        """Authenticate with OneDrive."""
        if not self.ONEDRIVE_AVAILABLE:
            raise ImportError("OneDrive libraries not installed. Install with: pip install msal requests")
        
        # OneDrive authentication requires app registration
        # This is a simplified version - full implementation needs app credentials
        client_id = os.getenv('ONEDRIVE_CLIENT_ID')
        client_secret = os.getenv('ONEDRIVE_CLIENT_SECRET')
        
        if not client_id:
            raise ValueError("OneDrive client ID required. Set ONEDRIVE_CLIENT_ID environment variable")
        
        # Use PublicClientApplication for device code flow
        app = self.PublicClientApplication(
            client_id=client_id,
            authority="https://login.microsoftonline.com/common"
        )
        
        # Get token using device code flow
        flow = app.initiate_device_flow(scopes=["Files.ReadWrite.All"])
        print(f"Visit {flow['verification_uri']} and enter code: {flow['user_code']}")
        
        result = app.acquire_token_by_device_flow(flow)
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            self.authenticated = True
            return True
        else:
            raise Exception(f"Authentication failed: {result.get('error_description')}")
    
    def create_folder(self, folder_path: str) -> bool:
        """Create folder in OneDrive."""
        if not self.authenticated:
            self.authenticate()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "name": Path(folder_path).name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        
        try:
            response = self.requests.post(
                'https://graph.microsoft.com/v1.0/me/drive/root/children',
                headers=headers,
                json=data
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False
    
    def upload_file(self, local_path: str, remote_path: str,
                   progress_callback: Optional[Callable] = None) -> bool:
        """Upload file to OneDrive."""
        if not self.authenticated:
            self.authenticate()
        
        file_size = os.path.getsize(local_path)
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Length': str(file_size)
        }
        
        try:
            with open(local_path, 'rb') as f:
                if file_size < 4 * 1024 * 1024:  # 4 MB
                    # Simple upload
                    headers['Content-Type'] = 'application/octet-stream'
                    response = self.requests.put(
                        f'https://graph.microsoft.com/v1.0/me/drive/root:/{remote_path}:/content',
                        headers=headers,
                        data=f.read()
                    )
                else:
                    # Resumable upload for large files
                    # Simplified - full implementation needs session management
                    headers['Content-Type'] = 'application/octet-stream'
                    response = self.requests.put(
                        f'https://graph.microsoft.com/v1.0/me/drive/root:/{remote_path}:/content',
                        headers=headers,
                        data=f.read()
                    )
            
            if progress_callback:
                progress_callback(100)
            
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error uploading file {local_path}: {e}")
            return False
    
    def upload_directory(self, local_dir: str, remote_base_path: str,
                        progress_callback: Optional[Callable] = None,
                        log_callback: Optional[Callable] = None) -> Dict:
        """Upload directory to OneDrive."""
        stats = {'uploaded': 0, 'failed': 0, 'total': 0}
        
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                stats['total'] += 1
                local_file = os.path.join(root, file)
                rel_path = os.path.relpath(local_file, local_dir)
                remote_file = os.path.join(remote_base_path, rel_path).replace('\\', '/')
                
                if self.upload_file(local_file, remote_file, progress_callback):
                    stats['uploaded'] += 1
                else:
                    stats['failed'] += 1
        
        return stats


class CloudStorageManager:
    """Manager for cloud storage operations."""
    
    def __init__(self):
        """Initialize cloud storage manager."""
        self.providers = {
            'googledrive': GoogleDriveProvider,
            'dropbox': DropboxProvider,
            'onedrive': OneDriveProvider
        }
    
    def get_provider(self, provider_name: str, credentials_path: Optional[str] = None) -> CloudStorageProvider:
        """
        Get cloud storage provider instance.
        
        Args:
            provider_name: Name of provider ('googledrive', 'dropbox', 'onedrive')
            credentials_path: Path to credentials file
            
        Returns:
            CloudStorageProvider instance
        """
        provider_name = provider_name.lower()
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {list(self.providers.keys())}")
        
        return self.providers[provider_name](credentials_path)
    
    def organize_and_upload(self, source_dir: str, cloud_provider: str,
                           remote_base_path: str, organize_first: bool = True,
                           target_dir: Optional[str] = None,
                           credentials_path: Optional[str] = None,
                           log_callback: Optional[Callable] = None) -> Dict:
        """
        Organize files locally and upload to cloud storage.
        
        Args:
            source_dir: Local source directory
            cloud_provider: Cloud provider name
            remote_base_path: Base path in cloud storage
            organize_first: Whether to organize files before uploading
            target_dir: Local target directory for organization (if None, uses temp)
            credentials_path: Path to credentials file
            log_callback: Optional callback function for logging messages
            
        Returns:
            Dictionary with operation statistics
        """
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)
        from directory_organizer import DirectoryOrganizer
        from file_analyzer import FileAnalyzer
        from ai_categorizer import AICategorizer
        
        stats = {
            'organized': False,
            'uploaded': 0,
            'failed': 0,
            'total_files': 0
        }
        
        # Step 1: Organize files locally if requested
        if organize_first:
            if not target_dir:
                import tempfile
                target_dir = tempfile.mkdtemp(prefix='organize_')
            
            print("Organizing files locally...")
            analyzer = FileAnalyzer()
            files_info = analyzer.scan_directory(source_dir, recursive=True)
            
            categorizer = AICategorizer()
            categorized = categorizer.categorize_files(files_info)
            
            organizer = DirectoryOrganizer(target_dir, dry_run=False, subcategorize=True)
            org_stats = organizer.organize_files(categorized, organization_strategy='category',
                                                 subcategorize=True, preserve_structure=True)
            
            stats['organized'] = True
            stats['total_files'] = org_stats['total_files']
            upload_source = target_dir
        else:
            upload_source = source_dir
        
        # Step 2: Upload to cloud storage
        print(f"Uploading to {cloud_provider}...")
        try:
            # Validate upload source directory
            if not os.path.exists(upload_source):
                raise FileNotFoundError(f"Upload source directory does not exist: {upload_source}")
            
            if not os.path.isdir(upload_source):
                raise ValueError(f"Upload source is not a directory: {upload_source}")
            
            # Count files before upload for better reporting
            file_count = 0
            for root, dirs, files in os.walk(upload_source):
                file_count += len(files)
            
            log(f"Found {file_count} files to upload in: {upload_source}")
            
            if file_count == 0:
                log("⚠️ Warning: No files found in upload source directory!")
                stats['total_files'] = 0
                return stats
            
            provider = self.get_provider(cloud_provider, credentials_path)
            log("Authenticating with cloud storage...")
            provider.authenticate()
            log("Authentication successful!")
            
            log(f"Starting upload from: {upload_source}")
            log(f"Uploading to: {remote_base_path}")
            
            # Pass log callback to upload_directory if provider supports it
            upload_stats = provider.upload_directory(upload_source, remote_base_path, 
                                                    progress_callback=None, 
                                                    log_callback=log_callback)
            
            stats['uploaded'] = upload_stats.get('uploaded', 0)
            stats['failed'] = upload_stats.get('failed', 0)
            stats['total_files'] = upload_stats.get('total', 0)
            
            # Log errors if any
            if upload_stats.get('errors'):
                print(f"\n⚠️ Upload errors encountered ({len(upload_stats['errors'])} errors):")
                for error in upload_stats['errors'][:10]:  # Show first 10 errors
                    print(f"  - {error}")
                if len(upload_stats['errors']) > 10:
                    print(f"  ... and {len(upload_stats['errors']) - 10} more errors")
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Error during upload: {error_msg}")
            import traceback
            traceback.print_exc()
            stats['uploaded'] = 0
            stats['failed'] = stats.get('total_files', 0)
            raise Exception(f"Cloud upload failed: {error_msg}")
        
        return stats

