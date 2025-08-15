#!/bin/bash

# Quick test of the webhook - run this after executing workflow in n8n
echo "🧪 Quick webhook test (run after executing workflow in n8n)"

# Create test file
echo "age,gender,opinion1,opinion2" > /tmp/test.csv
echo "25,M,4,3" >> /tmp/test.csv
echo "30,F,5,2" >> /tmp/test.csv

echo "Testing webhook..."
RESPONSE=$(curl -s -X POST http://localhost:5678/webhook-test/survey-cleaner -F 'survey_file=@/tmp/test.csv')

echo "Response:"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

if echo "$RESPONSE" | grep -q "age\|gender"; then
    echo "✅ Webhook working!"
else
    echo "❌ Webhook not working. Execute the workflow in n8n first."
fi