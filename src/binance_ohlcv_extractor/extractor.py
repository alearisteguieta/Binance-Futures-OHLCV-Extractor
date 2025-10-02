#!/usr/bin/env python3
"""
Extractor module for Binance USDT-M futures OHLCV.

This module exposes:
- criptodata(symbol, start_date_str, end_date=None, interval="1d", output_dir=".")
  -> pandas.DataFrame

Notes (written content):
- Purpose: provide a deterministic, documented function to fetch and export OHLCV.
- Provenance: prompt_id ffw-2025-10-02-v1 (see prompts/financial_framework_template.md).
- Maintainer: alearisteguieta (add contact in repo-wide CODEOWNERS if desired).
"""

import os
import time
from datetime import datetime, date, timedelta
from typing import List, Optional

import pandas as pd
import requests

MAX_LIMIT = 1000
TIMEFRAME_DEFAULT = "1d"


def _to_millis(dt: datetime) -> int:
    """Convert a datetime to milliseconds since epoch."""
    return int(dt.timestamp() * 1000)


def _parse_klines_response(klines: List[list]) -> pd.DataFrame:
    """
    Convert raw klines (list-of-lists) into a canonical pandas.DataFrame.

    Returns a DataFrame indexed by Date with float columns:
    ['open', 'high', 'low', 'close', 'volume']
    """
    df = pd.DataFrame(
        klines,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "num_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    # Convert and normalize
    df["Date"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    # For CSV readability we provide ISO strings in UTC; DataFrame index is tz-aware (UTC).
    df = df[["Date", "open", "high", "low", "close", "volume"]]
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    df.set_index("Date", inplace=True)
    return df


def _fetch_klines_requests(symbol: str, interval: str, start_ts_ms: int, end_ts_ms: int) -> List[list]:
    """
    Fetch klines using the Binance Futures public REST endpoint with pagination.
    This function returns the raw list-of-lists returned by the API.
    """
    endpoint = "https://fapi.binance.com/fapi/v1/klines"
    all_klines: List[list] = []
    next_start = start_ts_ms
    while True:
        resp = requests.get(
            endpoint,
            params={"symbol": symbol, "interval": interval, "startTime": next_start, "endTime": end_ts_ms, "limit": MAX_LIMIT},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        all_klines.extend(data)
        if len(data) < MAX_LIMIT:
            break
        last_open_time = int(data[-1][0])
        next_start = last_open_time + 1
        time.sleep(0.2)
    return all_klines


def criptodata(
    symbol: str,
    start_date_str: str,
    end_date: Optional[date] = None,
    interval: str = TIMEFRAME_DEFAULT,
    output_dir: str = ".",
) -> pd.DataFrame:
    """
    Orchestrate extraction, parsing and CSV export for a single symbol.

    Returns a pandas.DataFrame indexed by Date (UTC).
    """
    if end_date is None:
        end_date = date.today() - timedelta(days=1)

    # Normalize start/end datetimes (UTC)
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    start_dt_utc = datetime(start_dt.year, start_dt.month, start_dt.day, 0, 0, 0)
    end_dt_utc = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

    start_ms = _to_millis(start_dt_utc)
    end_ms = _to_millis(end_dt_utc)

    raw_klines = _fetch_klines_requests(symbol, interval, start_ms, end_ms)
    if not raw_klines:
        raise RuntimeError(f"No kline data returned for {symbol} between {start_date_str} and {end_date.isoformat()}")

    df = _parse_klines_response(raw_klines)

    # Filter to requested closed window
    df = df[(df.index >= start_dt_utc) & (df.index <= end_dt_utc)]

    # Ensure output directory and write CSV
    os.makedirs(output_dir, exist_ok=True)
    # For CSV we write ISO 8601 UTC timestamps (pandas will include timezone if tz-aware)
    csv_path = os.path.join(output_dir, f"{symbol}.csv")
    df.to_csv(csv_path, index=True, float_format="%.8f")

    return df
