#!/usr/bin/env python3
"""
fb_group_monitor_embed_alert.py
- Playwright-based Facebook group monitor:
  * multi-group, keyword filter, time filter
  * dedupe via SQLite
  * sends Discord EMBED messages for new posts
  * sends re-login ALERT to admin webhook when FB forces login
  * supports headless 24/7 operation (login once interactively to save cookies)
  * works with any chromium-based browser (Chrome, Edge, Chromium, etc.)
Notes:
- Run once with headless=False to login manually and save storage_state=fb_cookies.json
- Then run headless=True for 24/7.
"""

import os
import sys
import time
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# ===== USER CONFIG =====
# Browser selection: 'chromium', 'chrome', 'edge', or 'firefox'
BROWSER_TYPE = "chromium"  # Change to 'chrome' or 'edge' if you prefer
BROWSER_EXECUTABLE_PATH = None  # Set to specific path if using system browser, e.g., "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

GROUPS = [
    "https://www.facebook.com/groups/genshinimpactvnmbvct/",
    "https://www.facebook.com/groups/6911770178952785/",
    "https://www.facebook.com/groups/648618483681727/",
]

KEYWORDS = [
    "cần giúp", "giúp với", "hỗ trợ", "fix", "bị lỗi",
    "tuyển", "cần người", "tìm người", "bán", "mua",
]

# Webhook to receive normal post embeds
DISCORD_WEBHOOK_POST = "https://discord.com/api/webhooks/1448923475933790250/YpWdrh6tNqb32wixXGUOoYRkgaL5AMqWrq0b1gz7vlm2yr7yM_UKj-HeSv08B__3sZtQ"

# Webhook to receive admin alerts (re-login required, errors)
DISCORD_WEBHOOK_ALERT = "https://discord.com/api/webhooks/1448923476348899453/0mSp8q2IM3C7i7F34QiEM4N6JA44JfKvELsBC_i7nDR2PeBFMog95z0JS7rg4XKLTqz3"

# Cookie / storage file name (Playwright)
STORAGE_STATE = "fb_cookies.json"

# SQLite DB file for dedupe
DB_FILE = "seen_posts.db"

# runtime settings
MAX_SCROLL = 5
SCROLL_DELAY = 2
CHECK_INTERVAL_MINUTES = 5
ONLY_POST_LAST_HOURS = 6

# If re-login is detected, avoid spamming alerts; min interval (seconds) between alerts
ALERT_COOLDOWN = 60 * 30  # 30 minutes

