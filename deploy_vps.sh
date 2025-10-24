#!/bin/bash
# Quick CloudPanel deployment script for cambridgeexam.dobeda.com

echo "🚀 Deploying Cambridge Exam System to CloudPanel VPS..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install -y python3 python3-pip python3-venv git

# Create application user (if not exists)
if ! id "cambridgeexam" &>/dev/null; then
    useradd -m -s /bin/bash cambridgeexam
fi

# Create application directory
APP_DIR="/home/cambridgeexam/cambridge_exam_system"
mkdir -p $APP_DIR
cd $APP_DIR

# Clone repository
if [ ! -d ".git" ]; then
    git clone https://github.com/onefsmedia/cambridge-exam-system.git .
else
    git pull origin main
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_web.txt

# Create necessary directories
mkdir -p uploads reports logs
chmod 755 uploads reports logs

# Set ownership
chown -R cambridgeexam:cambridgeexam $APP_DIR

# Create systemd service
cat > /etc/systemd/system/cambridge-exam.service << EOF
[Unit]
Description=Cambridge Exam System
After=network.target

[Service]
Type=notify
User=cambridgeexam
Group=cambridgeexam
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 3 wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable cambridge-exam.service
systemctl start cambridge-exam.service

# Check status
systemctl status cambridge-exam.service

echo "✅ Deployment complete!"
echo "🌐 Application running on: http://your_domain:5000"
echo "📝 Configure nginx proxy in CloudPanel to point to localhost:5000"
echo "🔧 Service management:"
echo "   - Start: systemctl start cambridge-exam"
echo "   - Stop: systemctl stop cambridge-exam" 
echo "   - Restart: systemctl restart cambridge-exam"
echo "   - Logs: journalctl -u cambridge-exam -f"