# VPS SSH Diagnosis Commands

Run these commands in your VPS terminal to find the SSH port:

## 1. Check SSH service status
```bash
systemctl status ssh
```

## 2. Check what port SSH is listening on
```bash
netstat -tlnp | grep ssh
```

## 3. Check SSH configuration
```bash
cat /etc/ssh/sshd_config | grep -E "^Port|^#Port"
```

## 4. Check firewall status
```bash
ufw status
```

## 5. If SSH is not on standard port, check all listening ports
```bash
netstat -tlnp
```

## Quick one-liner to find SSH port:
```bash
ss -tlnp | grep sshd
```

Please run these commands and tell me what port SSH is listening on!