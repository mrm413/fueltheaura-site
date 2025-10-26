#!/bin/bash

echo "🔧 Fixing Advanced Supervisor AI Installation..."
echo "================================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

INSTALL_DIR="/opt/fueltheaura-ai"

echo -e "${BLUE}📦 Step 1: Installing Python dependencies with --break-system-packages...${NC}"
pip3 install --break-system-packages PyGithub beautifulsoup4 requests lxml

echo ""
echo -e "${BLUE}🔄 Step 2: Restarting Advanced Supervisor service...${NC}"
systemctl restart advanced-supervisor.service

echo ""
echo -e "${BLUE}⏳ Step 3: Waiting for service to start...${NC}"
sleep 5

echo ""
echo -e "${GREEN}✅ Checking service status...${NC}"
systemctl status advanced-supervisor.service --no-pager -l

echo ""
echo -e "${BLUE}📋 Step 4: Checking logs for errors...${NC}"
journalctl -u advanced-supervisor.service -n 20 --no-pager

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if service is running
if systemctl is-active --quiet advanced-supervisor.service; then
    echo -e "${GREEN}✅ SUCCESS! Advanced Supervisor AI is now running!${NC}"
    echo ""
    echo -e "${YELLOW}📊 Useful Commands:${NC}"
    echo "  View logs:     sudo journalctl -u advanced-supervisor.service -f"
    echo "  Check status:  sudo systemctl status advanced-supervisor.service"
    echo "  View reports:  ls -lth /opt/fueltheaura-ai/data/supervisor_reports/"
    echo ""
    echo -e "${GREEN}🎉 Your website is now self-improving 24/7!${NC}"
else
    echo -e "${RED}❌ Service is not running. Checking detailed logs...${NC}"
    echo ""
    journalctl -u advanced-supervisor.service -n 50 --no-pager
    echo ""
    echo -e "${YELLOW}💡 Troubleshooting:${NC}"
    echo "1. Check if all dependencies are installed:"
    echo "   pip3 list | grep -E 'PyGithub|beautifulsoup4|requests|lxml'"
    echo ""
    echo "2. Test the script manually:"
    echo "   cd /opt/fueltheaura-ai"
    echo "   python3 advanced_supervisor_ai.py"
    echo ""
    echo "3. Check for Python errors:"
    echo "   journalctl -u advanced-supervisor.service -n 100"
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"