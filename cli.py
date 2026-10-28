"""
cli.py
------
Chế độ giao diện dòng lệnh (Command Line Interface - CLI) cho WiFiLens.
Hiển thị bảng dữ liệu định dạng chuẩn, hỗ trợ màu sắc ANSI và các cờ tham số
giúp tự động hóa hoặc sử dụng trực tiếp trong Terminal.
"""

import argparse
import sys
import time
from typing import List

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from core.analyzer import analyze_channel_congestion
from core.exporter import export_to_csv, export_to_json, export_to_txt_report
from core.scanner import get_current_connection, scan_wifi_networks

# Định nghĩa mã màu ANSI cho Terminal
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RED = "\033[31m"


def print_banner():
    banner = f"""{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║               WIFILENS - TOOL QUÉT & PHÂN TÍCH WI-FI CHUYÊN SÂU              ║
║         (Phát triển cho Lab Mạng Máy Tính & An Toàn Thông Tin)               ║
╚══════════════════════════════════════════════════════════════════════════════╝{RESET}"""
    print(banner)


def display_cli_table(networks: List[dict], current_conn: dict = None):
    if current_conn and current_conn.get("state") == "connected":
        print(f"\n{BOLD}[+] CARD MẠNG:{RESET} {current_conn.get('description')}")
        print(
            f"{BOLD}[+] ĐANG KẾT NỐI:{RESET} {GREEN}{BOLD}{current_conn.get('ssid')}{RESET} ({current_conn.get('bssid')}) "
            f"| Kênh: {current_conn.get('channel')} ({current_conn.get('band')}) "
            f"| Sóng: {current_conn.get('signal_pct')}% ({current_conn.get('rssi_dbm')} dBm) "
            f"| Tốc độ: {current_conn.get('rx_rate_mbps')} Mbps\n"
        )
    else:
        print(f"\n{YELLOW}[!] Máy tính hiện chưa kết nối tới Access Point nào.{RESET}\n")

    print(f"{BOLD}[*] DANH SÁCH CÁC MẠNG LÂN CẬN (TỔNG SỐ: {len(networks)} AP):{RESET}")

    header = (
        f"{'STT':<4} {'SSID':<24} {'BSSID':<18} {'VENDOR':<20} "
        f"{'KÊNH':<6} {'SÓNG':<14} {'CHUẨN':<12} {'TỐC ĐỘ':<10} {'BẢO MẬT'}"
    )
    print(f"{BLUE}{header}{RESET}")
    print("-" * 125)

    for idx, net in enumerate(networks, start=1):
        is_conn = net.get("is_connected", False)
        ssid = net.get("ssid", "")
        if is_conn:
            ssid = f"[*] {ssid}"
        ssid = ssid[:23]

        bssid = net.get("bssid", "")
        vendor = net.get("vendor", "")[:19]
        ch = f"{net.get('channel', 0)} ({net.get('band', '').replace(' GHz', 'G')})"
        sig_pct = net.get("signal_pct", 0)
        dbm = net.get("rssi_dbm", -100)
        sig_str = f"{sig_pct}% ({dbm}dBm)"

        gen = net.get("wifi_generation", "")[:11]
        rate = f"{net.get('max_rate_mbps', 0.0)}M"
        sec = net.get("auth", "")

        # Chọn màu dựa theo sóng và kết nối
        color = RESET
        if is_conn:
            color = GREEN + BOLD
        elif sig_pct >= 70:
            color = CYAN
        elif sig_pct <= 35:
            color = YELLOW

        row = (
            f"{idx:<4} {ssid:<24} {bssid:<18} {vendor:<20} "
            f"{ch:<6} {sig_str:<14} {gen:<12} {rate:<10} {sec}"
        )
        print(f"{color}{row}{RESET}")

    print("-" * 125)


def run_cli_mode(args):
    print_banner()

    if args.continuous:
        interval = max(2, args.interval)
        print(f"{CYAN}[i] Bắt đầu chế độ quét liên tục (Mỗi {interval} giây). Nhấn Ctrl+C để dừng.{RESET}")
        try:
            while True:
                conn = get_current_connection()
                nets = scan_wifi_networks(trigger_hardware=True)
                display_cli_table(nets, conn)
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] Đã dừng quét liên tục.{RESET}")
            return

    # Quét 1 lần
    print(f"{CYAN}[i] Đang quét sóng phần cứng qua WlanScan API...{RESET}")
    conn = get_current_connection()
    nets = scan_wifi_networks(trigger_hardware=True)
    display_cli_table(nets, conn)

    # Phân tích kênh nếu yêu cầu
    if args.analyze:
        analysis = analyze_channel_congestion(nets)
        best_24 = analysis.get("best_channel_24", 1)
        best_5g = analysis.get("best_channels_5g", [])
        print(f"\n{BOLD}{MAGENTA}[*] KẾT QUẢ PHÂN TÍCH KÊNH TỐI ƯU:{RESET}")
        print(f"  - Kênh 2.4 GHz sạch nhất khuyên dùng: {GREEN}{BOLD}KÊNH {best_24}{RESET} (Ít nhiễu ACI/CCI nhất)")
        ch5_str = ", ".join([f"Kênh {c}" for c in best_5g[:4]]) if best_5g else "N/A"
        print(f"  - Kênh 5 GHz thông thoáng khuyên dùng: {GREEN}{BOLD}{ch5_str}{RESET}")

    # Xuất file nếu có tham số
    if args.csv:
        if export_to_csv(nets, args.csv):
            print(f"\n{GREEN}[✓] Đã xuất file CSV thành công:{RESET} {args.csv}")
        else:
            print(f"\n{RED}[✗] Lỗi xuất file CSV.{RESET}")

    if args.json:
        if export_to_json(nets, args.json):
            print(f"\n{GREEN}[✓] Đã xuất file JSON thành công:{RESET} {args.json}")
        else:
            print(f"\n{RED}[✗] Lỗi xuất file JSON.{RESET}")

    if args.report:
        if export_to_txt_report(nets, conn, args.report):
            print(f"\n{GREEN}[✓] Đã tạo báo cáo kiểm định thành công:{RESET} {args.report}")
        else:
            print(f"\n{RED}[✗] Lỗi tạo báo cáo kiểm định.{RESET}")
