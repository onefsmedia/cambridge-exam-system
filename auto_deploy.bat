@echo off
REM Automatic deployment script to VPS 82.25.93.227
REM No prompts - fully automated deployment

echo 🚀 Auto-Deploying Cambridge Exam System to VPS...
echo ================================================

REM VPS Configuration
set VPS_IP=82.25.93.227
set VPS_USER=root

echo 📋 Target: %VPS_USER%@%VPS_IP%
echo 🌐 Domain: cambridgeexam.dobeda.com
echo.

REM Step 1: Auto-commit and push to GitHub
echo 📤 Step 1: Auto-pushing to GitHub...
git add .

REM Auto-generate commit message with timestamp
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set mydate=%%a-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a:%%b
set COMMIT_MSG=Auto-deploy %mydate% %mytime%

git commit -m "%COMMIT_MSG%"
git push origin main

if %errorlevel% neq 0 (
    echo ❌ Git push failed!
    pause
    exit /b 1
)

echo ✅ Successfully pushed to GitHub

REM Step 2: Create VPS deployment script
echo.
echo 📡 Step 2: Creating VPS deployment script...

echo #!/bin/bash > auto_deploy.sh
echo echo "🔄 Auto-updating Cambridge Exam System..." >> auto_deploy.sh
echo. >> auto_deploy.sh
echo # Navigate to app directory >> auto_deploy.sh
echo APP_DIR="/home/cambridgeexam/cambridge_exam_system" >> auto_deploy.sh
echo if [ ! -d "$APP_DIR" ]; then >> auto_deploy.sh
echo   echo "📁 Creating app directory..." >> auto_deploy.sh
echo   mkdir -p $APP_DIR >> auto_deploy.sh
echo   cd $APP_DIR >> auto_deploy.sh
echo   git clone https://github.com/onefsmedia/cambridge-exam-system.git . >> auto_deploy.sh
echo else >> auto_deploy.sh
echo   cd $APP_DIR >> auto_deploy.sh
echo   echo "📥 Pulling latest changes..." >> auto_deploy.sh
echo   git pull origin main >> auto_deploy.sh
echo fi >> auto_deploy.sh
echo. >> auto_deploy.sh
echo # Setup virtual environment >> auto_deploy.sh
echo echo "🐍 Setting up Python environment..." >> auto_deploy.sh
echo if [ ! -d "venv" ]; then >> auto_deploy.sh
echo   python3 -m venv venv >> auto_deploy.sh
echo fi >> auto_deploy.sh
echo source venv/bin/activate >> auto_deploy.sh
echo pip install -r requirements_web.txt >> auto_deploy.sh
echo. >> auto_deploy.sh
echo # Create directories and fix permissions >> auto_deploy.sh
echo echo "🔧 Setting up directories and permissions..." >> auto_deploy.sh
echo mkdir -p uploads reports logs >> auto_deploy.sh
echo chmod 755 uploads reports logs >> auto_deploy.sh
echo sudo chown -R cambridgeexam:cambridgeexam $APP_DIR >> auto_deploy.sh
echo chmod +x app.py wsgi.py >> auto_deploy.sh
echo. >> auto_deploy.sh
echo # Create/update systemd service >> auto_deploy.sh
echo echo "⚙️ Setting up service..." >> auto_deploy.sh
echo sudo tee /etc/systemd/system/cambridge-exam.service ^> /dev/null ^<^< 'EOF' >> auto_deploy.sh
echo [Unit] >> auto_deploy.sh
echo Description=Cambridge Exam System >> auto_deploy.sh
echo After=network.target >> auto_deploy.sh
echo. >> auto_deploy.sh
echo [Service] >> auto_deploy.sh
echo Type=exec >> auto_deploy.sh
echo User=cambridgeexam >> auto_deploy.sh
echo Group=cambridgeexam >> auto_deploy.sh
echo WorkingDirectory=/home/cambridgeexam/cambridge_exam_system >> auto_deploy.sh
echo Environment=PATH=/home/cambridgeexam/cambridge_exam_system/venv/bin >> auto_deploy.sh
echo Environment=FLASK_ENV=production >> auto_deploy.sh
echo ExecStart=/home/cambridgeexam/cambridge_exam_system/venv/bin/python app.py >> auto_deploy.sh
echo Restart=always >> auto_deploy.sh
echo RestartSec=5 >> auto_deploy.sh
echo. >> auto_deploy.sh
echo [Install] >> auto_deploy.sh
echo WantedBy=multi-user.target >> auto_deploy.sh
echo EOF >> auto_deploy.sh
echo. >> auto_deploy.sh
echo # Restart service >> auto_deploy.sh
echo echo "🔄 Restarting service..." >> auto_deploy.sh
echo sudo systemctl daemon-reload >> auto_deploy.sh
echo sudo systemctl enable cambridge-exam >> auto_deploy.sh
echo sudo systemctl stop cambridge-exam 2^>/dev/null ^|^| true >> auto_deploy.sh
echo sleep 2 >> auto_deploy.sh
echo sudo systemctl start cambridge-exam >> auto_deploy.sh
echo sleep 3 >> auto_deploy.sh
echo. >> auto_deploy.sh
echo # Test deployment >> auto_deploy.sh
echo echo "🧪 Testing deployment..." >> auto_deploy.sh
echo if curl -s -f http://localhost:5000/health ^> /dev/null; then >> auto_deploy.sh
echo   echo "✅ Application is responding correctly" >> auto_deploy.sh
echo   echo "🌐 Live at: https://cambridgeexam.dobeda.com/" >> auto_deploy.sh
echo   sudo systemctl status cambridge-exam --no-pager >> auto_deploy.sh
echo else >> auto_deploy.sh
echo   echo "❌ Application test failed" >> auto_deploy.sh
echo   echo "📋 Service status:" >> auto_deploy.sh
echo   sudo systemctl status cambridge-exam --no-pager >> auto_deploy.sh
echo   echo "📋 Recent logs:" >> auto_deploy.sh
echo   sudo journalctl -u cambridge-exam -n 10 --no-pager >> auto_deploy.sh
echo fi >> auto_deploy.sh
echo. >> auto_deploy.sh
echo echo "🎉 Auto-deployment completed!" >> auto_deploy.sh

REM Step 3: Auto-deploy to VPS
echo.
echo 🔗 Step 3: Auto-deploying to VPS...

REM Copy and execute deployment script
echo 📤 Copying deployment script to VPS...
scp -P 2222 -o StrictHostKeyChecking=no auto_deploy.sh %VPS_USER%@%VPS_IP%:/tmp/

echo 🚀 Executing deployment on VPS...
ssh -p 2222 -o StrictHostKeyChecking=no %VPS_USER%@%VPS_IP% "chmod +x /tmp/auto_deploy.sh && /tmp/auto_deploy.sh"

REM Cleanup
del auto_deploy.sh

echo.
echo 🎉 Auto-deployment completed!
echo 🌐 Your application should be live at: https://cambridgeexam.dobeda.com/
echo.
echo 📋 Quick check commands:
echo   Test app: curl https://cambridgeexam.dobeda.com/health
echo   Check logs: ssh -p 2222 %VPS_USER%@%VPS_IP% "journalctl -u cambridge-exam -f"
echo.
pause