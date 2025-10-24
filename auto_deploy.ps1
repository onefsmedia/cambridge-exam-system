# Automatic PowerShell deployment script for VPS 82.25.93.227
# No prompts - fully automated deployment

param(
    [switch]$SkipGit = $false
)

Write-Host "🚀 Auto-Deploying Cambridge Exam System to VPS..." -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# VPS Configuration
$VpsIP = "82.25.93.227"
$VpsUser = "root"

Write-Host "`n📋 Target: $VpsUser@$VpsIP" -ForegroundColor Cyan
Write-Host "🌐 Domain: cambridgeexam.dobeda.com" -ForegroundColor Cyan

# Step 1: Auto-commit and push to GitHub
if (-not $SkipGit) {
    Write-Host "`n📤 Step 1: Auto-pushing to GitHub..." -ForegroundColor Yellow
    
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "Auto-deploy $timestamp"
    
    git commit -m $commitMessage
    git push origin main
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Git push failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Successfully pushed to GitHub" -ForegroundColor Green
}

# Step 2: Create VPS deployment script
Write-Host "`n📡 Step 2: Creating VPS deployment script..." -ForegroundColor Yellow

$vpsScript = @'
#!/bin/bash
echo "🔄 Auto-updating Cambridge Exam System..."

# Create user if doesn't exist
if ! id "cambridgeexam" &>/dev/null; then
    echo "👤 Creating cambridgeexam user..."
    sudo useradd -m -s /bin/bash cambridgeexam
fi

# Navigate to app directory
APP_DIR="/home/cambridgeexam/cambridge_exam_system"
if [ ! -d "$APP_DIR" ]; then
    echo "📁 Creating app directory..."
    sudo mkdir -p $APP_DIR
    cd $APP_DIR
    sudo git clone https://github.com/onefsmedia/cambridge-exam-system.git .
else
    cd $APP_DIR
    echo "📥 Pulling latest changes..."
    sudo git pull origin main
fi

# Setup virtual environment
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    sudo python3 -m venv venv
fi

sudo chown -R cambridgeexam:cambridgeexam $APP_DIR
sudo -u cambridgeexam bash -c "source venv/bin/activate && pip install -r requirements_web.txt"

# Create directories and fix permissions
echo "🔧 Setting up directories and permissions..."
sudo mkdir -p uploads reports logs templates static
sudo chmod 755 uploads reports logs templates static
sudo chown -R cambridgeexam:cambridgeexam $APP_DIR
sudo chmod +x app.py wsgi.py

# Create/update systemd service
echo "⚙️ Setting up service..."
sudo tee /etc/systemd/system/cambridge-exam.service > /dev/null << 'EOF'
[Unit]
Description=Cambridge Exam System
After=network.target

[Service]
Type=exec
User=cambridgeexam
Group=cambridgeexam
WorkingDirectory=/home/cambridgeexam/cambridge_exam_system
Environment=PATH=/home/cambridgeexam/cambridge_exam_system/venv/bin
Environment=FLASK_ENV=production
Environment=HOST=0.0.0.0
Environment=PORT=5000
ExecStart=/home/cambridgeexam/cambridge_exam_system/venv/bin/python app.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Restart service
echo "🔄 Restarting service..."
sudo systemctl daemon-reload
sudo systemctl enable cambridge-exam
sudo systemctl stop cambridge-exam 2>/dev/null || true
sleep 2
sudo systemctl start cambridge-exam
sleep 5

# Test deployment
echo "🧪 Testing deployment..."
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "✅ Application is responding correctly"
    echo "🌐 Live at: https://cambridgeexam.dobeda.com/"
    sudo systemctl status cambridge-exam --no-pager -l
else
    echo "❌ Application test failed"
    echo "📋 Service status:"
    sudo systemctl status cambridge-exam --no-pager -l
    echo "📋 Recent logs:"
    sudo journalctl -u cambridge-exam -n 20 --no-pager
    exit 1
fi

echo "🎉 Auto-deployment completed!"
'@

# Save script to temp file
$tempScript = "auto_deploy_temp.sh"
$vpsScript | Out-File -FilePath $tempScript -Encoding UTF8

# Step 3: Deploy to VPS
Write-Host "`n🔗 Step 3: Auto-deploying to VPS..." -ForegroundColor Yellow

try {
    # Copy script to VPS
    Write-Host "📤 Copying deployment script to VPS..." -ForegroundColor White
    scp -o StrictHostKeyChecking=no $tempScript ${VpsUser}@${VpsIP}:/tmp/

    # Execute on VPS
    Write-Host "🚀 Executing deployment on VPS..." -ForegroundColor White
    ssh -o StrictHostKeyChecking=no ${VpsUser}@${VpsIP} "chmod +x /tmp/$tempScript && /tmp/$tempScript"

    Write-Host "`n🎉 Auto-deployment completed successfully!" -ForegroundColor Green
    Write-Host "🌐 Your application should be live at: https://cambridgeexam.dobeda.com/" -ForegroundColor Cyan
    
    Write-Host "`n📋 Quick check commands:" -ForegroundColor Gray
    Write-Host "  Test app: " -NoNewline -ForegroundColor Gray
    Write-Host "curl https://cambridgeexam.dobeda.com/health" -ForegroundColor White
    Write-Host "  Check logs: " -NoNewline -ForegroundColor Gray
    Write-Host "ssh $VpsUser@$VpsIP 'journalctl -u cambridge-exam -f'" -ForegroundColor White
}
catch {
    Write-Host "❌ Deployment failed: $_" -ForegroundColor Red
    exit 1
}
finally {
    # Cleanup
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")