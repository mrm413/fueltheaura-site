#!/bin/bash

echo "🚀 Installing ML Analytics API..."
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/opt/fueltheaura-ai"
SERVICE_NAME="ml-api.service"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Copy ML API script
echo -e "${BLUE}📋 Installing ML API script...${NC}"
cp ml_api.py $INSTALL_DIR/
chmod +x $INSTALL_DIR/ml_api.py

# Install required Python packages
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip3 install -r requirements_api.txt

# Create systemd service
echo -e "${BLUE}⚙️  Creating systemd service...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME << EOF
[Unit]
Description=ML Analytics API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 $INSTALL_DIR/ml_api.py
Restart=always
RestartSec=10

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
echo -e "${BLUE}🚀 Starting ML API...${NC}"
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
echo "🌐 API Endpoints:"
echo "  Health Check:  http://localhost:5000/api/health"
echo "  Dashboard:     http://localhost:5000/api/ml/dashboard"
echo "  Stats:         http://localhost:5000/api/ml/stats"
echo "  Insights:      http://localhost:5000/api/ml/insights"
echo "  Predictions:   http://localhost:5000/api/ml/predictions"
echo "  Models:        http://localhost:5000/api/ml/models"
echo ""
echo -e "${GREEN}🎉 ML API is now running on port 5000!${NC}"