# ===== DB helpers =====
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seen (
            post_link TEXT PRIMARY KEY,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def is_seen(conn, link):
    if not link:
        return False
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM seen WHERE post_link = ?", (link,))
    return cur.fetchone() is not None

def mark_seen(conn, link):
    if not link:
        return
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO seen(post_link) VALUES(?)", (link,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

# ===== Discord helpers =====
def post_discord_embed(webhook_url, embed_obj):
    """
    embed_obj: dict following Discord embed schema.
    """
    if not webhook_url:
        print("[DISCORD] webhook not configured.")
        return False
    payload = {"embeds": [embed_obj]}
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        if 200 <= r.status_code < 300:
            return True
        else:
            print("[DISCORD] send failed:", r.status_code, r.text)
            return False
    except Exception as e:
        print("[DISCORD] exception:", e)
        return False

def send_post_embed(post):
    """
    post: {content, link, raw_time, parsed_time, thumbnail}
    """
    title = (post.get("content") or "")[:200]
    link = post.get("link")
    timestamp = post.get("parsed_time") or datetime.now().isoformat()
    thumbnail = post.get("thumbnail")

    embed = {
        "title": "New FB post matched",
        "description": title,
        "url": link,
        "timestamp": timestamp,
        "footer": {"text": "FB Group Monitor"},
        "fields": [
            {"name": "Time", "value": post.get("raw_time", "unknown"), "inline": True},
            {"name": "Link", "value": link or "N/A", "inline": False},
        ]
    }
    if thumbnail:
        embed["thumbnail"] = {"url": thumbnail}

    return post_discord_embed(DISCORD_WEBHOOK_POST, embed)

def send_alert(message):
    embed = {
        "title": "FB Monitor Alert",
        "description": message,
        "timestamp": datetime.now().isoformat(),
        "footer": {"text": "Action required"}
    }
    return post_discord_embed(DISCORD_WEBHOOK_ALERT, embed)

# ===== time parsing (Vietnamese-friendly) =====
def get_browser_launcher(pw, browser_type=None, executable_path=None):
    """
    Get the appropriate browser launcher from Playwright.
    Supports: chromium, chrome, edge, firefox
    
    Args:
        pw: Playwright instance
        browser_type: 'chromium', 'chrome', 'edge', or 'firefox'. Defaults to BROWSER_TYPE.
        executable_path: Optional path to specific browser executable
        
    Returns:
        Browser launcher object or None if browser type not available
    """
    browser_type = browser_type or BROWSER_TYPE
    browser_type = browser_type.lower().strip()
    
    try:
        if browser_type == "chrome":
            return pw.chromium
        elif browser_type == "edge":
            return pw.chromium
        elif browser_type == "firefox":
            return pw.firefox
        elif browser_type == "chromium":
            return pw.chromium
        else:
            print(f"[WARNING] Unknown browser type: {browser_type}. Using chromium.")
            return pw.chromium
    except AttributeError as e:
        print(f"[ERROR] Browser type '{browser_type}' not available: {e}")
        print("[WARNING] Falling back to chromium")
        return pw.chromium

def launch_browser(pw, headless=True, browser_type=None, executable_path=None):
    """
    Launch browser with proper configuration.
    
    Args:
        pw: Playwright instance
        headless: Run in headless mode
        browser_type: 'chromium', 'chrome', 'edge', or 'firefox'
        executable_path: Optional path to specific browser executable
        
    Returns:
        Browser instance
    """
    browser_type = browser_type or BROWSER_TYPE
    executable_path = executable_path or BROWSER_EXECUTABLE_PATH
    
    launcher = get_browser_launcher(pw, browser_type, executable_path)
    
    # Launch options
    launch_args = {
        "headless": headless,
    }
    
    # Add executable path if specified
    if executable_path and os.path.isfile(executable_path):
        launch_args["executable_path"] = executable_path
        print(f"[BROWSER] Using executable: {executable_path}")
    
    try:
        browser = launcher.launch(**launch_args)
        print(f"[BROWSER] Launched {browser_type} (headless={headless})")
        return browser
    except Exception as e:
        print(f"[ERROR] Failed to launch {browser_type}: {e}")
        if executable_path:
            print("[INFO] Retrying without executable path...")
            launch_args.pop("executable_path", None)
            try:
                browser = launcher.launch(**launch_args)
                return browser
            except Exception as e2:
                print(f"[ERROR] Still failed: {e2}")
                raise

# ===== time parsing (Vietnamese-friendly) =====
def parse_facebook_time(text):
    if not text:
        return None
    text = text.lower().strip()
    now = datetime.now()

    # common short forms
    if "vừa xong" in text:
        return now

    if "phút" in text:
        try:
            num = int(text.split()[0])
            return now - timedelta(minutes=num)
        except:
            pass

    if "giờ" in text:
        try:
            num = int(text.split()[0])
            return now - timedelta(hours=num)
        except:
            pass

    if "hôm nay" in text:
        # May be like "Hôm nay lúc 13:20"
        try:
            if "lúc" in text:
                time_part = text.split("lúc")[-1].strip()
                hh, mm = [int(x) for x in time_part.split(":")]
                return now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            else:
                return now
        except:
            return now

    if "hôm qua" in text:
        try:
            if "lúc" in text:
                time_part = text.split("lúc")[-1].strip()
                hh, mm = [int(x) for x in time_part.split(":")]
                d = now - timedelta(days=1)
                return d.replace(hour=hh, minute=mm, second=0, microsecond=0)
            else:
                d = now - timedelta(days=1)
                return d
        except:
            return now - timedelta(days=1)

    # try parse formats like "20 Tháng 1 lúc 14:10" or "20 tháng 1 lúc 14:10"
    try:
        parts = text.replace("lúc", "").strip()
        parts = parts.replace("tháng", "month")  # temporary placeholder
        # manually parse dd month mm HH:MM (since month name is numeric in VN: e.g., "1")
        # attempt pattern: "20 tháng 1 14:10"
        tokens = parts.replace(",", " ").split()
        # find numeric tokens
        nums = [t for t in tokens if t.isdigit()]
        if len(nums) >= 3:
            day = int(nums[0])
            month = int(nums[1])
            time_part = nums[2] if ":" not in tokens[-1] else tokens[-1]
            if ":" in time_part:
                hh, mm = [int(x) for x in time_part.split(":")]
            else:
                hh, mm = 0, 0
            dt = datetime(now.year, month, day, hh, mm)
            return dt
    except:
        pass

    return None

# ===== HTML extraction =====
POST_LINK_PATTERNS = [
    # generic patterns - we'll use anchor href if available
]

def extract_posts_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("div", attrs={"role": "article"})
    results = []
    for art in articles:
        text_full = art.get_text(" ").strip()
        text_lower = text_full.lower()
        if not any(k in text_lower for k in KEYWORDS):
            continue

        # find link: prefer anchors with permalink-like paths
        link = None
        a = art.find("a", href=True)
        if a:
            href = a["href"]
            # normalize relative links
            if href.startswith("/"):
                href = "https://www.facebook.com" + href
            link = href

        # raw time: many FB UIs put time in <abbr> or <span data-tooltip-content>
        raw_time = None
        parsed_time = None
        time_candidates = art.find_all(["abbr", "span", "div"])
        for t in time_candidates:
            txt = t.get_text(" ").strip()
            if txt:
                # heuristics: contains "giờ" "phút" "hôm" "tháng" or ":" -> candidate
                if any(tok in txt.lower() for tok in ["giờ", "phút", "hôm", "tháng", ":"]):
                    raw_time = txt
                    parsed_time = parse_facebook_time(txt)
                    if parsed_time:
                        break

        # thumbnail: try find first image
        thumb = None
        img = art.find("img")
        if img and img.has_attr("src"):
            thumb = img["src"]

        # if parsed_time None -> skip (we want time-limited posts)
        if not parsed_time:
            continue

        # filter by recency
        if parsed_time < datetime.now() - timedelta(hours=ONLY_POST_LAST_HOURS):
            continue

        results.append({
            "content": text_full.strip(),
            "content_snippet": (text_full.strip()[:300] + "...") if len(text_full.strip()) > 300 else text_full.strip(),
            "link": link,
            "raw_time": raw_time,
            "parsed_time": parsed_time.isoformat(),
            "thumbnail": thumb
        })

    return results

# ===== login / re-login detection =====
def detect_need_login(page):
    """
    Returns True if page indicates Facebook requires login.
    Checks:
    - URL contains '/login' or '/checkpoint'
    - presence of input#email on page
    - presence of text 'log in' / 'login' in content
    """
    try:
        url = page.url
        if "login" in url or "checkpoint" in url:
            return True

        # quick DOM heuristics
        content = page.content().lower()
        if "log in" in content or "đăng nhập" in content:
            # be conservative: ensure there is input#email
            if "input" in content and "email" in content:
                return True

        # Playwright selectors (safe): check existence of email input
        try:
            if page.query_selector("input#email") is not None:
                return True
        except:
            pass

    except Exception as e:
        print("[detect_need_login] exception:", e)

    return False

# ===== scanning / orchestration =====
def scan_group_page(page, url, conn, last_alert):
    print(f"[SCAN] {url}")
    try:
        page.goto(url, timeout=60000)
        time.sleep(4)
    except Exception as e:
        print("[SCAN] navigation error:", e)
        return last_alert

    # detect login requirement early
    if detect_need_login(page):
        now = time.time()
        if last_alert is None or (now - last_alert) > ALERT_COOLDOWN:
            send_alert(f"Facebook requested login/checkpoint when opening {url}. Manual intervention required.")
            last_alert = now
        else:
            print("[ALERT] login detected but in cooldown.")
        return last_alert

    html_all = ""
    for _ in range(MAX_SCROLL):
        try:
            page.mouse.wheel(0, 5000)
            time.sleep(SCROLL_DELAY)
            html_all += page.content()
        except Exception as e:
            print("[SCAN] scroll error:", e)
            break

    posts = extract_posts_from_html(html_all)
    print(f"[SCAN] {len(posts)} matched recent posts")

    for post in posts:
        link = post.get("link")
        # fallback: if no link, create pseudo-id from snippet + time
        pid = link or (post["content_snippet"][:200] + "|" + post["parsed_time"])
        if is_seen(conn, pid):
            print("[SKIP] seen:", pid)
            continue
        # mark seen early to prevent double-send on races
        mark_seen(conn, pid)

        ok = send_post_embed(post)
        if ok:
            print("[SENT]", pid)
        else:
            print("[SEND FAILED]", pid)
    return last_alert

def run_monitor(headless=True, browser_type=None, executable_path=None):
    conn = init_db()
    last_alert_time = None

    with sync_playwright() as pw:
        # Launch browser with configuration
        try:
            browser = launch_browser(pw, headless=headless, browser_type=browser_type, executable_path=executable_path)
        except Exception as e:
            print(f"[ERROR] Failed to launch browser: {e}")
            send_alert(f"FB Monitor: Failed to launch browser - {e}")
            return
        
        # try reuse storage_state
        try:
            context = browser.new_context(storage_state=STORAGE_STATE)
        except Exception:
            print("[INFO] No saved cookies found or cookies invalid, creating new context")
            context = browser.new_context()

        page = context.new_page()
        # check login status
        try:
            page.goto("https://www.facebook.com", timeout=60000)
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] Failed to navigate to Facebook: {e}")
            send_alert(f"FB Monitor: Failed to navigate to Facebook - {e}")
            browser.close()
            return
            
        if detect_need_login(page):
            # not logged in
            send_alert("FB Monitor: Not logged in. Run once with headless=False and perform manual login to save cookies to fb_cookies.json.")
            print("NOT LOGGED IN. Run with headless=False for manual login and save storage_state.")
            browser.close()
            return

        # main loop
        print("Starting monitor loop (headless=%s, browser=%s) ..." % (headless, browser_type or BROWSER_TYPE))
        try:
            while True:
                for g in GROUPS:
                    last_alert_time = scan_group_page(page, g, conn, last_alert_time)
                    time.sleep(3)
                print(f"[SLEEP] {CHECK_INTERVAL_MINUTES} minutes...")
                time.sleep(CHECK_INTERVAL_MINUTES * 60)
        except KeyboardInterrupt:
            print("[INFO] Monitor stopped by user")
        finally:
            browser.close()

