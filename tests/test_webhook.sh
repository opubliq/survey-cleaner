#!/bin/bash

# Test script for survey-cleaner webhook
# Usage: ./tests/test_webhook.sh

echo "Testing survey-cleaner webhook..."

# Create test CSV file
echo "age,gender,opinion1,opinion2" > /tmp/test.csv
echo "25,M,4,3" >> /tmp/test.csv
echo "30,F,5,2" >> /tmp/test.csv

# Test webhook
echo "Calling webhook with test file..."
curl -X POST http://localhost:5678/webhook-test/survey-cleaner \
  -F 'survey_file=@/tmp/test.csv' \
  -H "Accept: application/json" \
  | jq .

echo -e "\nTest completed."