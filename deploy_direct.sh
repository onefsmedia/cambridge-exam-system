#!/bin/bash
# Direct VPS Deployment Script for Cambridge Exam System

set -e
echo "🚀 Starting Cambridge Exam System deployment..."

# Variables
APP_DIR="/home/cambridgeexam/cambridge_exam_system"
REPO_URL="https://github.com/onefsmedia/cambridge-exam-system.git"

# Create user if doesn't exist
echo "👤 Setting up user..."
if ! id "cambridgeexam" &>/dev/null; then
    useradd -m -s /bin/bash cambridgeexam
    echo "✅ Created user cambridgeexam"
else
    echo "✅ User cambridgeexam already exists"
fi

# Install required packages
echo "📦 Installing required packages..."
apt update -q
apt install -y python3 python3-pip python3-venv git curl

# Setup application directory
echo "📁 Setting up application directory..."
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR"
    cd "$APP_DIR"
    git clone "$REPO_URL" .
    echo "✅ Cloned repository"
else
    cd "$APP_DIR"
    echo "📥 Pulling latest changes..."
    git pull origin main
    echo "✅ Updated repository"
fi

# Setup virtual environment
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Created virtual environment"
fi

source venv/bin/activate
pip install -r requirements_web.txt
echo "✅ Installed Python dependencies"

# Create directories and fix permissions
echo "🔧 Setting up directories and permissions..."
mkdir -p uploads reports logs
chmod 755 uploads reports logs
chown -R cambridgeexam:cambridgeexam "$APP_DIR"
chmod +x app.py wsgi.py

# Create systemd service
echo "⚙️ Setting up service..."
cat > /etc/systemd/system/cambridge-exam.service << 'EOF'
[Unit]
Description=Cambridge Exam System
After=network.target

[Service]
Type=exec
User=cambridgeexam
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
echo "🔄 Starting service..."
systemctl daemon-reload
systemctl enable cambridge-exam
systemctl stop cambridge-exam 2>/dev/null || true
sleep 2
systemctl start cambridge-exam
sleep 5

# Test deployment
echo "🧪 Testing deployment..."
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "✅ Application is responding correctly"
    echo "🌐 Live at: https://cambridgeexam.dobeda.com/"
    systemctl status cambridge-exam --no-pager -l
else
    echo "❌ Application not responding"
    echo "📋 Service status:"
    systemctl status cambridge-exam --no-pager
    echo "📋 Recent logs:"
    journalctl -u cambridge-exam -n 10 --no-pager
fi

echo "🎉 Deployment script completed!"