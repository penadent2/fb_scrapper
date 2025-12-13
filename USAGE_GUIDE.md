# Facebook Group Monitor - Hướng Dẫn Sử Dụng

## Cách Hoạt Động Mới

Script đã được cập nhật để hoạt động theo cách **đơn giản và ổn định hơn**:

1. **Đăng nhập 1 lần** khi khởi động script
2. **Giữ browser mở** và session luôn hoạt động
3. **Liên tục quét** các Facebook groups từ session đó
4. **Không cần lưu/load cookies** nữa - session tự động duy trì

## Cách Sử Dụng

### Chạy với Menu Tương Tác (Đơn Giản Nhất)

```bash
py fb_group_monitor_embed_alert.py
```

Sau đó chọn:
- **Option 1**: Chạy monitor với chế độ headless (ẩn browser)
- **Option 2**: Chạy monitor với browser hiển thị (để debug)

### Chạy Trực Tiếp

#### Chế độ hiển thị browser (Khuyến nghị cho lần đầu)

```bash
py fb_group_monitor_embed_alert.py --headless false
```

#### Chế độ headless (Chạy ngầm 24/7)

```bash
py fb_group_monitor_embed_alert.py --monitor
```

hoặc

```bash
py fb_group_monitor_embed_alert.py --headless true
```

## Quy Trình Hoạt Động

1. **Khởi động script** bằng một trong các lệnh trên
2. **Browser tự động mở** và vào Facebook
3. **Đăng nhập vào Facebook** trong cửa sổ browser (nếu chưa đăng nhập)
4. **Đợi 5-10 giây** để script phát hiện bạn đã đăng nhập
5. **Monitor tự động bắt đầu** quét các groups
6. **Giữ script chạy** - browser sẽ mở và session luôn hoạt động

## Cấu Hình

Chỉnh sửa các thông số trong file `fb_group_monitor_embed_alert.py`:

```python
# Danh sách groups cần theo dõi
GROUPS = [
    "https://www.facebook.com/groups/genshinimpactvnmbvct/",
    "https://www.facebook.com/groups/6911770178952785/",
    # Thêm groups khác...
]

# Từ khóa cần tìm
KEYWORDS = [
    "cần giúp", "giúp với", "hỗ trợ", "fix", "bị lỗi",
    "tuyển", "cần người", "tìm người", "bán", "mua",
]

# Discord webhooks
DISCORD_WEBHOOK_POST = "your_webhook_url_here"
DISCORD_WEBHOOK_ALERT = "your_alert_webhook_url_here"

# Chế độ headless mặc định
HEADLESS_MODE = True  # True = ẩn browser, False = hiển thị browser

# Thời gian quét (phút)
CHECK_INTERVAL_MINUTES = 1

# Chỉ lấy bài đăng trong X giờ gần đây
ONLY_POST_LAST_HOURS = 6
```

## Ưu Điểm Của Cách Mới

✅ **Đơn giản hơn**: Không cần chạy 2 lần (login + monitor)
✅ **Ổn định hơn**: Session luôn hoạt động, không bị hết hạn cookies
✅ **Dễ debug**: Có thể xem browser đang làm gì
✅ **Tự động phát hiện login**: Không cần nhấn Enter hay làm gì thêm
✅ **Auto-restart**: Nếu bạn tắt browser, script sẽ tự động mở lại và yêu cầu login lại

## Lưu Ý

- **Headless mode**: Facebook có thể phát hiện và yêu cầu xác thực thêm
- **Khuyến nghị**: Chạy với `--headless false` để ổn định nhất
- **Session timeout**: Nếu Facebook yêu cầu login lại, script sẽ tự động dừng và thông báo
- **Auto-restart**: Nếu bạn tắt browser thủ công, script sẽ tự động mở lại sau 5 giây
- **Ctrl+C**: Nhấn để dừng script hoàn toàn (không restart nữa)

## Troubleshooting

### Script báo "Login required" mặc dù đã login?

- Đợi thêm 5-10 giây sau khi login
- Đảm bảo bạn đã vào được Facebook feed (không còn ở trang login)
- Thử chạy lại với `--headless false`

### Browser không mở?

- Kiểm tra Playwright đã cài đặt: `py -m playwright install`
- Thử đổi browser: `--browser chromium` hoặc `--browser chrome`

### Monitor không tìm thấy bài đăng?

- Kiểm tra KEYWORDS có đúng không
- Kiểm tra ONLY_POST_LAST_HOURS (mặc định 6 giờ)
- Xem log để biết có bài nào match không

