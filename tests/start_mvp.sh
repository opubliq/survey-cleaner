#!/bin/bash

# Start Survey Cleaner MVP with n8n form
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

echo ""
echo -e "${GREEN}🎉 Survey Cleaner MVP is ready!${NC}"
echo ""
echo "📋 Usage:"
echo "  • n8n interface: http://localhost:5678"
echo "  • Workflow: survey-cleaner-mvp"
echo "  • Upload form: Use the built-in n8n form trigger"
echo ""
echo "🔧 Instructions:"
echo "  1. Open http://localhost:5678"
echo "  2. Open the 'survey-cleaner-mvp' workflow"  
echo "  3. Use the form trigger to upload files directly"
echo ""
echo "📁 Test files available:"
echo "  • Codebook: tests/test_codebook.txt"
echo "  • Survey data: tests/test_survey.csv"