# ===== entrypoint (run interactive login save) =====
def interactive_login_and_save(browser_type=None, executable_path=None):
    """
    Run once interactively (headless=False). After manual login, save storage_state to file.
    
    Args:
        browser_type: 'chromium', 'chrome', 'edge', or 'firefox'
        executable_path: Optional path to specific browser executable
    """
    with sync_playwright() as pw:
        try:
            browser = launch_browser(pw, headless=False, browser_type=browser_type, executable_path=executable_path)
        except Exception as e:
            print(f"[ERROR] Failed to launch browser: {e}")
            return
            
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto("https://www.facebook.com", timeout=60000)
            print("Please login manually in the opened browser window. After login completes and you see your feed, press ENTER here to save cookies.")
            input("Press ENTER after login...")
            context.storage_state(path=STORAGE_STATE)
            print(f"Saved cookies to {STORAGE_STATE}")
        except Exception as e:
            print(f"[ERROR] Failed during login: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    """
    Usage examples:
    
    1. First time setup - Interactive login with default browser (chromium):
       python fb_group_monitor_embed_alert.py --login
       
    2. First time setup - Interactive login with Chrome/Edge:
       python fb_group_monitor_embed_alert.py --login --browser chrome
       python fb_group_monitor_embed_alert.py --login --browser edge
       
    3. First time setup - Interactive login with specific browser path:
       python fb_group_monitor_embed_alert.py --login --browser chrome --executable "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
       
    4. Run monitor in headless mode (after login):
       python fb_group_monitor_embed_alert.py --monitor
       python fb_group_monitor_embed_alert.py --monitor --browser chrome
       
    5. Run interactive (non-headless) mode:
       python fb_group_monitor_embed_alert.py --monitor --headless false
    """
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    # Defaults
    mode = "monitor"  # 'login' or 'monitor'
    headless = True
    browser_type = BROWSER_TYPE
    executable_path = BROWSER_EXECUTABLE_PATH
    
    # Parse arguments
    i = 0
    while i < len(args):
        arg = args[i].lower()
        
        if arg in ["--login", "-l"]:
            mode = "login"
        elif arg in ["--monitor", "-m"]:
            mode = "monitor"
        elif arg in ["--headless"]:
            if i + 1 < len(args):
                headless = args[i + 1].lower() != "false"
                i += 1
        elif arg in ["--browser", "-b"]:
            if i + 1 < len(args):
                browser_type = args[i + 1].lower()
                i += 1
        elif arg in ["--executable", "-e"]:
            if i + 1 < len(args):
                executable_path = args[i + 1]
                i += 1
        elif arg in ["--help", "-h"]:
            print(__doc__)
            sys.exit(0)
        
        i += 1
    
    # Execute
    if mode == "login":
        print(f"[SETUP] Starting interactive login with {browser_type}...")
        interactive_login_and_save(browser_type=browser_type, executable_path=executable_path)
    else:
        print(f"[MONITOR] Starting in headless={headless} mode with {browser_type}...")
        run_monitor(headless=headless, browser_type=browser_type, executable_path=executable_path)
