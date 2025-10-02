#!/usr/bin/env python3
"""
CLI entrypoint for the Binance USDT-M OHLCV extractor.

Usage example:
  python -m binance_ohlcv_extractor.cli --symbols BTCUSDT ETHUSDT --start 2021-01-01 --interval 1d --out ./binance_futures_csvs

Notes (written content):
- This module is a thin wrapper around extractor.criptodata().
- It normalizes CLI input and prints user-facing progress messages.
- Provenance: generated/edited to include a module docstring on 2025-10-02.
"""

import argparse
from datetime import date
from typing import List, Optional

from .extractor import criptodata


def main() -> None:
    p = argparse.ArgumentParser(description="Binance USDT-M OHLCV extractor (CSV per symbol)")

    p.add_argument("--symbols", nargs="+", required=True, help="Symbols, e.g. BTCUSDT ETHUSDT")
    p.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    p.add_argument("--end", help="End date YYYY-MM-DD (defaults to yesterday)")
    p.add_argument("--interval", default="1d", help="Kline interval, e.g. 1m 5m 1h 4h 1d")
    p.add_argument("--out", default="./binance_futures_csvs", help="Output directory")
    p.add_argument("--force-requests", action="store_true", help="Bypass connector and use REST")
    args = p.parse_args()

    end_d: Optional[date] = None
    if args.end:
        y, m, d = [int(x) for x in args.end.split("-")]
        end_d = date(y, m, d)

    print(f"Starting extraction for: {', '.join(args.symbols)}")
    for s in args.symbols:
        try:
            df = criptodata(s, start_date_str=args.start, end_date=end_d, interval=args.interval, output_dir=args.out)
            print(f"  -> {s}: {len(df)} rows")
        except Exception as e:
            print(f"Error for {s}: {e}")

    print("Data extraction finished :)")


if __name__ == "__main__":
    main()
