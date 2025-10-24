# PowerShell script for direct VPS deployment
# Run this in PowerShell on your Windows machine

param(
    [Parameter(Mandatory=$true)]
    [string]$VpsIP,
    
    [Parameter(Mandatory=$false)]
    [string]$VpsUser = "root",
    
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "Deploy from Windows PowerShell"
)

Write-Host "🚀 Cambridge Exam System - Direct VPS Deployment" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Step 1: Push to GitHub
Write-Host "`n📤 Step 1: Pushing changes to GitHub..." -ForegroundColor Yellow
git add .
git commit -m $CommitMessage
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Successfully pushed to GitHub" -ForegroundColor Green

# Step 2: Create VPS deployment script
Write-Host "`n📡 Step 2: Preparing VPS deployment..." -ForegroundColor Yellow

$vpsScript = @"
#!/bin/bash
echo "🔄 Updating Cambridge Exam System..."
cd /home/cambridgeexam/cambridge_exam_system || exit 1

# Pull latest changes
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Update dependencies
echo "📦 Updating dependencies..."
source venv/bin/activate
pip install -r requirements_web.txt

# Create missing directories
mkdir -p uploads reports logs
chmod 755 uploads reports logs

# Fix permissions
sudo chown -R cambridgeexam:cambridgeexam /home/cambridgeexam/cambridge_exam_system
chmod +x app.py wsgi.py

# Restart service
echo "🔄 Restarting service..."
sudo systemctl restart cambridge-exam
sleep 3

# Check status
echo "📊 Checking service status..."
sudo systemctl status cambridge-exam --no-pager

# Test application
echo "🧪 Testing application..."
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "✅ Application is responding correctly"
    echo "🌐 Live at: https://cambridgeexam.dobeda.com/"
else
    echo "❌ Application test failed"
    echo "📋 Checking logs..."
    sudo journalctl -u cambridge-exam -n 10 --no-pager
fi

echo "🎉 Deployment completed!"
"@

# Save script to temp file
$tempScript = "deploy_vps_temp.sh"
$vpsScript | Out-File -FilePath $tempScript -Encoding UTF8

# Step 3: Deploy to VPS
Write-Host "`n🔗 Step 3: Deploying to VPS ($VpsIP)..." -ForegroundColor Yellow

try {
    # Copy script to VPS
    Write-Host "📤 Copying deployment script to VPS..."
    scp $tempScript ${VpsUser}@${VpsIP}:/tmp/

    # Execute on VPS
    Write-Host "🚀 Executing deployment on VPS..."
    ssh ${VpsUser}@${VpsIP} "chmod +x /tmp/$tempScript && /tmp/$tempScript"

    Write-Host "`n🎉 Deployment completed successfully!" -ForegroundColor Green
    Write-Host "🌐 Your application should be live at: https://cambridgeexam.dobeda.com/" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Deployment failed: $_" -ForegroundColor Red
}
finally {
    # Cleanup
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")