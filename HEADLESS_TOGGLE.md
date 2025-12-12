# FASTER HEADLESS TOGGLE - Quick Reference

## ⚡ 3 Ways to Switch Between Headless/Interactive Mode

### **Method 1: FASTEST - Edit Config (Recommended)**
Edit line 65 in `fb_group_monitor_embed_alert.py`:
```python
HEADLESS_MODE = True    # Change to False for interactive mode
```
Then run:
```bash
python fb_group_monitor_embed_alert.py --monitor
```

**Time to switch:** ~5 seconds ✨

---

### **Method 2: Interactive Menu (No typing)**
Just run:
```bash
python fb_group_monitor_embed_alert.py
```

You'll see:
```
============================================================
FB GROUP MONITOR - QUICK MENU
============================================================

1. Login (save cookies)
2. Monitor (headless mode - 24/7)
3. Monitor (interactive mode - see browser)
4. Exit

Enter choice (1-4): 
```

Press `2` for headless, `3` for interactive.

**Time to switch:** ~3 seconds ⚡

---

### **Method 3: Command Line (For automation)**
```bash
# Headless mode
python fb_group_monitor_embed_alert.py --monitor

# Interactive mode
python fb_group_monitor_embed_alert.py --monitor --headless false

# With specific browser
python fb_group_monitor_embed_alert.py --monitor --headless false --browser chromium
```

**Time to switch:** ~10 seconds

---

## 📊 Comparison

| Method | Speed | Easy | Best For |
|--------|-------|------|----------|
| Edit Config | ⚡⚡⚡ | ✅ | Frequent toggling |
| Menu | ⚡⚡ | ✅✅ | Quick testing |
| CLI Args | ⚡ | ⚠️ | Scripting/automation |

---

## 🎯 Recommended Workflow

1. **For 24/7 Production:**
   - Set `HEADLESS_MODE = True`
   - Run: `python fb_group_monitor_embed_alert.py --monitor`

2. **For Testing/Development:**
   - Set `HEADLESS_MODE = False`
   - Run: `python fb_group_monitor_embed_alert.py --monitor`
   - See browser activity in real-time

3. **For Quick Toggle:**
   - Just press `3` in the menu
   - Or edit config line 65

---

## 📝 Configuration Location

**File:** `fb_group_monitor_embed_alert.py`  
**Line:** 65  
**Variable:** `HEADLESS_MODE`

Change between `True` (headless) and `False` (interactive)

---

## 🔄 Default Behaviors

When running **without arguments**:
```bash
python fb_group_monitor_embed_alert.py
```
→ Shows interactive menu

When running **with --monitor**:
```bash
python fb_group_monitor_embed_alert.py --monitor
```
→ Uses `HEADLESS_MODE` setting (default: True)

When running **with explicit flag**:
```bash
python fb_group_monitor_embed_alert.py --monitor --headless false
```
→ Uses the explicit flag (overrides config)

---

## 🚀 Quick Commands

```bash
# Show menu (fastest interactive way)
python fb_group_monitor_embed_alert.py

# Run headless (use config setting)
python fb_group_monitor_embed_alert.py --monitor

# Run interactive (see browser)
python fb_group_monitor_embed_alert.py --monitor --headless false

# Interactive login
python fb_group_monitor_embed_alert.py --login

# Help
python fb_group_monitor_embed_alert.py --help
```

---

## 💡 Pro Tips

1. **For development:** Set `HEADLESS_MODE = False`, then just run:
   ```bash
   python fb_group_monitor_embed_alert.py --monitor
   ```

2. **For production:** Set `HEADLESS_MODE = True`, then run and forget!

3. **For testing:** Use the interactive menu:
   ```bash
   python fb_group_monitor_embed_alert.py
   # Then press 3 for interactive mode
   ```

---

**Done! Switching between headless and interactive modes is now SUPER fast!** ⚡
