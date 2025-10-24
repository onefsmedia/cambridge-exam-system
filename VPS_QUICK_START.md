# Cambridge Exam System - VPS Deployment

## 🌐 For CloudPanel Users

### Quick Deploy (Recommended)
```bash
# SSH into your VPS
ssh root@your_vps_ip

# Run auto-deployment script
wget https://raw.githubusercontent.com/onefsmedia/cambridge-exam-system/main/deploy_vps.sh
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### Manual CloudPanel Setup

1. **Create Python Site**
   - Domain: `examreports.yourdomain.com`
   - Python Version: 3.11
   - Document Root: `/public`

2. **Upload Files**
   ```bash
   cd /home/examreports/htdocs/examreports.yourdomain.com
   git clone https://github.com/onefsmedia/cambridge-exam-system.git .
   pip install -r requirements_web.txt
   ```

3. **Configure Reverse Proxy**
   In CloudPanel → Sites → examreports.yourdomain.com → Vhost:
   ```nginx
   location / {
       proxy_pass http://127.0.0.1:5000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

## 🖥️ Alternative: VNC Desktop Version

For the full GUI experience:

```bash
# Install VNC
sudo apt install -y xfce4 tightvncserver

# Set VNC password
vncpasswd

# Start VNC server
vncserver :1 -geometry 1280x800

# Connect with VNC viewer to: your_vps_ip:5901
```

## 🐳 Docker Option

```bash
# Build and run
git clone https://github.com/onefsmedia/cambridge-exam-system.git
cd cambridge-exam-system
docker build -t cambridge-exam .
docker run -d -p 5000:5000 cambridge-exam
```

## 🔧 Service Management

```bash
# Check status
systemctl status cambridge-exam

# View logs
journalctl -u cambridge-exam -f

# Restart service
systemctl restart cambridge-exam
```

Access your application at: **https://examreports.yourdomain.com**