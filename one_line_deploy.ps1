# One-line auto deployment commands for VPS 82.25.93.227

# Set execution policy if needed (run once)
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Quick deployment functions
function Auto-Deploy {
    Write-Host "🚀 One-line deployment to 82.25.93.227..." -ForegroundColor Green
    
    # Auto-commit and push
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    git commit -m "Auto-deploy $timestamp"
    git push origin main
    
    # Deploy to VPS
    $deployScript = @'
cd /home/cambridgeexam/cambridge_exam_system 2>/dev/null || (sudo mkdir -p /home/cambridgeexam/cambridge_exam_system && cd /home/cambridgeexam/cambridge_exam_system && sudo git clone https://github.com/onefsmedia/cambridge-exam-system.git .) && sudo git pull origin main && sudo chown -R cambridgeexam:cambridgeexam /home/cambridgeexam/cambridge_exam_system && sudo -u cambridgeexam bash -c "cd /home/cambridgeexam/cambridge_exam_system && python3 -m venv venv 2>/dev/null || true && source venv/bin/activate && pip install -r requirements_web.txt" && sudo systemctl restart cambridge-exam 2>/dev/null && sleep 3 && curl -s http://localhost:5000/health && echo "✅ Deployed to https://cambridgeexam.dobeda.com/"
'@
    
    ssh root@82.25.93.227 $deployScript
}

function Quick-Deploy {
    Write-Host "⚡ Super quick deployment..." -ForegroundColor Yellow
    git add . ; git commit -m "Quick deploy $(Get-Date -Format 'HH:mm:ss')" ; git push origin main ; ssh root@82.25.93.227 "cd /home/cambridgeexam/cambridge_exam_system && git pull origin main && sudo systemctl restart cambridge-exam && curl -s http://localhost:5000/health"
}

function Deploy-Status {
    Write-Host "📊 Checking deployment status..." -ForegroundColor Cyan
    ssh root@82.25.93.227 "systemctl status cambridge-exam --no-pager && curl -s http://localhost:5000/health"
}

function Deploy-Logs {
    Write-Host "📋 Viewing deployment logs..." -ForegroundColor Cyan
    ssh root@82.25.93.227 "journalctl -u cambridge-exam -n 20 --no-pager"
}

# Usage examples:
Write-Host "🎯 Available Commands:" -ForegroundColor Green
Write-Host "  Auto-Deploy       # Full automated deployment"
Write-Host "  Quick-Deploy      # Super fast deployment"
Write-Host "  Deploy-Status     # Check if app is running"
Write-Host "  Deploy-Logs       # View recent logs"
Write-Host ""
Write-Host "Example: " -NoNewline -ForegroundColor Gray
Write-Host "Auto-Deploy" -ForegroundColor White