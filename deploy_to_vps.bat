@echo off
REM Direct deployment script from Windows to VPS
REM This script pushes code from local machine to cambridgeexam.dobeda.com VPS

echo 🚀 Deploying Cambridge Exam System to VPS...
echo =============================================

REM Set VPS connection details
set VPS_IP=82.25.93.227
set VPS_USER=root

echo.
echo 📋 Deployment Target: %VPS_USER%@%VPS_IP%
echo 🌐 Domain: cambridgeexam.dobeda.com
echo.
echo 📋 Deployment Steps:
echo 1. Push latest changes to GitHub
echo 2. Connect to VPS and pull updates
echo 3. Restart services
echo.

REM Step 1: Push to GitHub first
echo 📤 Step 1: Pushing to GitHub...
git add .
git status
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG="Deploy updates to VPS %date% %time%"

git commit -m "%COMMIT_MSG%"
git push origin main

if %errorlevel% neq 0 (
    echo ❌ Git push failed!
    pause
    exit /b 1
)

echo ✅ Successfully pushed to GitHub

REM Step 2: Create deployment commands for VPS
echo.
echo 📡 Step 2: Generating VPS deployment commands...

REM Create temporary script for VPS
echo #!/bin/bash > deploy_temp.sh
echo echo "🔄 Updating Cambridge Exam System on VPS..." >> deploy_temp.sh
echo cd /home/cambridgeexam/cambridge_exam_system >> deploy_temp.sh
echo git pull origin main >> deploy_temp.sh
echo source venv/bin/activate >> deploy_temp.sh
echo pip install -r requirements_web.txt >> deploy_temp.sh
echo sudo systemctl restart cambridge-exam >> deploy_temp.sh
echo sudo systemctl status cambridge-exam --no-pager >> deploy_temp.sh
echo echo "✅ Deployment complete!" >> deploy_temp.sh
echo echo "🌐 Check: https://cambridgeexam.dobeda.com/" >> deploy_temp.sh

REM Step 3: Execute on VPS
echo.
echo 🔗 Step 3: Connecting to VPS and deploying...
echo.
echo Executing deployment on %VPS_IP%...

REM Use SCP to copy script then execute
scp deploy_temp.sh %VPS_USER%@%VPS_IP%:/tmp/
ssh %VPS_USER%@%VPS_IP% "chmod +x /tmp/deploy_temp.sh && /tmp/deploy_temp.sh"

REM Cleanup
del deploy_temp.sh

echo.
echo 🎉 Deployment completed!
echo 📱 Test your application: https://cambridgeexam.dobeda.com/
echo.
pause