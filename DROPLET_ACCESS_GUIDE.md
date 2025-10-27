# DigitalOcean Droplet Access Guide - FuelTheAura AI System

**Last Updated:** 2024-01-XX  
**Droplet Location:** DigitalOcean  
**System:** Ubuntu Linux  

---

## Table of Contents

1. [Accessing Your Droplet](#1-accessing-your-droplet)
2. [Checking AI Employee Status](#2-checking-ai-employee-status)
3. [Viewing Logs](#3-viewing-logs)
4. [Managing Services](#4-managing-services)
5. [Database Access](#5-database-access)
6. [File System Navigation](#6-file-system-navigation)
7. [Troubleshooting](#7-troubleshooting)
8. [Common Commands Reference](#8-common-commands-reference)

---

## 1. Accessing Your Droplet

### 1.1 Using PowerShell (Windows)

**Step 1: Open PowerShell**
- Press `Windows Key + X`
- Select "Windows PowerShell" or "Terminal"

**Step 2: Connect via SSH**

```powershell
# Basic SSH connection
ssh root@YOUR_DROPLET_IP

# Example:
ssh root@164.90.XXX.XXX
```

**Step 3: Enter Password**
- Type your root password (characters won't show while typing)
- Press Enter

**Alternative: Using SSH Key (More Secure)**

```powershell
# If you have an SSH key configured
ssh -i C:\Users\YourUsername\.ssh\id_rsa root@YOUR_DROPLET_IP
```

### 1.2 Using PuTTY (Alternative for Windows)

**Step 1: Download PuTTY**
- Download from: https://www.putty.org/

**Step 2: Configure Connection**
- Host Name: `YOUR_DROPLET_IP`
- Port: `22`
- Connection Type: `SSH`
- Click "Open"

**Step 3: Login**
- Username: `root`
- Password: `YOUR_PASSWORD`

### 1.3 First Time Connection

When connecting for the first time, you'll see:

```
The authenticity of host 'XXX.XXX.XXX.XXX' can't be established.
ECDSA key fingerprint is SHA256:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Are you sure you want to continue connecting (yes/no)?
```

**Type:** `yes` and press Enter

---

## 2. Checking AI Employee Status

### 2.1 Check All Services at Once

```bash
# Quick status check of all AI employees
systemctl status fueltheaura-ai.service --no-pager | grep Active
systemctl status health-scraper.service --no-pager | grep Active
systemctl status ai-learning.service --no-pager | grep Active
systemctl status advanced-supervisor.service --no-pager | grep Active
systemctl status auditor-ai.service --no-pager | grep Active
systemctl status supervisor-ai.service --no-pager | grep Active
systemctl status analyst-ai.service --no-pager | grep Active
systemctl status reporter-ai.service --no-pager | grep Active
```

**Expected Output:**
```
Active: active (running) since Mon 2024-01-XX 10:30:00 UTC; 2 days ago
Active: active (running) since Mon 2024-01-XX 10:30:00 UTC; 2 days ago
...
```

### 2.2 Detailed Status Check

```bash
# Check individual service with full details
systemctl status advanced-supervisor.service

# This shows:
# - Service status (active/inactive/failed)
# - Process ID (PID)
# - Memory usage
# - Recent log entries
# - Uptime
```

### 2.3 Check if Services are Enabled (Auto-start on boot)

```bash
# Check if services start automatically on boot
systemctl is-enabled advanced-supervisor.service
systemctl is-enabled auditor-ai.service
systemctl is-enabled analyst-ai.service
systemctl is-enabled reporter-ai.service

# Expected output: "enabled"
```

---

## 3. Viewing Logs

### 3.1 Real-Time Log Viewing (Live Tail)

```bash
# View Advanced Supervisor logs in real-time
journalctl -u advanced-supervisor.service -f

# Press Ctrl+C to stop viewing
```

**What you'll see:**
```
Jan XX 10:30:00 droplet python3[12345]: 🤖 Advanced Supervisor AI - 2024-01-XX 10:30:00
Jan XX 10:30:01 droplet python3[12345]: 🔄 Auto-updating code from GitHub...
Jan XX 10:30:05 droplet python3[12345]: ✅ Code update: up_to_date
```

### 3.2 View Recent Logs (Last 100 Lines)

```bash
# View last 100 log entries
journalctl -u advanced-supervisor.service -n 100

# View last 50 entries
journalctl -u advanced-supervisor.service -n 50
```

### 3.3 View Logs from Specific Time Period

```bash
# Logs from today
journalctl -u advanced-supervisor.service --since today

# Logs from last hour
journalctl -u advanced-supervisor.service --since "1 hour ago"

# Logs from specific date
journalctl -u advanced-supervisor.service --since "2024-01-15"

# Logs between two dates
journalctl -u advanced-supervisor.service --since "2024-01-15" --until "2024-01-16"
```

### 3.4 View Logs for All AI Employees

```bash
# View logs from multiple services
journalctl -u advanced-supervisor.service -u auditor-ai.service -u analyst-ai.service -f
```

### 3.5 Search Logs for Specific Terms

```bash
# Search for errors
journalctl -u advanced-supervisor.service | grep -i error

# Search for specific keyword
journalctl -u advanced-supervisor.service | grep -i "improvement"

# Count occurrences
journalctl -u advanced-supervisor.service | grep -c "success"
```

---

## 4. Managing Services

### 4.1 Starting Services

```bash
# Start a service
sudo systemctl start advanced-supervisor.service

# Start multiple services
sudo systemctl start auditor-ai.service analyst-ai.service
```

### 4.2 Stopping Services

```bash
# Stop a service
sudo systemctl stop advanced-supervisor.service

# Stop all AI employees
sudo systemctl stop advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

### 4.3 Restarting Services

```bash
# Restart a service (useful after code updates)
sudo systemctl restart advanced-supervisor.service

# Restart all AI employees
sudo systemctl restart advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

### 4.4 Enabling/Disabling Auto-Start

```bash
# Enable service to start on boot
sudo systemctl enable advanced-supervisor.service

# Disable service from starting on boot
sudo systemctl disable advanced-supervisor.service
```

### 4.5 Reload Systemd Configuration

```bash
# After modifying service files, reload systemd
sudo systemctl daemon-reload
```

---

## 5. Database Access

### 5.1 Navigate to Data Directory

```bash
# Go to AI data directory
cd /opt/fueltheaura-ai/data

# List all databases
ls -lh *.db
```

**Expected Output:**
```
-rw-r--r-- 1 root root 2.5M Jan XX 10:30 content_intelligence.db
-rw-r--r-- 1 root root 15M  Jan XX 10:30 health_content.db
-rw-r--r-- 1 root root 1.2M Jan XX 10:30 ai_learning.db
-rw-r--r-- 1 root root 856K Jan XX 10:30 supervisor_improvements.db
```

### 5.2 Access SQLite Databases

```bash
# Open supervisor improvements database
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db

# Once inside SQLite prompt:
```

**SQLite Commands:**

```sql
-- List all tables
.tables

-- View table structure
.schema improvements

-- View recent improvements
SELECT * FROM improvements ORDER BY timestamp DESC LIMIT 10;

-- Count total improvements
SELECT COUNT(*) FROM improvements;

-- View improvements by category
SELECT category, COUNT(*) as count 
FROM improvements 
GROUP BY category 
ORDER BY count DESC;

-- View high-impact improvements
SELECT * FROM improvements 
WHERE impact_score > 0.8 
ORDER BY timestamp DESC 
LIMIT 20;

-- Exit SQLite
.quit
```

### 5.3 Export Database Data

```bash
# Export improvements to CSV
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db \
  "SELECT * FROM improvements;" \
  -csv -header > improvements_export.csv

# Export to JSON
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db \
  "SELECT json_object('timestamp', timestamp, 'category', category, 'description', description) 
   FROM improvements LIMIT 100;" > improvements.json
```

### 5.4 Database Backup

```bash
# Manual backup of all databases
cd /opt/fueltheaura-ai/data
cp *.db /opt/fueltheaura-ai/backups/manual_backup_$(date +%Y%m%d_%H%M%S)/

# Verify backup
ls -lh /opt/fueltheaura-ai/backups/
```

---

## 6. File System Navigation

### 6.1 Directory Structure

```bash
# View complete directory structure
cd /opt/fueltheaura-ai
tree -L 2

# Or use ls for basic view
ls -la
```

**Key Directories:**

```
/opt/fueltheaura-ai/
├── advanced_supervisor_ai.py      # Advanced Supervisor script
├── auditor_ai.py                  # Auditor AI script
├── analyst_ai.py                  # Analyst AI script
├── reporter_ai.py                 # Reporter AI script
├── supervisor_ai.py               # Supervisor AI script
├── ai-venv/                       # Python virtual environment
├── data/                          # All data and databases
│   ├── audits/                    # Audit reports
│   ├── supervisor_reports/        # Supervisor reports
│   ├── analyst_reports/           # Analyst reports
│   ├── reports/                   # General reports
│   ├── improvements/              # Improvement logs
│   ├── *.db                       # SQLite databases
├── backups/                       # Database backups
└── logs/                          # Log files
```

### 6.2 View Recent Reports

```bash
# View latest supervisor reports
ls -lth /opt/fueltheaura-ai/data/supervisor_reports/ | head -10

# View latest audit reports
ls -lth /opt/fueltheaura-ai/data/audits/ | head -10

# View latest analyst reports
ls -lth /opt/fueltheaura-ai/data/analyst_reports/ | head -10

# View latest general reports
ls -lth /opt/fueltheaura-ai/data/reports/ | head -10
```

### 6.3 Read Report Files

```bash
# View latest supervisor report
cat /opt/fueltheaura-ai/data/supervisor_reports/$(ls -t /opt/fueltheaura-ai/data/supervisor_reports/ | head -1)

# View with pretty formatting (if jq is installed)
cat /opt/fueltheaura-ai/data/supervisor_reports/$(ls -t /opt/fueltheaura-ai/data/supervisor_reports/ | head -1) | jq .

# View specific sections
cat /opt/fueltheaura-ai/data/supervisor_reports/$(ls -t /opt/fueltheaura-ai/data/supervisor_reports/ | head -1) | jq '.improvement_summary'
```

### 6.4 Check Disk Space

```bash
# Check overall disk usage
df -h

# Check AI directory size
du -sh /opt/fueltheaura-ai

# Check size of each subdirectory
du -sh /opt/fueltheaura-ai/*

# Check database sizes
du -sh /opt/fueltheaura-ai/data/*.db
```

---

## 7. Troubleshooting

### 7.1 Service Won't Start

**Problem:** Service fails to start

**Solution:**

```bash
# Check service status for error messages
systemctl status advanced-supervisor.service

# View detailed logs
journalctl -u advanced-supervisor.service -n 50

# Check if Python script has syntax errors
cd /opt/fueltheaura-ai
source ai-venv/bin/activate
python3 advanced_supervisor_ai.py

# Check file permissions
ls -la /opt/fueltheaura-ai/*.py

# Fix permissions if needed
chmod +x /opt/fueltheaura-ai/*.py
```

### 7.2 Service Keeps Restarting

**Problem:** Service restarts repeatedly

**Solution:**

```bash
# View restart history
journalctl -u advanced-supervisor.service | grep -i restart

# Check for errors in logs
journalctl -u advanced-supervisor.service | grep -i error

# Check system resources
top
htop  # If installed

# Check memory usage
free -h

# Check if database is locked
lsof /opt/fueltheaura-ai/data/*.db
```

### 7.3 Database Errors

**Problem:** Database locked or corrupted

**Solution:**

```bash
# Check database integrity
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "PRAGMA integrity_check;"

# If corrupted, restore from backup
cd /opt/fueltheaura-ai/backups
ls -lth | head -5  # Find recent backup
cp backup_folder/*.db /opt/fueltheaura-ai/data/

# Restart services
sudo systemctl restart advanced-supervisor.service
```

### 7.4 Disk Space Full

**Problem:** No space left on device

**Solution:**

```bash
# Find large files
find /opt/fueltheaura-ai -type f -size +100M -exec ls -lh {} \;

# Clean old logs
journalctl --vacuum-time=7d

# Clean old backups (keep last 7 days)
find /opt/fueltheaura-ai/backups -type f -mtime +7 -delete

# Clean old reports (keep last 30 days)
find /opt/fueltheaura-ai/data/*/reports -type f -mtime +30 -delete
```

### 7.5 GitHub Update Failures

**Problem:** Can't pull from GitHub

**Solution:**

```bash
# Check GitHub token
echo $GITHUB_TOKEN

# If empty, set it
export GITHUB_TOKEN="your_github_token_here"

# Test GitHub connection
cd /opt/fueltheaura-ai
git pull origin main

# If authentication fails, reconfigure
git config --global credential.helper store
git pull origin main  # Enter credentials when prompted
```

### 7.6 Python Dependencies Missing

**Problem:** Import errors in logs

**Solution:**

```bash
# Activate virtual environment
cd /opt/fueltheaura-ai
source ai-venv/bin/activate

# Install missing dependencies
pip install requests beautifulsoup4 lxml PyGithub

# Or reinstall all requirements
pip install -r requirements.txt

# Restart services
sudo systemctl restart advanced-supervisor.service
```

---

## 8. Common Commands Reference

### 8.1 Quick Status Check

```bash
# One-liner to check all services
for service in fueltheaura-ai health-scraper ai-learning advanced-supervisor auditor-ai supervisor-ai analyst-ai reporter-ai; do 
  echo "=== $service ===" 
  systemctl is-active $service.service
done
```

### 8.2 View All Recent Activity

```bash
# Last hour of activity across all services
journalctl --since "1 hour ago" | grep -E "(advanced-supervisor|auditor-ai|analyst-ai|reporter-ai)"
```

### 8.3 Generate Quick Report

```bash
# Create a quick status report
cat << EOF > /tmp/ai_status_report.txt
FuelTheAura AI Status Report
Generated: $(date)
========================================

Service Status:
$(systemctl status advanced-supervisor.service --no-pager | grep Active)
$(systemctl status auditor-ai.service --no-pager | grep Active)
$(systemctl status analyst-ai.service --no-pager | grep Active)
$(systemctl status reporter-ai.service --no-pager | grep Active)

Disk Usage:
$(df -h /opt/fueltheaura-ai)

Database Sizes:
$(du -sh /opt/fueltheaura-ai/data/*.db)

Recent Improvements:
$(sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "SELECT COUNT(*) FROM improvements WHERE timestamp > datetime('now', '-24 hours');")

EOF

cat /tmp/ai_status_report.txt
```

### 8.4 Restart All AI Employees

```bash
# Restart all services at once
sudo systemctl restart advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service supervisor-ai.service

# Verify all started successfully
sleep 5
for service in advanced-supervisor auditor-ai analyst-ai reporter-ai supervisor-ai; do
  systemctl is-active $service.service
done
```

### 8.5 View System Resources

```bash
# CPU and Memory usage
top -bn1 | head -20

# Or with htop (more user-friendly)
htop

# Disk I/O
iostat -x 1 5

# Network usage
iftop  # If installed
```

---

## 9. Maintenance Tasks

### 9.1 Weekly Maintenance

```bash
# Run these commands weekly

# 1. Check service health
systemctl status advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service

# 2. Review logs for errors
journalctl --since "7 days ago" | grep -i error

# 3. Check disk space
df -h

# 4. Verify backups exist
ls -lth /opt/fueltheaura-ai/backups/ | head -10

# 5. Check database integrity
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "PRAGMA integrity_check;"
```

### 9.2 Monthly Maintenance

```bash
# Run these commands monthly

# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Clean old logs
journalctl --vacuum-time=30d

# 3. Clean old reports (keep 60 days)
find /opt/fueltheaura-ai/data -name "*.json" -mtime +60 -delete

# 4. Optimize databases
for db in /opt/fueltheaura-ai/data/*.db; do
  sqlite3 "$db" "VACUUM;"
done

# 5. Review improvement statistics
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db \
  "SELECT category, COUNT(*) as count, AVG(impact_score) as avg_impact 
   FROM improvements 
   WHERE timestamp > datetime('now', '-30 days') 
   GROUP BY category;"
```

---

## 10. Emergency Procedures

### 10.1 Complete System Restart

```bash
# If everything seems broken, restart all services

# Stop all services
sudo systemctl stop advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service supervisor-ai.service

# Wait 10 seconds
sleep 10

# Start all services
sudo systemctl start advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service supervisor-ai.service

# Check status
systemctl status advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

### 10.2 Restore from Backup

```bash
# If databases are corrupted

# 1. Stop all services
sudo systemctl stop advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service

# 2. Backup current (corrupted) databases
mkdir -p /opt/fueltheaura-ai/corrupted_backup_$(date +%Y%m%d)
cp /opt/fueltheaura-ai/data/*.db /opt/fueltheaura-ai/corrupted_backup_$(date +%Y%m%d)/

# 3. Find latest good backup
ls -lth /opt/fueltheaura-ai/backups/ | head -5

# 4. Restore from backup
cp /opt/fueltheaura-ai/backups/BACKUP_FOLDER/*.db /opt/fueltheaura-ai/data/

# 5. Restart services
sudo systemctl start advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service

# 6. Verify
systemctl status advanced-supervisor.service
```

### 10.3 Complete Reinstallation

```bash
# Nuclear option - reinstall everything

# 1. Backup data
mkdir -p /root/fueltheaura_backup_$(date +%Y%m%d)
cp -r /opt/fueltheaura-ai/data /root/fueltheaura_backup_$(date +%Y%m%d)/

# 2. Stop and disable services
sudo systemctl stop advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
sudo systemctl disable advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service

# 3. Remove old installation
rm -rf /opt/fueltheaura-ai

# 4. Clone fresh from GitHub
cd /opt
git clone https://github.com/mrm413/fueltheaura-site.git fueltheaura-ai

# 5. Run installation scripts
cd /opt/fueltheaura-ai
bash install_advanced_supervisor.sh
bash enhancements/install_all_ai_employees.sh

# 6. Restore data
cp -r /root/fueltheaura_backup_$(date +%Y%m%d)/data/* /opt/fueltheaura-ai/data/

# 7. Start services
sudo systemctl start advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

---

## 11. Getting Help

### 11.1 Check Documentation

```bash
# View README files
cat /opt/fueltheaura-ai/README.md
cat /opt/fueltheaura-ai/ADVANCED_SUPERVISOR_GUIDE.md
cat /opt/fueltheaura-ai/QUICK_START_ADVANCED_SUPERVISOR.md
```

### 11.2 Generate Debug Report

```bash
# Create comprehensive debug report
bash << 'EOF' > /tmp/debug_report.txt
echo "FuelTheAura AI Debug Report"
echo "Generated: $(date)"
echo "========================================"
echo ""
echo "=== System Info ==="
uname -a
echo ""
echo "=== Disk Space ==="
df -h
echo ""
echo "=== Memory ==="
free -h
echo ""
echo "=== Service Status ==="
systemctl status advanced-supervisor.service --no-pager
systemctl status auditor-ai.service --no-pager
systemctl status analyst-ai.service --no-pager
systemctl status reporter-ai.service --no-pager
echo ""
echo "=== Recent Errors ==="
journalctl --since "24 hours ago" | grep -i error | tail -20
echo ""
echo "=== Database Sizes ==="
du -sh /opt/fueltheaura-ai/data/*.db
echo ""
echo "=== Recent Improvements ==="
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db \
  "SELECT * FROM improvements ORDER BY timestamp DESC LIMIT 5;"
EOF

cat /tmp/debug_report.txt
```

---

## 12. Best Practices

### 12.1 Regular Checks (Daily)

```bash
# Quick daily health check (2 minutes)
systemctl status advanced-supervisor.service --no-pager | grep Active
df -h | grep /opt
journalctl -u advanced-supervisor.service --since "24 hours ago" | grep -i error
```

### 12.2 Security

```bash
# Change root password regularly
passwd

# Check for unauthorized access
last -20

# Review active connections
netstat -tulpn

# Check for suspicious processes
ps aux | grep -v root
```

### 12.3 Performance Monitoring

```bash
# Monitor system load
uptime

# Check process resource usage
ps aux --sort=-%mem | head -10
ps aux --sort=-%cpu | head -10

# Monitor in real-time
watch -n 5 'systemctl status advanced-supervisor.service --no-pager | grep -E "(Active|Memory|CPU)"'
```

---

## Quick Reference Card

**Connect to Droplet:**
```bash
ssh root@YOUR_DROPLET_IP
```

**Check All Services:**
```bash
systemctl status advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

**View Live Logs:**
```bash
journalctl -u advanced-supervisor.service -f
```

**Restart Service:**
```bash
sudo systemctl restart advanced-supervisor.service
```

**Check Disk Space:**
```bash
df -h
```

**View Recent Reports:**
```bash
ls -lth /opt/fueltheaura-ai/data/supervisor_reports/ | head -5
```

**Access Database:**
```bash
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db
```

**Emergency Restart All:**
```bash
sudo systemctl restart advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

---

**Need More Help?**
- Review the Comprehensive Audit Report
- Check GitHub repository documentation
- Contact your development team

**Remember:** Always backup before making major changes!