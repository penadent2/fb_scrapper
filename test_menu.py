#!/usr/bin/env python3
# Quick test script for the menu
import subprocess
import sys

# Test 1: Show menu with option 2 (headless monitor)
print("Testing interactive menu...")
result = subprocess.run(
    [sys.executable, "fb_group_monitor_embed_alert.py"],
    input="2\n",
    capture_output=True,
    text=True,
    timeout=5
)
print(result.stdout)
if result.returncode != 0 and "ERROR" not in result.stdout:
    print("[OK] Menu displayed successfully!")
