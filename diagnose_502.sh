#!/bin/bash
# 502 Bad Gateway Troubleshooting Script for Cambridge Exam System
# Run this on your VPS to diagnose and fix the issue

echo "🔍 Diagnosing 502 Bad Gateway Error..."
echo "======================================="

# Check if the application is running
echo "1. Checking if Cambridge Exam System service is running:"
if systemctl is-active --quiet cambridge-exam; then
    echo "✅ Service is running"
    systemctl status cambridge-exam --no-pager -l
else
    echo "❌ Service is NOT running"
    echo "Starting the service..."
    systemctl start cambridge-exam
    sleep 3
    systemctl status cambridge-exam --no-pager -l
fi

echo -e "\n2. Checking if application is listening on port 5000:"
if netstat -tuln | grep -q ":5000"; then
    echo "✅ Application is listening on port 5000"
    netstat -tuln | grep ":5000"
else
    echo "❌ Application is NOT listening on port 5000"
fi

echo -e "\n3. Testing application response:"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200"; then
    echo "✅ Application responds with 200 OK"
else
    echo "❌ Application not responding correctly"
    echo "Response:"
    curl -I http://localhost:5000 2>/dev/null || echo "Connection failed"
fi

echo -e "\n4. Checking application logs:"
echo "Last 10 lines of service logs:"
journalctl -u cambridge-exam -n 10 --no-pager

echo -e "\n5. Checking nginx configuration:"
if nginx -t 2>/dev/null; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration has errors:"
    nginx -t
fi

echo -e "\n6. Checking nginx status:"
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx is running"
else
    echo "❌ Nginx is not running"
    echo "Starting nginx..."
    systemctl start nginx
fi

echo -e "\n7. Quick fixes to try:"
echo "===================="
echo "Fix 1: Restart the application service"
echo "sudo systemctl restart cambridge-exam"
echo ""
echo "Fix 2: Check application directory permissions"
echo "sudo chown -R examreports:examreports /home/examreports/"
echo ""
echo "Fix 3: Restart nginx"
echo "sudo systemctl restart nginx"
echo ""
echo "Fix 4: Check if port 5000 is blocked"
echo "sudo ufw status | grep 5000"
echo ""
echo "Fix 5: Manual start for debugging"
echo "cd /home/examreports/cambridge_exam_system"
echo "source venv/bin/activate"
echo "python app.py"

echo -e "\n📋 Next steps:"
echo "1. If service is not running, check the logs above"
echo "2. If application is not responding, try manual start"
echo "3. If nginx config is invalid, fix the proxy settings"
echo "4. Check CloudPanel site configuration"