#!/bin/bash

# Complete AI Employee Installation Script
# Installs Auditor, Supervisor, Analyst, and Reporter AI employees

echo "🤖 FuelTheAura AI Employee Installation"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

cd /opt/fueltheaura-ai

echo "📦 Step 1: Installing AI Employee Scripts"
echo "-----------------------------------------"

# Download AI employee scripts from GitHub
echo "Downloading Auditor AI..."
curl -O https://raw.githubusercontent.com/mrm413/fueltheaura-site/main/enhancements/auditor_ai.py
chmod +x auditor_ai.py

echo "Downloading Supervisor AI..."
curl -O https://raw.githubusercontent.com/mrm413/fueltheaura-site/main/enhancements/supervisor_ai.py
chmod +x supervisor_ai.py

echo "Downloading Analyst AI..."
curl -O https://raw.githubusercontent.com/mrm413/fueltheaura-site/main/enhancements/analyst_ai.py
chmod +x analyst_ai.py

echo "Downloading Reporter AI..."
curl -O https://raw.githubusercontent.com/mrm413/fueltheaura-site/main/enhancements/reporter_ai.py
chmod +x reporter_ai.py

echo "✅ AI employee scripts downloaded"
echo ""

echo "📁 Step 2: Creating Data Directories"
echo "------------------------------------"
mkdir -p data/audits
mkdir -p data/supervisor_reports
mkdir -p data/analyst_reports
mkdir -p data/reports
mkdir -p backups
echo "✅ Directories created"
echo ""

echo "🔧 Step 3: Installing Python Dependencies"
echo "-----------------------------------------"
source ai-venv/bin/activate
pip install requests beautifulsoup4 lxml
echo "✅ Dependencies installed"
echo ""

echo "⚙️  Step 4: Creating Systemd Services"
echo "-------------------------------------"

# Create Auditor AI service
cat > /etc/systemd/system/auditor-ai.service << 'EOF'
[Unit]
Description=Auditor AI Employee
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/fueltheaura-ai
Environment="PATH=/opt/fueltheaura-ai/ai-venv/bin"
ExecStart=/opt/fueltheaura-ai/ai-venv/bin/python3 /opt/fueltheaura-ai/auditor_ai.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

# Create Supervisor AI service
cat > /etc/systemd/system/supervisor-ai.service << 'EOF'
[Unit]
Description=Supervisor AI Employee
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/fueltheaura-ai
Environment="PATH=/opt/fueltheaura-ai/ai-venv/bin"
ExecStart=/opt/fueltheaura-ai/ai-venv/bin/python3 /opt/fueltheaura-ai/supervisor_ai.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

# Create Analyst AI service
cat > /etc/systemd/system/analyst-ai.service << 'EOF'
[Unit]
Description=Analyst AI Employee
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/fueltheaura-ai
Environment="PATH=/opt/fueltheaura-ai/ai-venv/bin"
ExecStart=/opt/fueltheaura-ai/ai-venv/bin/python3 /opt/fueltheaura-ai/analyst_ai.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

# Create Reporter AI service
cat > /etc/systemd/system/reporter-ai.service << 'EOF'
[Unit]
Description=Reporter AI Employee
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/fueltheaura-ai
Environment="PATH=/opt/fueltheaura-ai/ai-venv/bin"
ExecStart=/opt/fueltheaura-ai/ai-venv/bin/python3 /opt/fueltheaura-ai/reporter_ai.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd services created"
echo ""

echo "🚀 Step 5: Starting AI Employees"
echo "--------------------------------"

# Reload systemd
systemctl daemon-reload

# Enable and start services
systemctl enable auditor-ai.service
systemctl start auditor-ai.service
echo "✅ Auditor AI started"

systemctl enable supervisor-ai.service
systemctl start supervisor-ai.service
echo "✅ Supervisor AI started"

systemctl enable analyst-ai.service
systemctl start analyst-ai.service
echo "✅ Analyst AI started"

systemctl enable reporter-ai.service
systemctl start reporter-ai.service
echo "✅ Reporter AI started"

echo ""
echo "✅ INSTALLATION COMPLETE!"
echo "========================"
echo ""
echo "📊 AI Employee Status:"
echo "---------------------"
systemctl status auditor-ai.service --no-pager | grep Active
systemctl status supervisor-ai.service --no-pager | grep Active
systemctl status analyst-ai.service --no-pager | grep Active
systemctl status reporter-ai.service --no-pager | grep Active

echo ""
echo "💡 Useful Commands:"
echo "------------------"
echo "Check status:     systemctl status [service-name]"
echo "View logs:        journalctl -u [service-name] -f"
echo "Restart service:  systemctl restart [service-name]"
echo "Stop service:     systemctl stop [service-name]"
echo ""
echo "📁 Data Locations:"
echo "-----------------"
echo "Audits:           /opt/fueltheaura-ai/data/audits/"
echo "Supervisor:       /opt/fueltheaura-ai/data/supervisor_reports/"
echo "Analyst:          /opt/fueltheaura-ai/data/analyst_reports/"
echo "Reports:          /opt/fueltheaura-ai/data/reports/"
echo "Backups:          /opt/fueltheaura-ai/backups/"
echo ""
echo "🎉 Your AI employee team is now operational!"