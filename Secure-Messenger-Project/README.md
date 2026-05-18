# 🔐 SECURE MESSENGER

> **End-to-End Encrypted Platform — Threat-aware Secure Messaging Simulator**

---

## Giới thiệu

**Secure Messenger** là một ứng dụng web mô phỏng hệ thống nhắn tin bảo mật đầu-cuối (End-to-End Encryption), được xây dựng nhằm minh họa các khái niệm mật mã học hiện đại và các kịch bản tấn công thực tế theo góc nhìn của hacker.

Dự án kết hợp giữa giao diện chat trực quan và bảng điều khiển kỹ thuật (Ratchet Monitor), cho phép người dùng quan sát toàn bộ luồng mã hóa — từ bắt tay khóa Diffie-Hellman, mã hóa AES-256, kiểm tra toàn vẹn SHA-256, cho đến mô phỏng tấn công XSS và chiếm đoạt tài khoản.

---

## Tính năng chính

| Tính năng | Mô tả |
|---|---|
| **Diffie-Hellman Handshake** | Trao đổi khóa bí mật giữa Alice và Bob (DH-256) |
| **AES-256 Encryption** | Mã hóa tin nhắn bằng thuật toán AES-256 tiêu chuẩn |
| **Vigenère Cipher** | Lựa chọn mã hóa thay thế bằng mật mã Vigenère |
| **SHA-256 Integrity** | Xác minh toàn vẹn nội dung tin nhắn |
| **Ratchet Monitor** | Giám sát cơ chế Double Ratchet theo thời gian thực |
| **Hacker Console** | Mô phỏng tấn công XSS và chiếm đoạt phiên đăng nhập |
| **Giao diện Chat 3 cột** | Chat song song Alice — Ratchet Monitor — Bob |
| **Danh sách bạn bè** | Nhắn tin với 8 người bạn, hỗ trợ mã hóa và gửi ảnh |
| **Gửi hình ảnh** | Tải và gửi ảnh trong cuộc trò chuyện |
| **Quản lý tài khoản** | Đổi tên, email, avatar; xem thống kê và huy hiệu |
| **Song ngữ (VI / EN)** | Chuyển đổi ngôn ngữ Việt — Anh toàn bộ giao diện |
| **Light / Dark Theme** | Giao diện sáng / tối chuyển đổi tức thì |
| **Seen & Typing Indicator** | Thông báo "đã xem" và bong bóng đang nhập |
| **Splash Screen** | Màn hình khởi động cinematic với hiệu ứng code rain |
| **Parallax Background** | Nền chuyển động 3D theo con trỏ chuột |
| **Firebase Realtime DB** | Đồng bộ tin nhắn thời gian thực qua Firebase |

---

## Hướng dẫn sử dụng (Tutorial)

Ứng dụng tích hợp **hướng dẫn tương tác** (powered by [Driver.js](https://driverjs.com/)) giúp người dùng làm quen với toàn bộ tính năng chỉ trong vài bước. Nhấn nút ❓ trên thanh điều hướng để khởi động tour.

> ⚠️ **Lưu ý quan trọng:**  
> Phiên bản cải tiến độc lập (Personal Refactored Version)
Sau khi hoàn thành môn học cùng nhóm, tôi đã tiến hành tối ưu hóa và nâng cấp độc lập mã nguồn dự án với các hạng mục:
- **Tái cấu trúc mã nguồn sạch (Clean Architecture):** Bóc tách hoàn toàn hàng ngàn dòng code JavaScript và CSS lộn xộn từ file gốc `index.html` vào các file module riêng biệt (`js/script.js` và `css/style.css`), giúp dự án đạt chuẩn công nghiệp.
- **Dọn dẹp & Tối ưu:** Tìm và giải quyết triệt để các lỗi lặp hàm, ghi đè biến và xung đột CSS tồn đọng từ bản làm nhóm.
- **Nâng cấp Tutorial Tour:** Chỉnh sửa luồng tương tác của `driver.js`
---

## Công nghệ sử dụng

- **HTML5 / CSS3 / JavaScript (ES Modules)**
- **CryptoJS 4.1.1** — AES-256, SHA-256 encryption
- **Firebase Realtime Database** — Đồng bộ tin nhắn
- **Driver.js 1.0.1** — Tour tương tác
- **Font Awesome 6** — Icon set
- **Google Fonts** — Quicksand, JetBrains Mono

---

## Cách chạy

1. Clone hoặc tải project về máy.
2. Đảm bảo có kết nối Internet (Firebase + CDN).
3. Mở file `index.html` bằng trình duyệt hiện đại (Chrome, Edge, Firefox).
4. Đợi splash screen khởi tải (~3.6 giây), sau đó bắt đầu trải nghiệm.

> Không cần cài đặt thêm bất kỳ phụ thuộc nào — toàn bộ thư viện được tải qua CDN.

---

## Cấu trúc dự án

```
secure-messenger/
├── index.html        # Giao diện chính — toàn bộ cấu trúc trang
├── css/
│   └── style.css     # Toàn bộ stylesheet (theme, animation, layout)
└── js/
    └── script.js     # Logic mã hóa, Firebase, UI, Tour, i18n
```

---

## Đội ngũ dự án

| # | Họ và tên | Vai trò | Nhiệm vụ |
|---|---|---|---|
| 1 | **Đinh Kỳ Vĩ** | Nhóm trưởng | Đề xuất ý tưởng và xây dựng luồng xử lý chính; Phát triển giao diện demo; Tối ưu thuật toán mã hóa |
| 2 | **Nguyễn Ngọc Hồng Đào** | Thành viên | Tinh chỉnh giao diện người dùng (UI/UX); Nghiên cứu và tích hợp tính năng; Quản lý nội dung hiển thị |
| 3 | **Nguyễn Duy Bảo Trân** | Thành viên | Xây dựng bản demo kỹ thuật (PoC) bằng Java; Lập trình tính năng mở rộng; Phát triển Web Modules |
| 4 | **Nguyễn Bùi Minh Hằng** | Thành viên | Thực hiện kiểm thử xâm nhập (Pen-test); Mô phỏng các kịch bản tấn công để kiểm tra hệ thống |
| 5 | **Nguyễn Thị Sang** | Thành viên | Có tham gia |
| 6 | **Đặng Hồng Nguyệt** | Thành viên | Có tham gia |
| 7 | **Hoàng Thị Kim Ngân** | Thành viên | Có tham gia |
| 8 | **Nguyễn Thanh Huyền** | Thành viên | Có tham gia |
| 9 | **Nguyễn Phan Thanh Lịch** | Thành viên | Có tham gia |

---

## Bản quyền

Dự án được phát triển phục vụ mục đích học thuật và nghiên cứu về bảo mật thông tin.  
© 2026 Secure Messenger Team. All rights reserved.
