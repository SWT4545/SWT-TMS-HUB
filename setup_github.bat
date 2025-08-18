@echo off
echo ========================================
echo SMITH & WILLIAMS TRUCKING - TMS HUB
echo GitHub Repository Setup Script
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo Step 1: Initializing Git Repository...
git init

echo.
echo Step 2: Adding files to staging...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: Smith & Williams TMS Hub - Complete deployment-ready system"

echo.
echo ========================================
echo LOCAL REPOSITORY CREATED SUCCESSFULLY!
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://github.com
echo 2. Create a new repository named: SWT-TMS-HUB
echo 3. Do NOT initialize with README or .gitignore
echo 4. Copy the repository URL
echo.
echo Then run the following commands:
echo.
echo git remote add origin YOUR_REPOSITORY_URL
echo git branch -M main
echo git push -u origin main
echo.
echo ========================================
pause