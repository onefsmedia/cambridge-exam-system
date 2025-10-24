@echo off
echo ========================================
echo Cambridge Exam System - GitHub Deployment
echo ========================================
echo.

echo Step 1: Authenticating with GitHub...
"C:\Program Files\GitHub CLI\gh.exe" auth login --web
if %errorlevel% neq 0 (
    echo Authentication failed. Please authenticate manually.
    pause
    exit /b 1
)

echo.
echo Step 2: Creating GitHub repository...
"C:\Program Files\GitHub CLI\gh.exe" repo create cambridge-exam-system --public --description "Modern Cambridge International Examination Report System with advanced text wrapping and professional PDF generation"
if %errorlevel% neq 0 (
    echo Repository creation failed. It may already exist.
    echo Continuing with push...
)

echo.
echo Step 3: Setting up remote and pushing code...
git branch -M main

echo Adding remote origin...
git remote add origin https://github.com/%USERNAME%/cambridge-exam-system.git 2>nul
if %errorlevel% neq 0 (
    echo Remote already exists, updating...
    git remote set-url origin https://github.com/%USERNAME%/cambridge-exam-system.git
)

echo Pushing to GitHub...
git push -u origin main
if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Your repository has been deployed to GitHub!
    echo 🌐 Repository URL: https://github.com/%USERNAME%/cambridge-exam-system
    echo.
    echo Opening repository in browser...
    start https://github.com/%USERNAME%/cambridge-exam-system
) else (
    echo ❌ Push failed. Please check your GitHub authentication and try again.
)

echo.
pause