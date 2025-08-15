#!/usr/bin/env python3
"""
Auto-activate n8n webhook by sending a dummy request
"""

import requests
import time
import sys

def activate_webhook():
    """Send a dummy request to activate the webhook"""
    try:
        # Create a dummy multipart request to activate the webhook
        files = {'dummy': ('dummy.txt', 'dummy content', 'text/plain')}
        
        response = requests.post(
            'http://localhost:5678/webhook-test/survey-cleaner',
            files=files,
            timeout=10
        )
        
        # Any response (even 404 after first call) means the webhook was activated
        print(f"Webhook activation attempt: {response.status_code}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error activating webhook: {e}")
        return False

def test_webhook_active():
    """Test if webhook is currently active"""
    try:
        files = {'test': ('test.csv', 'test,data\n1,2', 'text/csv')}
        
        response = requests.post(
            'http://localhost:5678/webhook-test/survey-cleaner',
            files=files,
            timeout=5
        )
        
        return response.status_code != 404
        
    except requests.exceptions.RequestException:
        return False

def try_browser_automation():
    """Try to open n8n and execute workflow via browser automation"""
    try:
        import selenium
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # This would require selenium setup
        print("Browser automation could work but requires selenium setup")
        return False
        
    except ImportError:
        print("Selenium not available for browser automation")
        return False

if __name__ == "__main__":
    print("🔄 Attempting to activate n8n webhook...")
    
    # Method 1: Try direct activation
    if activate_webhook():
        time.sleep(1)
        if test_webhook_active():
            print("✅ Webhook activated successfully!")
            sys.exit(0)
    
    print("❌ Auto-activation failed")
    print("📋 Manual steps required:")
    print("  1. Open http://localhost:5678")
    print("  2. Open workflow 'survey-cleaner-mvp'")
    print("  3. Click 'Test workflow'")
    sys.exit(1)