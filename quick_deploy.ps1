# Quick one-line deployment commands

# First, set your VPS details (replace with your actual IP)
$VPS_IP = "YOUR_VPS_IP_HERE"
$VPS_USER = "root"

# One-command deployment
function Deploy-ToVPS {
    param([string]$vpsIP, [string]$vpsUser = "root")
    
    # Push to GitHub
    git add .; git commit -m "Deploy $(Get-Date)"; git push origin main
    
    # Deploy to VPS
    ssh "$vpsUser@$vpsIP" "cd /home/cambridgeexam/cambridge_exam_system && git pull origin main && source venv/bin/activate && pip install -r requirements_web.txt && sudo systemctl restart cambridge-exam && sudo systemctl status cambridge-exam --no-pager"
}

# Usage examples:
# Deploy-ToVPS -vpsIP "1.2.3.4"
# Deploy-ToVPS -vpsIP "1.2.3.4" -vpsUser "ubuntu"