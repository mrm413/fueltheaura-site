# Quick Start Commands - FuelTheAura AI System

**For:** Windows PowerShell Access to DigitalOcean Droplet

---

## 🚀 Step 1: Connect to Your Droplet

```powershell
# Open PowerShell (Windows Key + X, then select "Windows PowerShell")
ssh root@YOUR_DROPLET_IP

# Example:
ssh root@164.90.XXX.XXX

# Enter your password when prompted (characters won't show while typing)
```

**First time?** Type `yes` when asked about authenticity.

---

## ✅ Step 2: Check Everything is Running

```bash
# Quick status check - Copy and paste this entire block:
echo "=== FuelTheAura AI Status Check ==="
echo ""
echo "Advanced Supervisor AI:"
systemctl is-active advanced-supervisor.service
echo ""
echo "Auditor AI:"
systemctl is-active auditor-ai.service
echo ""
echo "Analyst AI:"
systemctl is-active analyst-ai.service
echo ""
echo "Reporter AI:"
systemctl is-active reporter-ai.service
echo ""
echo "All services should show: active"
```

**Expected Output:** All services showing `active`

---

## 📊 Step 3: View Recent Activity

```bash
# See what Advanced Supervisor is doing right now:
journalctl -u advanced-supervisor.service -n 50

# See live updates (press Ctrl+C to stop):
journalctl -u advanced-supervisor.service -f
```

---

## 📈 Step 4: Check Recent Improvements

```bash
# View latest improvement reports:
ls -lth /opt/fueltheaura-ai/data/supervisor_reports/ | head -5

# Read the most recent report:
cat /opt/fueltheaura-ai/data/supervisor_reports/$(ls -t /opt/fueltheaura-ai/data/supervisor_reports/ | head -1)
```

---

## 💾 Step 5: Check Database Statistics

```bash
# Access the improvements database:
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db

# Once inside SQLite, run these commands:
```

```sql
-- See total improvements made:
SELECT COUNT(*) as total_improvements FROM improvements;

-- See improvements by category:
SELECT category, COUNT(*) as count 
FROM improvements 
GROUP BY category 
ORDER BY count DESC;

-- See recent high-impact improvements:
SELECT timestamp, category, description, impact_score 
FROM improvements 
WHERE impact_score > 0.7 
ORDER BY timestamp DESC 
LIMIT 10;

-- Exit SQLite:
.quit
```

---

## 🔄 Step 6: Restart a Service (If Needed)

```bash
# Restart Advanced Supervisor:
sudo systemctl restart advanced-supervisor.service

# Check it started successfully:
systemctl status advanced-supervisor.service

# Restart all AI employees:
sudo systemctl restart advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

---

## 💽 Step 7: Check Disk Space

```bash
# Check available disk space:
df -h

# Check AI directory size:
du -sh /opt/fueltheaura-ai

# Check database sizes:
du -sh /opt/fueltheaura-ai/data/*.db
```

---

## 📝 Step 8: View Logs for Errors

```bash
# Check for any errors in the last 24 hours:
journalctl -u advanced-supervisor.service --since "24 hours ago" | grep -i error

# Check all AI employees for errors:
journalctl --since "24 hours ago" | grep -i error | grep -E "(advanced-supervisor|auditor-ai|analyst-ai|reporter-ai)"
```

---

## 🎯 Common Tasks

### View All Service Status at Once

```bash
for service in advanced-supervisor auditor-ai analyst-ai reporter-ai supervisor-ai; do 
  echo "=== $service ===" 
  systemctl is-active $service.service
  echo ""
done
```

### Generate Quick Status Report

```bash
cat << 'EOF' > /tmp/status.txt
FuelTheAura AI Status Report
Generated: $(date)
========================================

Services:
$(systemctl is-active advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service)

Disk Space:
$(df -h | grep -E "(Filesystem|/dev/vda)")

Recent Improvements (24h):
$(sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "SELECT COUNT(*) FROM improvements WHERE timestamp > datetime('now', '-24 hours');")

Latest Reports:
$(ls -lt /opt/fueltheaura-ai/data/supervisor_reports/ | head -3)
EOF

cat /tmp/status.txt
```

### View Latest Audit Results

```bash
# See latest audit report:
cat /opt/fueltheaura-ai/data/audits/$(ls -t /opt/fueltheaura-ai/data/audits/ | head -1)
```

### View Latest Analyst Report

```bash
# See latest content analysis:
cat /opt/fueltheaura-ai/data/analyst_reports/$(ls -t /opt/fueltheaura-ai/data/analyst_reports/ | head -1)
```

---

## 🆘 Emergency Commands

### Everything Seems Broken - Restart All

```bash
# Stop all services:
sudo systemctl stop advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service

# Wait 10 seconds:
sleep 10

# Start all services:
sudo systemctl start advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service

# Check status:
systemctl status advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service
```

### Check System Resources

```bash
# CPU and Memory:
top -bn1 | head -20

# Or press 'q' to quit after viewing:
htop

# Disk I/O:
iostat -x 1 5
```

### View System Uptime

```bash
uptime
```

---

## 📱 One-Liner Commands (Copy & Paste)

**Quick Health Check:**
```bash
echo "Services:" && systemctl is-active advanced-supervisor.service auditor-ai.service analyst-ai.service reporter-ai.service && echo "" && echo "Disk:" && df -h | grep vda && echo "" && echo "Memory:" && free -h
```

**Count Improvements Today:**
```bash
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "SELECT COUNT(*) as improvements_today FROM improvements WHERE date(timestamp) = date('now');"
```

**View Last 10 Improvements:**
```bash
sqlite3 /opt/fueltheaura-ai/data/supervisor_improvements.db "SELECT timestamp, category, description FROM improvements ORDER BY timestamp DESC LIMIT 10;"
```

**Check Website Status:**
```bash
curl -I https://fueltheaura.com | head -1
```

---

## 🎓 Pro Tips

1. **Use Tab Completion:** Start typing a command and press Tab to auto-complete
2. **Use Up Arrow:** Press up arrow to recall previous commands
3. **Use Ctrl+C:** Stop any running command
4. **Use Ctrl+L:** Clear the screen
5. **Use `history`:** See all your previous commands

---

## 📚 Where to Find More Information

- **Detailed Guide:** Read `DROPLET_ACCESS_GUIDE.md`
- **Full Audit:** Read `COMPREHENSIVE_AUDIT_REPORT.md`
- **Overview:** Read `EXECUTIVE_SUMMARY.md`

---

## 🔐 Security Reminder

- Never share your droplet IP or password
- Change your password regularly: `passwd`
- Review login history: `last -20`
- Check active connections: `netstat -tulpn`

---

## ✨ You're All Set!

Your AI employees are working 24/7 to improve your website. Check in weekly to see the improvements!

**Questions?** Refer to the detailed guides or contact your development team.

---

**Happy Monitoring! 🚀**