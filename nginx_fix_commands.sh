#!/bin/bash

# Nginx Configuration Fix for Cambridge Exam System
# Run these commands on your VPS to fix the 502 Bad Gateway error

echo "🔧 Fixing nginx configuration for Cambridge Exam System..."

# 1. Create nginx site configuration
cat > /etc/nginx/sites-available/cambridgeexam.dobeda.com << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name cambridgeexam.dobeda.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name cambridgeexam.dobeda.com;

    # SSL Configuration (CloudPanel managed)
    ssl_certificate /etc/ssl/certs/cambridgeexam.dobeda.com.crt;
    ssl_certificate_key /etc/ssl/private/cambridgeexam.dobeda.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Proxy to Flask application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (if any)
    location /static/ {
        alias /home/cambridgeexam/cambridge_exam_system/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:5000;
        access_log off;
    }

    # Error and access logs
    error_log /var/log/nginx/cambridgeexam.dobeda.com.error.log;
    access_log /var/log/nginx/cambridgeexam.dobeda.com.access.log;
}
EOF

echo "✅ Created nginx site configuration"

# 2. Enable the site
ln -sf /etc/nginx/sites-available/cambridgeexam.dobeda.com /etc/nginx/sites-enabled/

echo "✅ Enabled nginx site"

# 3. Test nginx configuration
nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
    
    # 4. Reload nginx
    systemctl reload nginx
    echo "✅ Reloaded nginx"
    
    # 5. Check if services are running
    echo ""
    echo "🔍 Service Status:"
    echo "===================="
    echo "Cambridge Exam Service:"
    systemctl status cambridge-exam.service --no-pager -l | head -10
    
    echo ""
    echo "Nginx Service:"
    systemctl status nginx --no-pager -l | head -5
    
    echo ""
    echo "🌐 Testing application:"
    echo "======================="
    echo "Local health check:"
    curl -s http://127.0.0.1:5000/health || echo "❌ Local connection failed"
    
    echo ""
    echo "🎉 Configuration completed!"
    echo "Your site should now be accessible at: https://cambridgeexam.dobeda.com/"
    
else
    echo "❌ Nginx configuration has errors. Please check the configuration."
    nginx -t
fi