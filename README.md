# Facebook Group Monitor with Discord Alerts

A Python-based Facebook group monitor that detects posts matching keywords and sends Discord notifications. Works with any chromium-based web browser.

## Features

- Monitor multiple Facebook groups
- Keyword filtering
- Time-based filtering (only recent posts)
- SQLite-based deduplication
- Discord embed messages for matched posts
- Admin alerts for re-login requirements
- 24/7 headless operation
- Support for multiple browsers (Chromium, Chrome, Edge, Firefox)

## Dependencies

All dependencies are installed automatically. Required packages:
- `playwright` - Browser automation
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests for Discord webhooks
- Python 3.8+

## Installation

1. Install Python dependencies (if not already installed):
```bash
pip install playwright beautifulsoup4 requests
```

2. Download Playwright browser binaries (required first time):
```bash
playwright install chromium
```

To use Chrome/Edge instead:
```bash
playwright install chrome
```

## Configuration

Edit the following in `fb_group_monitor_embed_alert.py`:

### Facebook Groups
```python
GROUPS = [
    "https://www.facebook.com/groups/your-group-id/",
    # Add more groups here
]
```

### Keywords to Monitor
```python
KEYWORDS = [
    "cần giúp",
    "giúp với",
    # Add your keywords
]
```

### Discord Webhooks
```python
# For post notifications
DISCORD_WEBHOOK_POST = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

# For admin alerts (re-login, errors)
DISCORD_WEBHOOK_ALERT = "https://discord.com/api/webhooks/YOUR_ALERT_WEBHOOK_URL"
```

### Browser Selection
```python
BROWSER_TYPE = "chromium"  # Options: "chromium", "chrome", "edge", "firefox"
BROWSER_EXECUTABLE_PATH = None  # Set to specific path if needed
```

### Monitor Settings
```python
MAX_SCROLL = 5                    # Number of scroll actions per group
SCROLL_DELAY = 2                  # Seconds between scrolls
CHECK_INTERVAL_MINUTES = 5        # Minutes between group checks
ONLY_POST_LAST_HOURS = 6          # Only monitor posts from last N hours
ALERT_COOLDOWN = 60 * 30          # Min seconds between re-login alerts
```

## Usage

### First-Time Setup (Interactive Login)

**Default browser (Chromium):**
```bash
python fb_group_monitor_embed_alert.py --login
```

**Using Chrome:**
```bash
python fb_group_monitor_embed_alert.py --login --browser chrome
```

**Using Edge:**
```bash
python fb_group_monitor_embed_alert.py --login --browser edge
```

**Using specific browser path:**
```bash
python fb_group_monitor_embed_alert.py --login --browser chrome --executable "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

**Steps:**
1. Wait for browser to open
2. Log in to Facebook manually
3. Navigate to your groups and verify you can see posts
4. Return to terminal and press ENTER
5. Cookies will be saved to `fb_cookies.json`

### Run Monitor (Headless Mode)

**Default (after first login):**
```bash
python fb_group_monitor_embed_alert.py --monitor
```

**With specific browser:**
```bash
python fb_group_monitor_embed_alert.py --monitor --browser chrome
```

**Interactive mode (browser visible):**
```bash
python fb_group_monitor_embed_alert.py --monitor --headless false
```

### Command Line Options

```
--login, -l              Start interactive login mode
--monitor, -m            Start monitoring (default)
--browser, -b BROWSER    Browser type: chromium, chrome, edge, firefox
--executable, -e PATH    Path to browser executable
--headless BOOL          true/false (default: true for monitor)
--help, -h              Show help
```

## Supported Browsers

### Chromium (Default)
- Lightweight, automatic download
- No system browser required

### Chrome
- Uses installed Google Chrome browser
- Path typically: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Edge
- Uses installed Microsoft Edge browser
- Path typically: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

### Firefox
- Full Firefox support
- Playwright downloads automatically if not present

## File Structure

```
fb_scrapper/
├── fb_group_monitor_embed_alert.py  # Main script
├── fb_cookies.json                   # Saved login cookies (auto-generated)
├── seen_posts.db                     # SQLite database for deduplication (auto-generated)
└── README.md                         # This file
```

## Troubleshooting

### Browser fails to launch
- Ensure Playwright browser is installed: `playwright install chromium`
- For system browsers (Chrome/Edge), verify the path is correct
- Check that the browser isn't already running exclusively

### Login not saved
- Make sure you pressed ENTER in the terminal after logging in
- Verify `fb_cookies.json` file was created
- Try deleting old `fb_cookies.json` and re-running login

### Posts not being detected
- Check `KEYWORDS` list contains expected terms
- Verify `ONLY_POST_LAST_HOURS` isn't filtering out old posts
- Check the groups are accessible without login

### Discord webhook errors
- Verify webhook URLs are correct and active
- Check Discord server permissions
- Ensure webhook hasn't expired

### High memory usage
- Reduce `MAX_SCROLL` value
- Increase `CHECK_INTERVAL_MINUTES` to check less frequently
- Reduce number of `GROUPS` monitored

## Tips for 24/7 Operation

1. **Use headless mode** for server deployment:
   ```bash
   python fb_group_monitor_embed_alert.py --monitor
   ```

2. **Use a process manager** to auto-restart on crash:
   - Windows: Task Scheduler or NSSM
   - Linux: systemd or supervisor

3. **Log to file** by redirecting output:
   ```bash
   python fb_group_monitor_embed_alert.py --monitor >> monitor.log 2>&1
   ```

4. **Monitor performance** - watch for memory leaks:
   - Restart daily if needed
   - Monitor disk space for `seen_posts.db`

## Security Notes

- **Cookies**: `fb_cookies.json` contains your Facebook login. Keep it private!
- **Webhooks**: Discord webhook URLs in this script should be treated as secrets
- **Environment Variables**: Consider moving sensitive data to `.env` files for production

## Performance Notes

- Typical memory usage: 100-300 MB per browser instance
- First check takes longer (page loading, scrolling)
- Subsequent checks faster due to browser caching
- Database grows ~1KB per unique post detected

## License

MIT License - Feel free to modify and distribute

## Support

For issues:
1. Check the Troubleshooting section
2. Review error messages in console output
3. Try with `--headless false` to see what's happening visually
4. Check that all dependencies are installed: `pip list`
