# Quick Start Guide

## Step 1: Install Dependencies

Run this once to install all required Python packages:

```bash
pip install -r requirements.txt
```

Or individually:

```bash
pip install playwright beautifulsoup4 requests
```

## Step 2: Install Browser(s)

Choose your preferred browser and install it:

### Option A: Automatic (Recommended)
```bash
python install_browsers.py
```

Then select:
- `1` for Chromium (default, no system browser needed)
- `2` for Chrome (requires Chrome installed)
- `3` for Firefox
- `all` for all browsers

### Option B: Manual Command
```bash
# Install Chromium (default, recommended)
playwright install chromium

# OR install Chrome
playwright install chrome

# OR install Firefox
playwright install firefox
```

## Step 3: Configure the Script

Edit `fb_group_monitor_embed_alert.py` and update:

1. **Facebook Groups** (around line 35):
   ```python
   GROUPS = [
       "https://www.facebook.com/groups/your-group-id/",
   ]
   ```

2. **Keywords to Monitor** (around line 40):
   ```python
   KEYWORDS = [
       "your keyword here",
       "another keyword",
   ]
   ```

3. **Discord Webhooks** (around line 45):
   ```python
   DISCORD_WEBHOOK_POST = "your-webhook-url-here"
   DISCORD_WEBHOOK_ALERT = "your-alert-webhook-url-here"
   ```

4. **Browser Type** (around line 30, optional):
   ```python
   BROWSER_TYPE = "chromium"  # or "chrome", "edge", "firefox"
   ```

## Step 4: Interactive Login

Run once to login to Facebook and save cookies:

```bash
python fb_group_monitor_embed_alert.py --login
```

**What happens:**
1. A browser window opens
2. Log in to Facebook manually
3. Make sure you're in your target groups
4. Return to terminal and press ENTER
5. Cookies are saved automatically

### Alternative: Use Specific Browser for Login
```bash
# Login with Chrome
python fb_group_monitor_embed_alert.py --login --browser chrome

# Login with Edge
python fb_group_monitor_embed_alert.py --login --browser edge
```

## Step 5: Start Monitoring

Run the monitor in headless mode (no window):

```bash
python fb_group_monitor_embed_alert.py --monitor
```

**What happens:**
1. Monitor starts checking your groups
2. Every 5 minutes (configurable), it scans all groups
3. When posts matching keywords are found, Discord notifications are sent
4. Script runs 24/7 until you stop it (Ctrl+C)

### Alternative: Run in Interactive Mode
```bash
# See browser activity while monitoring
python fb_group_monitor_embed_alert.py --monitor --headless false
```

## Step 6: Set Up for 24/7 Operation

### Windows - Task Scheduler Method

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Facebook Group Monitor"
4. Trigger: At startup
5. Action: Start a program
6. Program: `python`
7. Arguments: `fb_group_monitor_embed_alert.py --monitor`
8. Working directory: path to your script folder

### Windows - NSSM Method (Recommended)

1. Download NSSM from https://nssm.cc/
2. Open Command Prompt as Admin
3. Run:
   ```bash
   nssm install FBMonitor "C:\path\to\python.exe" "C:\path\to\fb_group_monitor_embed_alert.py --monitor"
   nssm start FBMonitor
   ```

### Linux - Systemd Method

Create `/etc/systemd/system/fb-monitor.service`:

```ini
[Unit]
Description=Facebook Group Monitor
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/fb_scrapper
ExecStart=/path/to/python fb_group_monitor_embed_alert.py --monitor
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable fb-monitor
sudo systemctl start fb-monitor
```

## Troubleshooting

### Browser won't launch
```bash
# Reinstall browsers
python install_browsers.py all

# Or manual
playwright install chromium
```

### Login didn't save
- Make sure you pressed ENTER in terminal after login
- Check if `fb_cookies.json` was created
- Delete old cookies and try again: `rm fb_cookies.json`

### No posts being detected
- Check keywords in script match actual posts
- Try with `--headless false` to see what's visible
- Verify groups are accessible without login

### Discord not receiving messages
- Test webhook URL in Discord settings
- Verify webhook URLs in script are correct
- Check Discord server has proper permissions

### Memory usage too high
- Reduce `MAX_SCROLL` (currently 5)
- Increase `CHECK_INTERVAL_MINUTES` (currently 5)
- Reduce number of groups monitored

## Check Logs

To see what's happening, redirect output to a file:

```bash
# On Windows
python fb_group_monitor_embed_alert.py --monitor >> monitor.log 2>&1

# On Linux/Mac
python fb_group_monitor_embed_alert.py --monitor > monitor.log 2>&1
```

Then read the log:
```bash
tail -f monitor.log
```

## Common Commands Reference

```bash
# First time setup
python fb_group_monitor_embed_alert.py --login

# Start monitoring (Chromium)
python fb_group_monitor_embed_alert.py --monitor

# Start with Chrome
python fb_group_monitor_embed_alert.py --monitor --browser chrome

# Start with Edge
python fb_group_monitor_embed_alert.py --monitor --browser edge

# Interactive mode (see browser)
python fb_group_monitor_embed_alert.py --monitor --headless false

# Help
python fb_group_monitor_embed_alert.py --help

# Install browsers interactively
python install_browsers.py
```

## Files Created/Modified

After running, you'll have:
- `fb_cookies.json` - Your login session (KEEP PRIVATE!)
- `seen_posts.db` - Database of posts already processed
- `monitor.log` - Log file (if you redirect output)

## Support

If something isn't working:
1. Check troubleshooting section above
2. Try with `--headless false` to see what's happening visually
3. Check that all dependencies are installed: `pip list`
4. Read error messages carefully - they usually tell you what's wrong

## Next Steps

Once monitoring is working:
1. Fine-tune keywords in `KEYWORDS` list
2. Adjust timing settings (`CHECK_INTERVAL_MINUTES`, etc.)
3. Set up 24/7 operation using Task Scheduler or systemd
4. Monitor logs for issues

Good luck! Your Facebook group monitor is now ready to use! 🚀
