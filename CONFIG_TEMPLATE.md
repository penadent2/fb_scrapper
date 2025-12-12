# Configuration Template for fb_group_monitor_embed_alert.py

## Browser Configuration

```python
# Choose your browser: 'chromium' (default), 'chrome', 'edge', or 'firefox'
BROWSER_TYPE = "chromium"

# Optional: Path to specific browser executable (leave None for auto-detection)
# Examples:
# BROWSER_EXECUTABLE_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# BROWSER_EXECUTABLE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
BROWSER_EXECUTABLE_PATH = None
```

## Facebook Configuration

```python
# List of Facebook group URLs to monitor
GROUPS = [
    "https://www.facebook.com/groups/YOUR_GROUP_ID_1/",
    "https://www.facebook.com/groups/YOUR_GROUP_ID_2/",
    "https://www.facebook.com/groups/YOUR_GROUP_ID_3/",
]

# Keywords to search for in posts
# Posts containing ANY of these keywords will trigger a Discord notification
KEYWORDS = [
    "cần giúp",           # Vietnamese: need help
    "giúp với",           # Vietnamese: help me
    "hỗ trợ",             # Vietnamese: support
    "fix",                # English: fix
    "bị lỗi",             # Vietnamese: got error
    "tuyển",              # Vietnamese: hiring
    "cần người",          # Vietnamese: need people
    "tìm người",          # Vietnamese: looking for people
    "bán",                # Vietnamese: selling
    "mua",                # Vietnamese: buying
]
```

## Discord Webhook Configuration

Get your webhooks from Discord server settings → Integrations → Webhooks

```python
# Webhook URL for normal post notifications
# Posts matching keywords will be sent here as Discord embeds
DISCORD_WEBHOOK_POST = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# Webhook URL for admin alerts
# Re-login requirements, errors, and important events go here
DISCORD_WEBHOOK_ALERT = "https://discord.com/api/webhooks/YOUR_ALERT_WEBHOOK_ID/YOUR_ALERT_WEBHOOK_TOKEN"
```

## File Configuration

```python
# Name of file to store Facebook login session cookies
# This file is created after first login and reused for subsequent runs
STORAGE_STATE = "fb_cookies.json"

# Name of SQLite database file for tracking posts
# Prevents sending duplicate notifications
DB_FILE = "seen_posts.db"
```

## Monitoring Behavior Configuration

```python
# Number of scroll actions per group check
# Higher = more posts checked, higher memory usage
MAX_SCROLL = 5

# Delay between scroll actions (seconds)
# Lower = faster scanning, higher load on Facebook
SCROLL_DELAY = 2

# How often to check groups (minutes)
# Lower = more frequent updates, higher resource usage
CHECK_INTERVAL_MINUTES = 5

# Only monitor posts from the last N hours
# Posts older than this will be ignored
ONLY_POST_LAST_HOURS = 6

# Minimum time between re-login alerts (seconds)
# Prevents alert spam if Facebook repeatedly asks to login
ALERT_COOLDOWN = 60 * 30  # 30 minutes
```

---

## Configuration Guide by Use Case

### Use Case 1: Monitor Fast-Moving Group (Real-Time)
```python
MAX_SCROLL = 3
SCROLL_DELAY = 1
CHECK_INTERVAL_MINUTES = 1
ONLY_POST_LAST_HOURS = 2
```

### Use Case 2: Monitor Slow Group (Daily Summary)
```python
MAX_SCROLL = 10
SCROLL_DELAY = 3
CHECK_INTERVAL_MINUTES = 60
ONLY_POST_LAST_HOURS = 24
```

### Use Case 3: Monitor Multiple Groups (Balanced)
```python
MAX_SCROLL = 5
SCROLL_DELAY = 2
CHECK_INTERVAL_MINUTES = 5
ONLY_POST_LAST_HOURS = 6
```

### Use Case 4: Low Resource Server
```python
MAX_SCROLL = 2
SCROLL_DELAY = 3
CHECK_INTERVAL_MINUTES = 15
ONLY_POST_LAST_HOURS = 12
```

---

## Discord Webhook Setup

### Creating a Webhook
1. Open Discord server
2. Server Settings → Integrations
3. Click "Webhooks" → "Create Webhook"
4. Name it (e.g., "FB Group Monitor")
5. Choose the channel (where notifications go)
6. Copy the webhook URL

### Webhook URL Format
```
https://discord.com/api/webhooks/WEBHOOK_ID/WEBHOOK_TOKEN
```

**Keep this URL SECRET!** Anyone with this URL can post to your webhook.

### Testing Your Webhook (with curl)
```bash
curl -X POST https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN \
  -H 'Content-Type: application/json' \
  -d '{"content":"Test message"}'
```

---

## Getting Facebook Group IDs

### Method 1: From URL
Group URL: `https://www.facebook.com/groups/123456789/`
Group ID: `123456789`

### Method 2: Visit Group
1. Open Facebook group
2. Look at URL in address bar
3. The long number is your group ID

