#!/bin/bash

echo "🚀 Installing Advanced Supervisor AI Employee..."
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/opt/fueltheaura-ai"
SERVICE_NAME="advanced-supervisor.service"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Create installation directory if it doesn't exist
echo -e "${BLUE}📁 Setting up directories...${NC}"
mkdir -p $INSTALL_DIR
mkdir -p $INSTALL_DIR/data
mkdir -p $INSTALL_DIR/data/improvements
mkdir -p $INSTALL_DIR/data/supervisor_reports

# Copy Advanced Supervisor AI script
echo -e "${BLUE}📋 Installing Advanced Supervisor AI script...${NC}"
cp advanced_supervisor_ai.py $INSTALL_DIR/
chmod +x $INSTALL_DIR/advanced_supervisor_ai.py

# Install required Python packages
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip3 install --upgrade PyGithub beautifulsoup4 requests lxml

# Create systemd service
echo -e "${BLUE}⚙️  Creating systemd service...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME << EOF
[Unit]
Description=Advanced Supervisor AI Employee
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=$INSTALL_DIR/.env
ExecStart=/usr/bin/python3 $INSTALL_DIR/advanced_supervisor_ai.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo -e "${BLUE}🔄 Reloading systemd...${NC}"
systemctl daemon-reload

# Enable service
echo -e "${BLUE}✅ Enabling service...${NC}"
systemctl enable $SERVICE_NAME

# Start service
echo -e "${BLUE}🚀 Starting Advanced Supervisor AI...${NC}"
systemctl start $SERVICE_NAME

# Wait a moment for service to start
sleep 3

# Check status
echo ""
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo ""
echo "📊 Service Status:"
systemctl status $SERVICE_NAME --no-pager -l

echo ""
echo -e "${YELLOW}📝 Useful Commands:${NC}"
echo "  Check status:  sudo systemctl status $SERVICE_NAME"
echo "  View logs:     sudo journalctl -u $SERVICE_NAME -f"
echo "  Restart:       sudo systemctl restart $SERVICE_NAME"
echo "  Stop:          sudo systemctl stop $SERVICE_NAME"
echo ""
echo "📁 Reports Location: $INSTALL_DIR/data/supervisor_reports/"
echo "📁 Improvements: $INSTALL_DIR/data/improvements/"
echo ""
echo -e "${GREEN}🎉 Advanced Supervisor AI is now running!${NC}"
echo "   It will automatically:"
echo "   ✅ Update code from GitHub every 6 hours"
echo "   ✅ Analyze and improve SEO"
echo "   ✅ Optimize website performance"
echo "   ✅ Enhance design and UX"
echo "   ✅ Monitor content quality"
echo "   ✅ Implement automatic improvements"