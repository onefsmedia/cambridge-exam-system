# SSH Setup Commands for VPS

Since SSH is not running, run these commands in your VPS terminal:

## 1. Check if SSH is installed
```bash
which sshd
```

## 2. Install SSH if not present
```bash
apt update
apt install openssh-server -y
```

## 3. Start SSH service
```bash
systemctl start ssh
systemctl enable ssh
```

## 4. Check SSH status
```bash
systemctl status ssh
```

## 5. Verify SSH is now listening
```bash
ss -tlnp | grep sshd
```

## 6. Check what port SSH is using
```bash
cat /etc/ssh/sshd_config | grep Port
```

## 7. Configure firewall to allow SSH
```bash
ufw allow ssh
ufw allow 22/tcp
```

## 8. If you want to use port 2222 instead
```bash
nano /etc/ssh/sshd_config
# Change #Port 22 to Port 2222
systemctl restart ssh
ufw allow 2222/tcp
```

Run these commands step by step and let me know the output!