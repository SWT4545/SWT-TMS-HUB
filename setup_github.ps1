# Smith & Williams Trucking - TMS Hub
# GitHub Repository Setup Script (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SMITH & WILLIAMS TRUCKING - TMS HUB" -ForegroundColor Yellow
Write-Host "GitHub Repository Setup Script" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "✓ Git is installed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Initializing Git Repository..." -ForegroundColor Cyan
git init

Write-Host ""
Write-Host "Step 2: Adding files to staging..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "Step 3: Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Smith & Williams TMS Hub - Complete deployment-ready system"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "LOCAL REPOSITORY CREATED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com" -ForegroundColor White
Write-Host "2. Create a new repository named: SWT-TMS-HUB" -ForegroundColor White
Write-Host "3. Do NOT initialize with README or .gitignore" -ForegroundColor White
Write-Host "4. Copy the repository URL" -ForegroundColor White
Write-Host ""
Write-Host "Then run the following commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "git remote add origin YOUR_REPOSITORY_URL" -ForegroundColor Cyan
Write-Host "git branch -M main" -ForegroundColor Cyan
Write-Host "git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green

# Ask if user wants to open GitHub
$response = Read-Host "Would you like to open GitHub in your browser? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    Start-Process "https://github.com/new"
}

Read-Host "Press Enter to exit"