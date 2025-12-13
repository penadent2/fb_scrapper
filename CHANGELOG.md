# Changelog - Facebook Group Monitor

## Version 2.0 - Persistent Session Mode (2024-12-13)

### 🎯 Major Changes

#### Cách Hoạt Động Mới
- **Trước**: Phải chạy `--login` để lưu cookies, sau đó chạy `--monitor` để load cookies
- **Bây giờ**: Chỉ cần chạy `--monitor`, browser mở và giữ session liên tục

#### Tính Năng Mới

1. **Persistent Login Session**
   - Đăng nhập 1 lần khi khởi động
   - Browser giữ mở và session luôn hoạt động
   - Không cần lưu/load cookies nữa

2. **Auto-Restart**
   - Nếu bạn tắt browser thủ công, script tự động mở lại sau 5 giây
   - Tự động yêu cầu login lại
   - Chỉ dừng hoàn toàn khi nhấn Ctrl+C

3. **Tự Động Phát Hiện Login**
   - Script tự động phát hiện khi bạn đã login thành công
   - Không cần nhấn Enter hay làm gì thêm
   - Tự động bắt đầu monitor sau khi login

4. **Browser Alive Detection**
   - Kiểm tra browser/page có còn hoạt động không
   - Tự động xử lý khi browser bị đóng
   - Thông báo rõ ràng khi có vấn đề

### 🔧 Technical Improvements

1. **Anti-Detection**
   - Thêm user agent tùy chỉnh
   - Thêm viewport settings
   - Thêm locale và timezone
   - Sử dụng new headless mode (harder to detect)

2. **Error Handling**
   - Xử lý khi browser bị đóng thủ công
   - Xử lý khi session hết hạn
   - Tự động retry khi có lỗi

3. **Code Cleanup**
   - Loại bỏ chế độ `--login` riêng (không cần nữa)
   - Đơn giản hóa menu
   - Cải thiện logging và debug messages

### 📝 Breaking Changes

- **Removed**: `--login` flag (không cần nữa)
- **Changed**: Mặc định sẽ chạy monitor với auto-restart
- **Changed**: Menu chỉ còn 2 options thay vì 3

### 🚀 Usage Changes

**Trước:**
```bash
# Bước 1: Login
py fb_group_monitor_embed_alert.py --login

# Bước 2: Monitor
py fb_group_monitor_embed_alert.py --monitor
```

**Bây giờ:**
```bash
# Chỉ cần 1 lệnh
py fb_group_monitor_embed_alert.py --headless false
```

### 📚 New Files

- `USAGE_GUIDE.md`: Hướng dẫn sử dụng chi tiết
- `CHANGELOG.md`: File này
- `test_login.py`: Script test login đơn giản (có thể xóa)

### 🐛 Bug Fixes

- Fixed: Cookies hết hạn sau một thời gian
- Fixed: Headless mode bị Facebook phát hiện
- Fixed: Script không tự động restart khi browser đóng
- Fixed: Không có thông báo rõ ràng khi cần login

### ⚠️ Known Issues

- Headless mode vẫn có thể bị Facebook phát hiện trong một số trường hợp
- Khuyến nghị chạy với `--headless false` để ổn định nhất

### 🔜 Future Improvements

- [ ] Thêm option để disable auto-restart
- [ ] Thêm retry logic khi Facebook yêu cầu captcha
- [ ] Thêm support cho multiple accounts
- [ ] Thêm web UI để quản lý monitor

