#!/usr/bin/env python3
"""
Simple script to test Facebook login and save cookies
"""
import time
from playwright.sync_api import sync_playwright

STORAGE_STATE = "fb_cookies.json"

def main():
    with sync_playwright() as pw:
        # Launch browser in non-headless mode
        browser = pw.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--window-size=1280,720',
            ]
        )
        
        # Create context with anti-detection settings
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720},
            locale='vi-VN',
            timezone_id='Asia/Ho_Chi_Minh',
        )
        
        page = context.new_page()
        
        print("Opening Facebook...")
        page.goto("https://www.facebook.com")
        
        print("\n" + "="*60)
        print("PLEASE LOGIN TO FACEBOOK IN THE BROWSER WINDOW")
        print("After you see your Facebook feed, press ENTER here...")
        print("="*60 + "\n")
        
        input("Press ENTER after you've logged in: ")
        
        # Save cookies
        try:
            context.storage_state(path=STORAGE_STATE)
            print(f"\n✓ Cookies saved to {STORAGE_STATE}")
            print("You can now close the browser and run the monitor in headless mode.")
        except Exception as e:
            print(f"\n✗ Failed to save cookies: {e}")
        
        browser.close()

if __name__ == "__main__":
    main()

