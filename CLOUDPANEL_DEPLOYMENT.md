# Cambridge Exam System - CloudPanel VPS Deployment Guide

## 🚀 Deployment Options

### Option 1: Web Application (Recommended)
Deploy as a web application that users can access through their browser.

#### CloudPanel Setup Steps:

1. **Create Python Site in CloudPanel**
   ```
   - Login to CloudPanel
   - Go to "Sites" → "Add Site"
   - Choose "Python" as application type
   - Set domain: examreports.yourdomain.com
   - Python version: 3.11
   ```

2. **Upload Application Files**
   ```bash
   # Connect via SSH or use CloudPanel file manager
   cd /home/examreports/htdocs/examreports.yourdomain.com
   
   # Clone repository
   git clone https://github.com/onefsmedia/cambridge-exam-system.git .
   
   # Install dependencies
   pip install -r requirements_web.txt
   ```

3. **Configure Application**
   ```bash
   # Set permissions
   chmod +x app.py wsgi.py
   
   # Create necessary directories
   mkdir -p uploads reports logs
   chmod 755 uploads reports logs
   ```

4. **CloudPanel Configuration**
   - Set Python executable path: `/usr/bin/python3`
   - Set application startup file: `wsgi.py`
   - Set application callable: `application`
   - Enable SSL certificate

#### Environment Variables (CloudPanel)
```
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your_secure_secret_key_here
MAX_CONTENT_LENGTH=16777216
```

#### Nginx Configuration (CloudPanel will handle this)
The web version will be accessible at: `https://examreports.yourdomain.com`

---

### Option 2: VNC Remote Desktop
Access the desktop GUI version remotely.

#### Setup Steps:

1. **Install VNC Server**
   ```bash
   # SSH into your VPS
   ssh root@your_vps_ip
   
   # Run the setup script
   wget https://raw.githubusercontent.com/onefsmedia/cambridge-exam-system/main/setup_vnc.sh
   chmod +x setup_vnc.sh
   ./setup_vnc.sh
   ```

2. **Configure VNC Password**
   ```bash
   vncpasswd
   # Enter your secure password
   ```

3. **Start VNC Server**
   ```bash
   vncserver :1 -geometry 1280x800 -depth 24
   ```

4. **Connect from Your Computer**
   - Download VNC Viewer: https://www.realvnc.com/download/viewer/
   - Connect to: `your_vps_ip:5901`
   - Enter your VNC password

5. **Run the Application**
   ```bash
   # In VNC desktop, open terminal
   cd ~/cambridge_exam_system
   source venv/bin/activate
   python main_gui_complete.py
   ```

---

### Option 3: Docker Container (Advanced)

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY . .
   
   RUN pip install -r requirements_web.txt
   
   EXPOSE 5000
   
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
   ```

2. **Deploy with Docker**
   ```bash
   docker build -t cambridge-exam-system .
   docker run -d -p 5000:5000 cambridge-exam-system
   ```

---

## 🔧 CloudPanel Specific Configuration

### Python Site Settings
- **Document Root**: `/public` (for static files)
- **Python Version**: 3.11
- **Application Type**: Flask
- **Startup File**: `wsgi.py`

### SSL Certificate
```bash
# Enable Let's Encrypt SSL
cloudpanel site:ssl:enable examreports.yourdomain.com
```

### Firewall Rules
```bash
# Allow HTTP/HTTPS traffic
ufw allow 80
ufw allow 443

# For VNC (if using Option 2)
ufw allow 5901
```

### Backup Configuration
```bash
# Setup automatic backups in CloudPanel
# Go to "Backups" → "Add Backup"
# Include: Database, Files, Logs
```

---

## 🚦 Testing Your Deployment

### Web Application Test
```bash
curl -I https://examreports.yourdomain.com
# Should return 200 OK
```

### Health Check Endpoint
```bash
curl https://examreports.yourdomain.com/health
# Should return JSON with status: healthy
```

---

## 📊 Monitoring & Logs

### CloudPanel Logs Location
```
/home/examreports/logs/
├── access.log
├── error.log
└── app.log
```

### Application Logs
```python
# In app.py, logs go to:
/home/examreports/logs/app.log
```

---

## 🔐 Security Considerations

1. **Environment Variables**
   ```bash
   # Set in CloudPanel environment settings
   SECRET_KEY=your_256_bit_secret_key
   FLASK_ENV=production
   ```

2. **File Permissions**
   ```bash
   chmod 644 app.py wsgi.py
   chmod 755 uploads reports
   ```

3. **Rate Limiting** (Optional)
   ```bash
   # Add nginx rate limiting in CloudPanel
   limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
   ```

---

## 📱 Mobile Responsive
The web version is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

## 🎯 Features Available in Web Version
- ✅ All Cambridge subjects (175+)
- ✅ Grade calculations
- ✅ PDF generation
- ✅ Professional reports
- ✅ Mobile responsive
- ✅ Real-time preview
- ✅ File downloads

## 🆘 Troubleshooting

### Common Issues:
1. **Permission Denied**
   ```bash
   chmod +x app.py wsgi.py
   chown -R examreports:examreports /home/examreports/htdocs/
   ```

2. **Module Not Found**
   ```bash
   pip install -r requirements_web.txt
   ```

3. **PDF Generation Fails**
   ```bash
   sudo apt install libcairo2-dev pkg-config python3-dev
   pip install --upgrade reportlab
   ```

Choose **Option 1 (Web Application)** for the best CloudPanel experience!