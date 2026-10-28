"""
main.py
-------
Điểm khởi chạy chính (Entry Point) của phần mềm WiFiLens.
Hỗ trợ cả 2 chế độ:
- Chế độ Giao diện Đồ họa (GUI): python main.py (hoặc python main.py --gui)
- Chế độ Dòng lệnh (CLI): python main.py --cli
"""

import argparse
import sys

# Đảm bảo mã hóa UTF-8 cho console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="WiFiLens Pro - Công cụ Quét và Phân tích Mạng Wi-Fi Chuyên Sâu",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--cli",
        action="store_true",
        help="Chạy ở chế độ giao diện dòng lệnh (Command Line Interface)",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Phân tích độ nghẽn kênh và khuyến nghị kênh tối ưu (Chỉ áp dụng với --cli)",
    )
    parser.add_argument(
        "--continuous", "-c",
        action="store_true",
        help="Quét liên tục theo chu kỳ (Chỉ áp dụng với --cli)",
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=3,
        help="Khoảng thời gian quét lại tính bằng giây (Mặc định: 3)",
    )
    parser.add_argument(
        "--csv",
        type=str,
        metavar="FILEPATH",
        help="Xuất kết quả quét ra file CSV (Ví dụ: --csv report.csv)",
    )
    parser.add_argument(
        "--json",
        type=str,
        metavar="FILEPATH",
        help="Xuất kết quả quét ra file JSON (Ví dụ: --json output.json)",
    )
    parser.add_argument(
        "--report",
        type=str,
        metavar="FILEPATH",
        help="Tạo file báo cáo kiểm định văn bản tổng quan (Ví dụ: --report audit.txt)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.cli or args.continuous or args.analyze or args.csv or args.json or args.report:
        # Chạy chế độ CLI
        from cli import run_cli_mode
        run_cli_mode(args)
    else:
        # Chạy chế độ GUI mặc định
        try:
            from ui.gui_app import WiFiLensApp
            app = WiFiLensApp()
            app.mainloop()
        except Exception as e:
            print(f"[!] Không thể mở giao diện GUI (Lỗi: {e}). Chuyển sang chế độ CLI...")
            from cli import run_cli_mode
            args.analyze = True
            run_cli_mode(args)


if __name__ == "__main__":
    main()
