#!/bin/bash

# Start MVP Survey Cleaner
# Usage: ./start_mvp.sh

set -e

echo "🚀 Starting Survey Cleaner MVP..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if n8n is running
if ! curl -s http://localhost:5678/healthz > /dev/null 2>&1; then
    echo -e "${RED}❌ n8n is not running on localhost:5678${NC}"
    echo "Please start n8n first: npm run start or docker-compose up"
    exit 1
fi

echo -e "${GREEN}✅ n8n is running${NC}"

# Try to auto-activate webhook
echo -e "${BLUE}🔄 Attempting to auto-activate webhook...${NC}"

if python3 web/activate_webhook.py; then
    echo -e "${GREEN}✅ Webhook auto-activated${NC}"
else
    echo -e "${YELLOW}⚠️  Auto-activation failed - manual execution needed in n8n${NC}"
fi

# Start proxy HTTP server for the web interface
echo -e "${BLUE}🌐 Starting web server with proxy...${NC}"

# Kill any existing Python server on port 3000
pkill -f "python.*3000" 2>/dev/null || true

# Start Python proxy server in background
cd web
python3 server.py > /dev/null 2>&1 &
WEB_SERVER_PID=$!
cd ..

# Wait a moment for server to start
sleep 2

# Check if web server is running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Web server running on http://localhost:3000${NC}"
else
    echo -e "${RED}❌ Failed to start web server${NC}"
    kill $WEB_SERVER_PID 2>/dev/null || true
    exit 1
fi

# Open browser
echo -e "${BLUE}🌐 Opening browser...${NC}"
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000 > /dev/null 2>&1
elif command -v open > /dev/null; then
    open http://localhost:3000 > /dev/null 2>&1
else
    echo -e "${YELLOW}Please open http://localhost:3000 in your browser${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Survey Cleaner MVP is ready!${NC}"
echo ""
echo "📋 Usage:"
echo "  • Web interface: http://localhost:3000"
echo "  • n8n workflow: http://localhost:5678"
echo "  • Webhook endpoint: http://localhost:5678/webhook-test/survey-cleaner"
echo ""
echo "🔧 Commands:"
echo "  • Test webhook: ./tests/test_webhook.sh"
echo "  • Stop web server: kill $WEB_SERVER_PID"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop the web server${NC}"

# Keep script running and handle cleanup
cleanup() {
    echo ""
    echo -e "${YELLOW}🔄 Stopping web server...${NC}"
    kill $WEB_SERVER_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for web server
wait $WEB_SERVER_PID