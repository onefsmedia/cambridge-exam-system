# Cambridge Exam System - Deployment Guide for cambridgeexam.dobeda.com

## 🚀 **Quick Deploy for Your Domain**

### **Option 1: Automated Deployment (Recommended)**

SSH into your VPS and run:

```bash
# Download and run the deployment script
wget https://raw.githubusercontent.com/onefsmedia/cambridge-exam-system/main/fix_502.sh
chmod +x fix_502.sh
sudo ./fix_502.sh
```

### **Option 2: Manual CloudPanel Setup**

#### **Step 1: Create Site in CloudPanel**
1. Login to CloudPanel
2. Go to **Sites** → **Add Site**
3. Site Settings:
   - **Domain**: `cambridgeexam.dobeda.com`
   - **Site Type**: Python
   - **Python Version**: 3.11
   - **Document Root**: `/public`

#### **Step 2: Upload Application**
```bash
# SSH into your VPS
ssh root@your_vps_ip

# Navigate to site directory
cd /home/cambridgeexam/htdocs/cambridgeexam.dobeda.com

# Clone the repository
git clone https://github.com/onefsmedia/cambridge-exam-system.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_web.txt

# Set permissions
chmod +x app.py wsgi.py
mkdir -p uploads reports logs
chmod 755 uploads reports logs
```

#### **Step 3: Configure Reverse Proxy**
1. In CloudPanel → **Sites** → **cambridgeexam.dobeda.com** → **Vhost**
2. Add this configuration:

```nginx
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

#### **Step 4: Create Systemd Service**
```bash
sudo tee /etc/systemd/system/cambridge-exam.service << 'EOF'
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
ExecStart=/home/cambridgeexam/cambridge_exam_system/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable cambridge-exam
sudo systemctl start cambridge-exam
```

#### **Step 5: Enable SSL Certificate**
1. In CloudPanel → **Sites** → **cambridgeexam.dobeda.com** → **SSL/TLS**
2. Click **New Let's Encrypt Certificate**
3. Enable **Force HTTPS**

---

## 🔧 **Troubleshooting 502 Errors**

### **Quick Diagnosis**
```bash
# Check if service is running
systemctl status cambridge-exam

# Check if app responds on port 5000
curl -I http://localhost:5000

# Check application logs
journalctl -u cambridge-exam -f

# Check nginx configuration
nginx -t
```

### **Common Fixes**

**1. Restart Application Service**
```bash
sudo systemctl restart cambridge-exam
```

**2. Check Port 5000 is Available**
```bash
sudo netstat -tuln | grep :5000
# Should show: tcp 0.0.0.0:5000 LISTEN
```

**3. Fix Permissions**
```bash
sudo chown -R cambridgeexam:cambridgeexam /home/cambridgeexam/
```

**4. Manual Test**
```bash
cd /home/cambridgeexam/cambridge_exam_system
source venv/bin/activate
python app.py
# Should show: * Running on http://0.0.0.0:5000
```

---

## 🧪 **Testing Your Deployment**

### **Application Health Check**
```bash
# Test application directly
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

### **Full Domain Test**
```bash
# Test your live domain
curl -I https://cambridgeexam.dobeda.com

# Expected response:
# HTTP/2 200 OK
```

---

## 📊 **Monitoring & Logs**

### **View Application Logs**
```bash
# Real-time logs
journalctl -u cambridge-exam -f

# Last 50 lines
journalctl -u cambridge-exam -n 50
```

### **View Nginx Logs**
```bash
# Access logs
tail -f /var/log/nginx/access.log

# Error logs
tail -f /var/log/nginx/error.log
```

---

## 🎯 **Final Verification**

After deployment, your Cambridge Exam System should be accessible at:

**🌐 https://cambridgeexam.dobeda.com/**

### **Expected Features:**
- ✅ Modern web interface
- ✅ 175+ Cambridge subjects
- ✅ PDF report generation
- ✅ Mobile responsive design
- ✅ SSL encryption
- ✅ Professional presentation

### **Test the System:**
1. Visit https://cambridgeexam.dobeda.com/
2. Fill in student information
3. Add subjects and scores
4. Generate PDF report
5. Download should work immediately

---

## 🆘 **Need Help?**

If you encounter any issues:

1. **Run the diagnostic script:**
   ```bash
   wget https://raw.githubusercontent.com/onefsmedia/cambridge-exam-system/main/diagnose_502.sh
   chmod +x diagnose_502.sh
   ./diagnose_502.sh
   ```

2. **Check service status:**
   ```bash
   systemctl status cambridge-exam
   ```

3. **Review logs:**
   ```bash
   journalctl -u cambridge-exam -n 20
   ```

Your Cambridge Exam System is now ready for production use! 🎉