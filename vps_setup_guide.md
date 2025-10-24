# VPS Initial Setup Guide

## Step 1: Login to your VPS
At the login prompt, enter your username (likely `root` or a user account you created during VPS setup).

```
srv819361 login: root
Password: [enter your password]
```

## Step 2: Check SSH Service Status
Once logged in, check if SSH is running:
```bash
systemctl status ssh
```

## Step 3: Enable SSH if needed
If SSH is not running, enable it:
```bash
systemctl enable ssh
systemctl start ssh
```

## Step 4: Check SSH Port Configuration
Check what port SSH is configured to use:
```bash
cat /etc/ssh/sshd_config | grep Port
```

## Step 5: Configure SSH Port (if needed)
If you need to change the SSH port to 2222:
```bash
nano /etc/ssh/sshd_config
```
Find the line `#Port 22` and change it to `Port 2222`, then restart SSH:
```bash
systemctl restart ssh
```

## Step 6: Check Firewall
Make sure the SSH port is open in the firewall:
```bash
ufw status
ufw allow 2222/tcp  # or whatever port SSH is using
ufw allow 22/tcp    # standard SSH port
```

## Step 7: Test SSH Connection
From another terminal (or your Windows machine), test the connection:
```bash
ssh -p 2222 root@82.25.93.227
# or
ssh -p 22 root@82.25.93.227
```

## Step 8: Once SSH is working, run our deployment
Once you can SSH in, our auto-deployment script should work!

## Common Issues and Solutions:

### If SSH port is different:
- CloudPanel often uses port 22 by default
- Some providers use port 2222 for security
- Check with: `netstat -tlnp | grep ssh`

### If you need to create a user:
```bash
adduser cambridgeexam
usermod -aG sudo cambridgeexam
```

### If you need to install git:
```bash
apt update
apt install git curl python3 python3-pip python3-venv
```

## Quick Commands Reference:
```bash
# Check what's listening on what ports
netstat -tlnp

# Check SSH service
systemctl status ssh

# Check firewall
ufw status

# Check if our domain resolves to this IP
nslookup cambridgeexam.dobeda.com
```