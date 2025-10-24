#!/bin/bash
# Auto-fix script for Cambridge Exam System 502 Error
# This script will automatically configure nginx to proxy to your Flask app

set -e  # Exit on any error

echo "🔧 Cambridge Exam System - Auto-fixing 502 Bad Gateway Error"
echo "=============================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script as root (or with sudo)"
    exit 1
fi

# 1. First, verify the Flask app is running
echo "🔍 Step 1: Checking Flask application status..."
if systemctl is-active --quiet cambridge-exam.service; then
    echo "✅ Cambridge Exam service is running"
else
    echo "⚠️  Starting Cambridge Exam service..."
    systemctl start cambridge-exam.service
    sleep 3
fi

# Test local connection
if curl -s -f http://127.0.0.1:5000/health > /dev/null; then
    echo "✅ Flask app responding on port 5000"
else
    echo "❌ Flask app not responding. Checking logs..."
    systemctl status cambridge-exam.service --no-pager -l
    exit 1
fi

# 2. Find the correct nginx configuration path
echo ""
echo "🔍 Step 2: Finding nginx configuration..."

# Common CloudPanel site config locations
POSSIBLE_CONFIGS=(
    "/etc/nginx/sites-available/cambridgeexam.dobeda.com"
    "/etc/nginx/sites-enabled/cambridgeexam.dobeda.com"
    "/etc/nginx/conf.d/cambridgeexam.dobeda.com.conf"
    "/etc/nginx/sites-available/cambridgeexam.dobeda.com.conf"
)

NGINX_CONFIG=""
for config in "${POSSIBLE_CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        NGINX_CONFIG="$config"
        echo "✅ Found nginx config: $config"
        break
    fi
done

# If no config found, create one
if [ -z "$NGINX_CONFIG" ]; then
    echo "⚠️  No existing config found. Creating new nginx configuration..."
    NGINX_CONFIG="/etc/nginx/sites-available/cambridgeexam.dobeda.com"
    
    # Create comprehensive nginx config
    cat > "$NGINX_CONFIG" << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name cambridgeexam.dobeda.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name cambridgeexam.dobeda.com;

    # SSL Configuration (adjust paths as needed)
    ssl_certificate /etc/ssl/certs/cambridgeexam.dobeda.com.crt;
    ssl_certificate_key /etc/ssl/private/cambridgeexam.dobeda.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Main proxy configuration
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
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:5000;
        access_log off;
    }

    # Static files (if any)
    location /static/ {
        alias /home/cambridgeexam/cambridge_exam_system/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Logs
    error_log /var/log/nginx/cambridgeexam.dobeda.com.error.log;
    access_log /var/log/nginx/cambridgeexam.dobeda.com.access.log;
}
EOF
    echo "✅ Created new nginx configuration"
else
    # Backup existing config
    cp "$NGINX_CONFIG" "${NGINX_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backed up existing configuration"
    
    # Check if proxy configuration already exists
    if grep -q "proxy_pass.*127.0.0.1:5000" "$NGINX_CONFIG"; then
        echo "✅ Proxy configuration already exists"
    else
        echo "⚠️  Adding proxy configuration to existing file..."
        
        # Create a temporary file with the proxy configuration
        cat > /tmp/proxy_config << 'EOF'
    # Cambridge Exam System Proxy Configuration
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
EOF
        
        # Try to insert the proxy configuration
        if grep -q "location.*/" "$NGINX_CONFIG"; then
            echo "⚠️  Existing location block found. Please manually add proxy configuration."
            echo "Configuration needed:"
            cat /tmp/proxy_config
        else
            # Insert before the last closing brace of the server block
            sed -i '/^[[:space:]]*}[[:space:]]*$/i\
\
    # Cambridge Exam System Proxy Configuration\
    location / {\
        proxy_pass http://127.0.0.1:5000;\
        proxy_set_header Host $host;\
        proxy_set_header X-Real-IP $remote_addr;\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\
        proxy_set_header X-Forwarded-Proto $scheme;\
        proxy_redirect off;\
        proxy_connect_timeout 60s;\
        proxy_send_timeout 60s;\
        proxy_read_timeout 60s;\
    }' "$NGINX_CONFIG"
            echo "✅ Added proxy configuration"
        fi
    fi
fi

# 3. Enable the site if not already enabled
echo ""
echo "🔍 Step 3: Enabling nginx site..."
if [ ! -L "/etc/nginx/sites-enabled/cambridgeexam.dobeda.com" ]; then
    ln -sf "$NGINX_CONFIG" /etc/nginx/sites-enabled/cambridgeexam.dobeda.com
    echo "✅ Enabled nginx site"
else
    echo "✅ Site already enabled"
fi

# 4. Test nginx configuration
echo ""
echo "🔍 Step 4: Testing nginx configuration..."
if nginx -t; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration has errors!"
    echo "Restoring backup if available..."
    if [ -f "${NGINX_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)" ]; then
        cp "${NGINX_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)" "$NGINX_CONFIG"
        echo "⚠️  Restored backup configuration"
    fi
    exit 1
fi

# 5. Reload nginx
echo ""
echo "🔍 Step 5: Reloading nginx..."
systemctl reload nginx
echo "✅ Nginx reloaded successfully"

# 6. Final tests
echo ""
echo "🔍 Step 6: Running final tests..."

# Test local connection
echo "Testing local Flask app..."
if curl -s -f http://127.0.0.1:5000/health > /dev/null; then
    echo "✅ Local Flask app responding"
else
    echo "❌ Local Flask app not responding"
fi

# Test through nginx (if possible)
echo "Testing through nginx..."
if curl -s -f -H "Host: cambridgeexam.dobeda.com" http://127.0.0.1/health > /dev/null; then
    echo "✅ Nginx proxy working"
else
    echo "⚠️  Nginx proxy test failed (may need SSL certificate)"
fi

# 7. Show status summary
echo ""
echo "📊 DEPLOYMENT STATUS SUMMARY"
echo "============================="
echo "Flask Application:"
systemctl is-active cambridge-exam.service && echo "  ✅ Running" || echo "  ❌ Not running"

echo "Nginx Service:"
systemctl is-active nginx && echo "  ✅ Running" || echo "  ❌ Not running"

echo "Port 5000 (Flask):"
ss -tlnp | grep ":5000" > /dev/null && echo "  ✅ Listening" || echo "  ❌ Not listening"

echo "Nginx Configuration:"
nginx -t > /dev/null 2>&1 && echo "  ✅ Valid" || echo "  ❌ Invalid"

echo ""
echo "🎉 AUTO-FIX COMPLETED!"
echo "Your Cambridge Exam System should now be accessible at:"
echo "👉 https://cambridgeexam.dobeda.com/"
echo ""
echo "If you still see 502 errors, check:"
echo "1. SSL certificate configuration"
echo "2. Firewall settings"
echo "3. DNS configuration"
echo ""
echo "View logs with:"
echo "  sudo tail -f /var/log/nginx/cambridgeexam.dobeda.com.error.log"
echo "  sudo journalctl -u cambridge-exam.service -f"