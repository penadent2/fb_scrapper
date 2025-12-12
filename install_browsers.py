#!/usr/bin/env python3
"""
install_browsers.py
Helper script to install Playwright browsers for different options.
Run this to ensure all browsers are available.
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {cmd}")
            return True
        else:
            print(f"✗ {cmd}")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {cmd} - {e}")
        return False

def main():
    print("=" * 60)
    print("Playwright Browser Installation Helper")
    print("=" * 60)
    print()
    
    browsers = {
        "chromium": "Lightweight, no system browser required",
        "chrome": "Google Chrome (requires Chrome installed)",
        "firefox": "Firefox (Playwright downloads it)",
    }
    
    print("Available browsers:")
    for i, (browser, desc) in enumerate(browsers.items(), 1):
        print(f"  {i}. {browser:12} - {desc}")
    print()
    
    # Check if running with argument
    if len(sys.argv) > 1:
        choice = sys.argv[1].lower()
        
        if choice == "all":
            print("Installing all browsers...")
            for browser in browsers:
                cmd = f"playwright install {browser}"
                print(f"\nInstalling {browser}...")
                run_command(cmd)
        elif choice in browsers:
            cmd = f"playwright install {choice}"
            print(f"Installing {choice}...")
            run_command(cmd)
        else:
            print(f"Unknown browser: {choice}")
            print("Usage: python install_browsers.py [all|chromium|chrome|firefox]")
            sys.exit(1)
    else:
        # Interactive mode
        print("Enter browser number to install (or 'all' for all browsers): ", end="")
        choice = input().strip().lower()
        
        if choice == "all":
            print("\nInstalling all browsers...")
            for browser in browsers:
                cmd = f"playwright install {browser}"
                print(f"\nInstalling {browser}...")
                run_command(cmd)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(browsers):
                browser = list(browsers.keys())[idx]
                cmd = f"playwright install {browser}"
                print(f"\nInstalling {browser}...")
                run_command(cmd)
            else:
                print("Invalid selection")
                sys.exit(1)
        else:
            print("Invalid input")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Installation complete!")
    print("=" * 60)
    print("\nYou can now run:")
    print("  python fb_group_monitor_embed_alert.py --login")
    print("  python fb_group_monitor_embed_alert.py --monitor")
    print()

if __name__ == "__main__":
    main()
