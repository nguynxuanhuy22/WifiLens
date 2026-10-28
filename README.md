# 📡 WiFiLens Pro - Tool Quét & Phân Tích Mạng Wi-Fi Chuyên Sâu

> **Đề tài Lab:** Tool quét các mạng Wi-Fi lân cận kèm thông số chi tiết  
> **Môn học:** Mạng Máy Tính & An Toàn Thông Tin  
> **Nền tảng:** Windows 10 / Windows 11 | **Ngôn ngữ:** Python 3 (Zero External Dependencies)

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform Windows](https://img.shields.io/badge/Platform-Windows-0078D6.svg)](https://microsoft.com)
[![License MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-brightgreen.svg)]()

---

## 🌟 Điểm Nổi Bật & Tính Năng Vượt Trội

Khác với các đoạn mã mẫu đơn giản trôi nổi trên mạng, **WiFiLens Pro** được thiết kế bài bản theo kiến trúc module sạch (Clean Architecture), kết hợp trực tiếp giữa **Windows Native Wifi API (WlanScan qua ctypes)** và trình phân tích cú pháp nâng cao để cung cấp dữ liệu thời gian thực mà không bị phụ thuộc vào cache cũ của hệ thống:

1. **Quét chủ động phần cứng (Hardware Active Probe):**
   - Gọi trực tiếp hàm `WlanScan` từ thư viện `wlanapi.dll` của Windows để buộc card mạng phát khung *Probe Request* thời gian thực.
2. **Nhận diện nhà sản xuất Router (OUI Database):**
   - Tích hợp từ điển IEEE OUI xác định hãng sản xuất (ZTE, FPT Telecom/Arcadyan, VNPT, Viettel, TP-Link, Asus, Cisco, Apple, Intel, Xiaomi, Huawei...).
   - Hỗ trợ phát hiện bit *Locally Administered* cho các mạng Mesh và Virtual AP.
3. **Phân tích thông số kỹ thuật đa chiều:**
   - SSID (bao gồm phát hiện mạng ẩn `<Hidden SSID>`), BSSID (địa chỉ MAC của AP).
   - Đổi công suất tín hiệu từ `%` sang chuẩn viễn thông `dBm (RSSI)`.
   - Chuẩn hóa thế hệ Wi-Fi: **Wi-Fi 7 (802.11be)**, **Wi-Fi 6/6E (802.11ax)**, **Wi-Fi 5 (802.11ac)**, **Wi-Fi 4 (802.11n)**.
   - Kênh (Channel) & Tần số trung tâm (Center Frequency in MHz).
   - BSS Load: Số lượng thiết bị đang kết nối (Connected Stations) và độ chiếm dụng kênh (% Channel Utilization).
   - Tốc độ truyền tải tối đa lý thuyết (Basic rates & Other rates Mbps).
4. **Trực quan hóa đồ thị phổ sóng (Spectrum Analyzer) bằng Canvas thuần:**
   - Vẽ đường cong năng lượng Parabol mô phỏng độ rộng phổ 20/22 MHz trên kênh 2.4 GHz và 5 GHz.
   - Trực quan hóa hiện tượng chồng lấn kênh (Channel Overlap) và nhiễu sóng.
5. **Đồ thị biến thiên sóng theo thời gian (Signal History Tracker):**
   - Theo dõi độ suy hao tín hiệu (Signal Attenuation) khi di chuyển máy tính hoặc kiểm tra độ ổn định của router.
6. **Thuật toán khuyến nghị kênh tối ưu (Channel Optimization):**
   - Tính toán điểm nhiễu Co-Channel (CCI) và Adjacent Channel (ACI) để tìm kênh sạch nhất (1, 6 hoặc 11).
7. **Đánh giá rủi ro an ninh mạng (Security Audit):**
   - Phân tích chuẩn mã hóa (Open, WEP, WPA-TKIP, WPA2-CCMP/AES, WPA3-SAE, Enterprise).
   - Cảnh báo rủi ro về tấn công Sniffing, Evil Twin AP, Brute-force 4-Way Handshake.
8. **Đa dạng chế độ:**
   - Giao diện đồ họa hiện đại (**Modern GUI**).
   - Giao diện dòng lệnh chuyên nghiệp (**CLI Mode**).
   - Xuất dữ liệu đa định dạng: **CSV**, **JSON**, **Báo cáo kiểm định TXT**.

---

## 🏗️ Kiến Trúc Hệ Thống (Architecture)

```
WiFiLens/
├── core/
│   ├── scanner.py          # Kích hoạt WlanScan API phần cứng & phân tích netsh
│   ├── analyzer.py         # Tính dBm, đánh giá sóng, chuẩn Wi-Fi, thuật toán tính nhiễu kênh
│   ├── oui_db.py           # Cơ sở dữ liệu OUI tra cứu hãng sản xuất Access Point
│   └── exporter.py         # Module xuất dữ liệu (CSV, JSON, Báo cáo TXT)
├── ui/
│   ├── spectrum_canvas.py  # Đồ thị phổ kênh 2.4GHz & 5GHz thuần Tkinter Canvas
│   ├── history_canvas.py   # Đồ thị biến thiên cường độ sóng thời gian thực
│   └── gui_app.py          # Giao diện Cyber Dark hiện đại, đa luồng (Multi-threading)
├── cli.py                  # Giao diện dòng lệnh Terminal với màu sắc ANSI
├── main.py                 # Điểm khởi chạy chính (hỗ trợ chuyển đổi GUI/CLI)
├── requirements.txt        # 100% Python Standard Library (Không cần pip install)
├── README.md               # Tài liệu hướng dẫn & giải thích thông số
└── VIDEO_SCRIPT_GUIDE.md   # Kịch bản quay video thuyết trình kèm mặt cho sinh viên
```

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### Yêu Cầu Tiên Quyết
- Máy tính chạy **Windows 10** hoặc **Windows 11**.
- Đã cài đặt **Python 3.8** trở lên (Khuyến nghị Python 3.10+).
- Card mạng Wi-Fi của máy đang bật.

### 1. Khởi Chạy Giao Diện Đồ Họa (GUI Mode - Khuyến Nghị)
Chỉ cần mở PowerShell hoặc Command Prompt và chạy:
```bash
python main.py
```
*(Giao diện đồ họa Dark Theme sẽ xuất hiện với đầy đủ bảng danh sách, biểu đồ phổ kênh và biểu đồ thời gian thực).*

### 2. Khởi Chạy Chế Độ Dòng Lệnh (CLI Mode)
Quét và in bảng thông số ra Terminal:
```bash
python main.py --cli
```

Quét kèm phân tích kênh sạch nhất và đánh giá bảo mật:
```bash
python main.py --cli --analyze
```

Quét liên tục theo chu kỳ mỗi 3 giây (Live Terminal Monitoring):
```bash
python main.py --cli --continuous --interval 3
```

Xuất kết quả quét ra file CSV, JSON hoặc TXT:
```bash
python main.py --cli --csv report.csv --json output.json --report audit.txt
```

---

## 📖 Bảng Giải Thích Chi Tiết Các Thông Số Kỹ Thuật

| Thông số | Tên đầy đủ / Định dạng | Ý nghĩa kỹ thuật & Ứng dụng thực tế |
| :--- | :--- | :--- |
| **SSID** | *Service Set Identifier* | Tên của mạng Wi-Fi được đặt bởi người quản trị. Nếu mạng bật chế độ ẩn SSID, router sẽ gửi khung Beacon với độ dài chuỗi SSID bằng 0 (Tool nhận diện là `<Hidden Network>`). |
| **BSSID** | *Basic Service Set Identifier* | Địa chỉ MAC 48-bit (6 byte) phần cứng của chip phát sóng (Access Point). Cho phép phân biệt các trạm phát sóng khác nhau trong cùng một hệ thống mạng Mesh hoặc Roaming. |
| **Vendor** | *OUI Manufacturer* | Nhà sản xuất thiết bị router/AP, được giải mã từ 3 byte đầu tiên (OUI) của địa chỉ MAC theo chuẩn IEEE. |
| **Signal (%) & RSSI (dBm)** | *Received Signal Strength Indicator* | Cường độ tín hiệu sóng nhận được tại anten máy client. Giá trị dBm là thang đo logarit (giá trị âm). Càng gần 0 sóng càng mạnh: <br>• **$\ge -50$ dBm (100%):** Xuất sắc (cạnh router) <br>• **$-50 \to -65$ dBm:** Tốt (chơi game, xem 4K) <br>• **$-65 \to -75$ dBm:** Khá (lướt web) <br>• **$< -80$ dBm:** Yếu (nguy cơ rớt mạng). |
| **Channel & Frequency** | Kênh & Tần số trung tâm (MHz) | Dải tần số vô tuyến được ấn định cho kết nối. Ví dụ: Kênh 1 ($2412\text{ MHz}$), Kênh 6 ($2437\text{ MHz}$), Kênh 11 ($2462\text{ MHz}$), Kênh 36 ($5180\text{ MHz}$). |
| **Band** | Băng tần phát sóng | • **2.4 GHz:** Bước sóng dài, đâm xuyên tường tốt, nhưng dễ nhiễu và băng thông thấp. <br>• **5 GHz:** Bước sóng ngắn, suy hao nhanh nhưng băng thông cực lớn, ít bị nhiễu. |
| **Chuẩn Wi-Fi (Radio Type)** | Thế hệ IEEE 802.11 | • **802.11b (Wi-Fi 1):** Tối đa 11 Mbps. <br>• **802.11g (Wi-Fi 3):** Tối đa 54 Mbps. <br>• **802.11n (Wi-Fi 4):** Lên đến 600 Mbps (Hỗ trợ MIMO). <br>• **802.11ac (Wi-Fi 5):** Lên đến 6.9 Gbps (Băng tần 5 GHz, MU-MIMO). <br>• **802.11ax (Wi-Fi 6):** Lên đến 9.6 Gbps (OFDMA, 1024-QAM, tiết kiệm pin TWT). <br>• **802.11be (Wi-Fi 7):** Lên đến 46 Gbps (320 MHz, 4096-QAM, MLO). |
| **Bảo Mật (Authentication)** | Chuẩn xác thực | • **Open:** Không mật khẩu, cực kỳ rủi ro (dữ liệu gửi dạng văn bản thuần). <br>• **WPA2-Personal (CCMP):** Mã hóa AES an toàn, phổ biến nhất hiện nay. <br>• **WPA3-Personal (SAE):** Chuẩn mới nhất, dùng giao thức Dragonfly chống tấn công dò mật khẩu ngoại tuyến (Offline Dictionary Attack). |
| **Mã Hóa (Encryption / Cipher)** | Thuật toán mật mã | • **TKIP:** Cũ, lỗi thời, dễ bị tấn công Michael MIC. <br>• **CCMP / AES:** Mã hóa khối tiêu chuẩn quân đội, an toàn cao. |
| **Max Rate (Mbps)** | Tốc độ truyền tối đa | Tốc độ kết nối dữ liệu vật lý tối đa mà Access Point hỗ trợ theo các tập tốc độ cơ bản (Basic/Other rates). |
| **BSS Load** | Tải của Access Point | • **Connected Stations:** Số thiết bị client đang liên kết với AP. <br>• **Channel Utilization:** Tỷ lệ phần trăm thời gian kênh bị chiếm dụng để truyền tải dữ liệu. |

---

## ⚖️ Giấy Phép & Bản Quyền

Dự án được phát hành dưới giấy phép mã nguồn mở **MIT License**. Mã nguồn được viết mới 100% cho mục đích học tập và nghiên cứu thực nghiệm trong môn học Mạng Máy Tính & An Toàn Thông Tin, tuân thủ nguyên tắc liêm chính học thuật.
