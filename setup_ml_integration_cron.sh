#!/bin/bash

echo "🔧 Setting up ML Insights Integration Cron Job..."
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
WEBSITE_DIR="/workspace/fueltheaura-site"
SCRIPT_PATH="$WEBSITE_DIR/ml_insights_integration.py"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Verify script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Integration script not found at $SCRIPT_PATH"
    exit 1
fi

# Create cron job
echo -e "${BLUE}📅 Creating cron job...${NC}"

# Add cron job to run every hour
(crontab -l 2>/dev/null; echo "0 * * * * cd $WEBSITE_DIR && /usr/bin/python3 ml_insights_integration.py >> /var/log/ml-integration.log 2>&1") | crontab -

echo -e "${GREEN}✅ Cron job created!${NC}"
echo ""
echo "📋 Current crontab:"
crontab -l | grep ml_insights_integration

echo ""
echo -e "${YELLOW}📝 Details:${NC}"
echo "  Schedule: Every hour (at minute 0)"
echo "  Script: $SCRIPT_PATH"
echo "  Log: /var/log/ml-integration.log"
echo ""
echo -e "${BLUE}💡 Useful Commands:${NC}"
echo "  View cron jobs:  crontab -l"
echo "  Edit cron jobs:  crontab -e"
echo "  View logs:       tail -f /var/log/ml-integration.log"
echo "  Run manually:    python3 $SCRIPT_PATH"
echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo "   ML insights will be updated automatically every hour"