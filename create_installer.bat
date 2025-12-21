@echo off
REM Batch script to create installer with auto-dependency installation
echo ============================================================
echo Creating Directory Management System Installer
echo ============================================================
echo.

REM Change to script directory to ensure correct paths
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Installing build dependencies...
REM Try python -m pip first (most reliable)
python -m pip install pyinstaller
if errorlevel 1 (
    echo Trying alternative pip command...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        echo Make sure pip is installed: python -m ensurepip --upgrade
        pause
        exit /b 1
    )
)

echo.
echo Step 2: Installing project dependencies...
echo Current directory: %CD%
if not exist requirements.txt (
    echo ERROR: requirements.txt not found in current directory
    echo Please make sure you're running this script from the project root
    pause
    exit /b 1
)
REM Try python -m pip first (most reliable)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Trying alternative pip command...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Make sure pip is installed: python -m ensurepip --upgrade
        pause
        exit /b 1
    )
)

echo.
echo Step 3: Building executable...
python build_exe.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Build Complete!
echo ============================================================
echo.
echo The executable is located in: dist\DirectoryManagementSystem.exe
echo.
echo You can now:
echo 1. Test the executable by running it
echo 2. Distribute the .exe file to other Windows computers
echo 3. The .exe includes all dependencies and does not require Python installation
echo.
pause