### Method 3: From Facebook Group Link
1. Right-click group → Copy link
2. Extract the ID from the URL

---

## Browser Configuration Examples

### Using Default Chromium
```python
BROWSER_TYPE = "chromium"
BROWSER_EXECUTABLE_PATH = None
```
Command: `python fb_group_monitor_embed_alert.py --monitor`

### Using Google Chrome
```python
BROWSER_TYPE = "chrome"
BROWSER_EXECUTABLE_PATH = None  # Auto-detect
```
Command: `python fb_group_monitor_embed_alert.py --monitor --browser chrome`

### Using Microsoft Edge
```python
BROWSER_TYPE = "edge"
BROWSER_EXECUTABLE_PATH = None  # Auto-detect
```
Command: `python fb_group_monitor_embed_alert.py --monitor --browser edge`

### Using Specific Chrome Installation
```python
BROWSER_TYPE = "chrome"
BROWSER_EXECUTABLE_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
```
Command: `python fb_group_monitor_embed_alert.py --monitor --executable "path/to/chrome.exe"`

### Using Firefox
```python
BROWSER_TYPE = "firefox"
BROWSER_EXECUTABLE_PATH = None
```
Command: `python fb_group_monitor_embed_alert.py --monitor --browser firefox`

---

## Advanced Configuration

### Customizing Time Parsing
The script can parse Vietnamese time formats:
- "vừa xong" → just now
- "5 phút" → 5 minutes ago
- "2 giờ" → 2 hours ago
- "hôm nay lúc 14:30" → today at 14:30
- "20 tháng 1 lúc 14:10" → Jan 20 at 14:10

### Customizing Post Extraction
The script looks for:
- Posts with "role=article" attribute
- Text content containing keywords
- Facebook timestamp elements
- Post links and thumbnails

To debug HTML extraction:
1. Run with `--headless false`
2. Inspect elements in browser
3. Add CSS selectors to extraction logic

### Customizing Discord Embeds
Edit `send_post_embed()` function to change:
- Embed color
- Thumbnail size
- Fields displayed
- Footer text

---

## Performance Tuning

### High Memory Usage?
```python
MAX_SCROLL = 2        # Reduce scrolling
CHECK_INTERVAL_MINUTES = 10  # Check less often
```

### Too Many False Positives?
```python
KEYWORDS = [...]      # Be more specific
ONLY_POST_LAST_HOURS = 3   # Narrow time window
```

### Missing Posts?
```python
MAX_SCROLL = 10       # Check more posts
SCROLL_DELAY = 1      # Don't wait between scrolls
CHECK_INTERVAL_MINUTES = 2  # Check more often
```

### Too Many Notifications?
```python
KEYWORDS = [...]      # Fewer keywords
ONLY_POST_LAST_HOURS = 1   # Only very recent
```

---

## Troubleshooting Configuration

### Facebook asks to login repeatedly
- Increase `ALERT_COOLDOWN` to reduce alert spam
- Try different browser type
- Make sure cookies file is writable

### No posts found
- Check `KEYWORDS` are correct
- Verify `ONLY_POST_LAST_HOURS` isn't too small
- Run with `--headless false` to see what's displayed

### Memory usage climbing
- Reduce `MAX_SCROLL`
- Increase `CHECK_INTERVAL_MINUTES`
- Reduce number of `GROUPS`
- Restart script daily

### Discord notifications not working
- Verify webhook URLs
- Check Discord channel permissions
- Test webhook manually
- Check for Discord rate limiting

---

## Example Complete Configuration

```python
# ===== Browser =====
BROWSER_TYPE = "chrome"
BROWSER_EXECUTABLE_PATH = None

# ===== Groups =====
GROUPS = [
    "https://www.facebook.com/groups/123456789/",
    "https://www.facebook.com/groups/987654321/",
]

# ===== Keywords =====
KEYWORDS = [
    "cần giúp",
    "bị lỗi",
    "tuyển",
]

# ===== Discord =====
DISCORD_WEBHOOK_POST = "https://discord.com/api/webhooks/123456/abcdef"
DISCORD_WEBHOOK_ALERT = "https://discord.com/api/webhooks/654321/fedcba"

# ===== Behavior =====
MAX_SCROLL = 5
SCROLL_DELAY = 2
CHECK_INTERVAL_MINUTES = 5
ONLY_POST_LAST_HOURS = 6
ALERT_COOLDOWN = 60 * 30
```

Then run:
```bash
python fb_group_monitor_embed_alert.py --login
python fb_group_monitor_embed_alert.py --monitor
```

---

## Best Practices

1. **Security**
   - Keep `fb_cookies.json` private
   - Keep webhook URLs secret
   - Don't commit sensitive data to git

2. **Reliability**
   - Monitor logs for errors
   - Restart script daily
   - Keep Facebook password strong

3. **Performance**
   - Start with default settings
   - Adjust based on results
   - Monitor memory usage

4. **Maintenance**
   - Clean old entries from `seen_posts.db` monthly
   - Refresh cookies monthly
   - Update keywords as needed

---

That's it! Customize based on your needs. 🎉
