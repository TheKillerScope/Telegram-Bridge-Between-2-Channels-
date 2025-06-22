#!/bin/bash
# Telegram Bridge Automated Setup Script

set -e

echo "🚀 Setting up Telegram Channel Bridge..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ This script must be run as root${NC}"
   echo "Please run: sudo $0"
   exit 1
fi

# Project directory
PROJECT_DIR="/root/tg-bridge"

echo -e "${BLUE}📁 Creating project directory: $PROJECT_DIR${NC}"
mkdir -p "$PROJECT_DIR"

echo -e "${BLUE}📦 Updating system packages...${NC}"
apt update

echo -e "${BLUE}📦 Installing Python and pip...${NC}"
apt install -y python3 python3-pip

echo -e "${BLUE}📦 Installing Telethon...${NC}"
pip3 install telethon

echo -e "${BLUE}📝 Setting up project files...${NC}"

# Copy files to project directory
if [ -f "bridge.py" ]; then
    cp bridge.py "$PROJECT_DIR/"
else
    echo -e "${YELLOW}⚠️ bridge.py not found in current directory${NC}"
    echo -e "${YELLOW}   Please copy bridge.py to $PROJECT_DIR manually${NC}"
fi

if [ -f "generate_session.py" ]; then
    cp generate_session.py "$PROJECT_DIR/"
else
    echo -e "${YELLOW}⚠️ generate_session.py not found in current directory${NC}"
    echo -e "${YELLOW}   Please copy generate_session.py to $PROJECT_DIR manually${NC}"
fi

if [ -f "config.py" ]; then
    cp config.py "$PROJECT_DIR/"
else
    echo -e "${YELLOW}⚠️ config.py not found in current directory${NC}"
    echo -e "${YELLOW}   Please copy config.py to $PROJECT_DIR manually${NC}"
fi

# Set permissions
echo -e "${BLUE}🔧 Setting up permissions...${NC}"
chmod +x "$PROJECT_DIR"/*.py 2>/dev/null || true

# Create log file
echo -e "${BLUE}📝 Setting up logging...${NC}"
touch /var/log/tg-bridge.log
chmod 644 /var/log/tg-bridge.log

# Copy systemd service file
if [ -f "tg-bridge.service" ]; then
    echo -e "${BLUE}⚙️ Installing systemd service...${NC}"
    cp tg-bridge.service /etc/systemd/system/
else
    echo -e "${YELLOW}⚠️ tg-bridge.service not found in current directory${NC}"
    echo -e "${YELLOW}   Please copy tg-bridge.service to /etc/systemd/system/ manually${NC}"
fi

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Edit the configuration:"
echo "   nano $PROJECT_DIR/config.py"
echo ""
echo "2. Generate session string:"
echo "   cd $PROJECT_DIR && python3 generate_session.py"
echo ""
echo "3. Configure the systemd service:"
echo "   nano /etc/systemd/system/tg-bridge.service"
echo "   (Replace YOUR_SESSION_STRING_HERE with your actual session string)"
echo ""
echo "4. Start the service:"
echo "   systemctl daemon-reload"
echo "   systemctl enable tg-bridge"
echo "   systemctl start tg-bridge"
echo ""
echo "5. Monitor the service:"
echo "   systemctl status tg-bridge"
echo "   journalctl -u tg-bridge -f"
echo ""
echo -e "${GREEN}🎉 Your Telegram bridge is ready to be configured!${NC}"
