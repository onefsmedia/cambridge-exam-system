#!/bin/bash
# Quick fix script for 502 Bad Gateway error

echo "🚀 Quick Fix for 502 Bad Gateway Error"
echo "======================================"

# Ensure we're in the right directory
APP_DIR="/home/examreports/cambridge_exam_system"
if [ ! -d "$APP_DIR" ]; then
    echo "❌ Application directory not found at $APP_DIR"
    echo "Creating directory and cloning repository..."
    mkdir -p $APP_DIR
    cd $APP_DIR
    git clone https://github.com/onefsmedia/cambridge-exam-system.git .
fi

cd $APP_DIR

# Install missing dependencies
echo "📦 Installing/updating dependencies..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements_web.txt

# Fix permissions
echo "🔧 Fixing permissions..."
sudo chown -R examreports:examreports $APP_DIR
chmod +x app.py wsgi.py

# Create missing directories
mkdir -p uploads reports logs templates
chmod 755 uploads reports logs templates

# Stop any existing service
echo "🛑 Stopping existing service..."
sudo systemctl stop cambridge-exam 2>/dev/null || true

# Kill any processes on port 5000
echo "🔍 Killing processes on port 5000..."
sudo pkill -f "python.*app.py" 2>/dev/null || true
sudo fuser -k 5000/tcp 2>/dev/null || true

# Test the app manually first
echo "🧪 Testing application manually..."
cd $APP_DIR
source venv/bin/activate

# Start the app in background for testing
python app.py &
APP_PID=$!
sleep 5

# Test if it's working
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200"; then
    echo "✅ Application is working manually"
    kill $APP_PID
else
    echo "❌ Application failed manual test"
    kill $APP_PID 2>/dev/null || true
    echo "Checking for errors..."
    python app.py
    exit 1
fi

# Recreate systemd service with correct paths
echo "🔄 Recreating systemd service..."
sudo tee /etc/systemd/system/cambridge-exam.service << EOF
[Unit]
Description=Cambridge Exam System
After=network.target

[Service]
Type=exec
User=examreports
Group=examreports
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=FLASK_ENV=production
ExecStart=$APP_DIR/venv/bin/python app.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload and start service
echo "🔄 Starting service..."
sudo systemctl daemon-reload
sudo systemctl enable cambridge-exam
sudo systemctl start cambridge-exam

# Wait and check status
sleep 5
if systemctl is-active --quiet cambridge-exam; then
    echo "✅ Service is running successfully"
    systemctl status cambridge-exam --no-pager -l
else
    echo "❌ Service failed to start"
    journalctl -u cambridge-exam -n 20 --no-pager
    exit 1
fi

# Test service response
echo "🧪 Testing service response..."
sleep 3
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200"; then
    echo "✅ Service is responding correctly"
else
    echo "❌ Service is not responding"
    journalctl -u cambridge-exam -n 10 --no-pager
fi

# Check nginx configuration
echo "🌐 Checking nginx configuration..."
if nginx -t; then
    echo "✅ Nginx configuration is valid"
    sudo systemctl reload nginx
else
    echo "❌ Nginx configuration error - please check CloudPanel settings"
fi

echo ""
echo "🎉 Fix completed!"
echo "📋 If still getting 502 errors:"
echo "1. Check CloudPanel site configuration"
echo "2. Ensure proxy_pass points to http://127.0.0.1:5000"
echo "3. Check nginx error logs: tail -f /var/log/nginx/error.log"
echo "4. Check application logs: journalctl -u cambridge-exam -f"