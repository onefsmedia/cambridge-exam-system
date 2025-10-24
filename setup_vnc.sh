#!/bin/bash
# VNC Setup Script for running GUI applications on VPS
# This allows you to run the desktop version remotely

echo "🖥️  Setting up VNC for Cambridge Exam System..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install desktop environment (lightweight)
sudo apt install -y xfce4 xfce4-goodies

# Install VNC server
sudo apt install -y tightvncserver

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv

# Install system dependencies for GUI
sudo apt install -y python3-tk

# Create application directory
mkdir -p ~/cambridge_exam_system
cd ~/cambridge_exam_system

# Clone your repository
git clone https://github.com/onefsmedia/cambridge-exam-system.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create VNC startup script
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &
EOF

chmod +x ~/.vnc/xstartup

# Create systemd service for VNC
sudo tee /etc/systemd/system/vncserver@.service << 'EOF'
[Unit]
Description=Start TightVNC server at startup
After=syslog.target network.target

[Service]
Type=forking
User=cambridge
Group=cambridge
WorkingDirectory=/home/cambridge

PIDFile=/home/cambridge/.vnc/%H:%i.pid
ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 :%i
ExecStop=/usr/bin/vncserver -kill :%i

[Install]
WantedBy=multi-user.target
EOF

echo "✅ VNC setup complete!"
echo "📝 Next steps:"
echo "1. Set VNC password: vncpasswd"
echo "2. Start VNC: vncserver :1"
echo "3. Connect to your_vps_ip:5901"
echo "4. Run: python main_gui_complete.py"