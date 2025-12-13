# Hướng Dẫn Xử Lý Facebook Checkpoint

## Checkpoint Là Gì?

Facebook checkpoint là cơ chế bảo mật khi Facebook phát hiện:
- Hoạt động bất thường
- Đăng nhập từ thiết bị mới
- Automation/bot behavior
- Truy cập quá nhiều trang trong thời gian ngắn

## Khi Nào Checkpoint Xuất Hiện?

Trong script này, checkpoint thường xuất hiện khi:
1. **Lần đầu chạy script** - Facebook chưa tin tưởng browser
2. **Chạy headless mode** - Facebook dễ phát hiện automation
3. **Quét quá nhanh** - Truy cập nhiều groups trong thời gian ngắn
4. **IP mới hoặc VPN** - Facebook nghi ngờ hoạt động bất thường

## Cách Script Xử Lý Checkpoint

### 1. Phát Hiện Tự Động
Script tự động phát hiện khi Facebook yêu cầu checkpoint:
```
⚠️  FACEBOOK CHECKPOINT/LOGIN REQUIRED
Facebook is asking for verification when opening: [URL]
```

### 2. Tạm Dừng Để Bạn Xử Lý
- Script tự động **dừng 2 phút** để bạn xử lý
- Browser vẫn mở, bạn có thể tương tác
- Hoàn thành checkpoint trong browser

### 3. Tự Động Thử Lại
- Sau 2 phút, script tự động reload trang
- Nếu checkpoint đã xong → Tiếp tục quét
- Nếu vẫn còn checkpoint → Skip group đó

### 4. Thông Báo Discord
Script gửi alert đến Discord webhook:
```
⚠️ Facebook checkpoint required when opening [URL]
Please check the browser and complete verification.
```

## Cách Xử Lý Checkpoint

### Bước 1: Khi Thấy Thông Báo
```
⚠️  FACEBOOK CHECKPOINT/LOGIN REQUIRED
Please complete the checkpoint in the browser window:
1. Complete any security checks
2. Verify your identity if asked
3. Wait until you can see the group page

Monitor will pause for 2 minutes to let you complete this.
```

### Bước 2: Mở Browser
- Browser đang mở, chuyển sang cửa sổ browser
- Bạn sẽ thấy trang checkpoint của Facebook

### Bước 3: Hoàn Thành Checkpoint
Tùy loại checkpoint, bạn có thể cần:

**A. Xác Thực Danh Tính**
- Nhập mật khẩu lại
- Nhập mã OTP từ SMS/Email
- Xác nhận qua ứng dụng Facebook

**B. Xác Nhận Thiết Bị**
- Chọn "This is my device"
- Đặt tên cho thiết bị
- Cho phép lưu thiết bị

**C. Xác Minh Bảo Mật**
- Trả lời câu hỏi bảo mật
- Xác nhận bạn bè
- Upload ảnh chứng minh thư (hiếm khi)

**D. Captcha**
- Chọn hình ảnh theo yêu cầu
- Nhập mã captcha

### Bước 4: Đợi Script Tiếp Tục
- Sau khi hoàn thành checkpoint
- Đợi script tự động reload (tối đa 2 phút)
- Script sẽ kiểm tra và tiếp tục quét

## Mẹo Tránh Checkpoint

### 1. Chạy Ở Chế Độ Visible (Không Headless)
```bash
py fb_group_monitor_embed_alert.py --headless false
```
✅ Facebook khó phát hiện hơn
✅ Bạn có thể xem và xử lý checkpoint ngay

### 2. Giảm Tần Suất Quét
Trong file `fb_group_monitor_embed_alert.py`:
```python
CHECK_INTERVAL_MINUTES = 5  # Thay vì 1 phút
```

### 3. Giảm Số Lượng Groups
Quét ít groups hơn để giảm tải:
```python
GROUPS = [
    "https://www.facebook.com/groups/group1/",
    # Comment out các groups khác
]
```

### 4. Tăng Thời Gian Scroll
```python
SCROLL_DELAY = 3  # Thay vì 2 giây
MAX_SCROLL = 3    # Thay vì 5 lần
```

### 5. Sử dụng Account Đã Tin Cậy
- Dùng account Facebook đã lâu năm
- Account đã xác thực email/số điện thoại
- Account có hoạt động thường xuyên

### 6. Chạy Vào Giờ Bình Thường
- Tránh chạy lúc nửa đêm
- Chạy vào giờ hành chính (9h-17h)
- Giống hành vi người dùng thật

## Cấu Hình Checkpoint Wait Time

Bạn có thể thay đổi thời gian chờ checkpoint:

```python
# Trong fb_group_monitor_embed_alert.py
CHECKPOINT_WAIT_TIME = 120  # 2 phút (mặc định)

# Tăng lên nếu bạn cần nhiều thời gian hơn
CHECKPOINT_WAIT_TIME = 300  # 5 phút
```

## Troubleshooting

### Vấn Đề: Checkpoint Xuất Hiện Liên Tục
**Nguyên nhân**: Facebook đang nghi ngờ account
**Giải pháp**:
1. Dừng script 1-2 giờ
2. Đăng nhập Facebook bình thường, lướt feed
3. Chạy lại với `--headless false`
4. Giảm tần suất quét

### Vấn Đề: Không Đủ Thời Gian Xử Lý
**Giải pháp**: Tăng `CHECKPOINT_WAIT_TIME` lên 5-10 phút

### Vấn Đề: Script Spam Alerts
**Nguyên nhân**: Cooldown quá ngắn
**Giải pháp**: Tăng `ALERT_COOLDOWN`:
```python
ALERT_COOLDOWN = 60 * 60  # 1 giờ thay vì 30 phút
```

### Vấn Đề: Account Bị Khóa
**Nguyên nhân**: Chạy quá nhiều, Facebook phát hiện bot
**Giải pháp**:
1. Dừng script ngay
2. Đăng nhập Facebook web bình thường
3. Hoàn thành các bước xác minh
4. Đợi 24-48 giờ trước khi chạy lại
5. Chạy với cấu hình nhẹ nhàng hơn

## Kết Luận

- ✅ Script có cơ chế xử lý checkpoint tự động
- ✅ Bạn có 2 phút để xử lý checkpoint
- ✅ Có thể tùy chỉnh thời gian chờ
- ✅ Chạy visible mode để dễ xử lý hơn
- ⚠️ Nếu checkpoint xuất hiện quá nhiều, giảm tần suất quét

