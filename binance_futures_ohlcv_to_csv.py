#!/usr/bin/env python3
"""
Script: binance_futures_ohlcv_to_csv.py
Purpose: Download historical daily candlestick (1d) OHLCV data from Binance USDT-M futures
         for a list of tickers and save one CSV per ticker.
Libraries: binance-connector (if available) OR fallback to requests,
           pandas, datetime, os, time
Usage:   Set environment variables BINANCE_API_KEY and BINANCE_API_SECRET (optional for public endpoints),
         then run: python binance_futures_ohlcv_to_csv.py
Output:  CSV files named <TICKER>.csv (e.g. BTCUSDT.csv)
"""

import os
import time
import math
import json
from datetime import datetime, date, timedelta
import pandas as pd

# We'll attempt to use the official binance-connector if installed, but fall back to direct REST calls
# to the Binance futures klines endpoint if it's not available. This keeps the script robust across setups.
try:
    # Newer binance connector exposes modular clients; Spot shown below is an example for spot,
    # but for futures we'll use the public REST endpoint directly if futures client isn't available.
    from binance.spot import Spot # type: ignore
    BINANCE_CONNECTOR_AVAILABLE = True
except Exception:
    BINANCE_CONNECTOR_AVAILABLE = False

# If you prefer to force use of requests (no connector), set this to True
_FORCE_REQUESTS_FALLBACK = False

# Binance Futures (USDT-M) public REST klines endpoint
FAPI_KLINES_ENDPOINT = "https://fapi.binance.com/fapi/v1/klines"

# Default configuration required by the user
DEFAULT_TICKERS = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT"]
TIMEFRAME = "1d"  # daily
START_DATE_STR = "2021-01-01"  # inclusive

# Limit per request (Binance allows up to 1000 per request)
MAX_LIMIT = 1000


def _ensure_api_keys():
    """
    Read API keys from environment variables for secure handling.
    If they are not found this function returns None, None. Public endpoints don't require them.
    """
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")
    return api_key, api_secret


def _to_millis(dt: datetime) -> int:
    """Convert a datetime (aware or naive UTC) to milliseconds since epoch."""
    return int(dt.timestamp() * 1000)


def _parse_klines_response(klines):
    """
    Parse raw klines (list of lists) into a pandas.DataFrame with the columns:
    Date (datetime), Open, High, Low, Close, Volume
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

    # Convert types and keep only the requested columns
    df["Date"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_convert(None)
    df = df[["Date", "open", "high", "low", "close", "volume"]]
    # Convert numeric columns to floats
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    # Set Date as index
    df.set_index("Date", inplace=True)
    return df


def _fetch_klines_requests(symbol: str, interval: str, start_ts_ms: int, end_ts_ms: int):
    """
    Fetch klines using direct requests to Binance Futures (fapi) endpoint.
    Handles pagination by repeatedly requesting up to MAX_LIMIT bars until end_ts_ms is reached.
    Returns a list of raw klines (each is a list).
    """
    import requests

    all_klines = []
    limit = MAX_LIMIT
    next_start = start_ts_ms

    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": next_start,
            "endTime": end_ts_ms,
            "limit": limit,
        }
        resp = requests.get(FAPI_KLINES_ENDPOINT, params=params, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code} error fetching klines for {symbol}: {resp.text}")
        data = resp.json()
        if not data:
            break

        all_klines.extend(data)

        # If we received less than limit, we've reached the end
        if len(data) < limit:
            break

        # Otherwise, advance next_start to the open time of the last candle + 1 ms to avoid overlap
        last_open_time = int(data[-1][0])
        next_start = last_open_time + 1

        # Safety: avoid infinite loops
        time.sleep(0.2)

    return all_klines


def _fetch_klines_connector(symbol: str, interval: str, start_ts_ms: int, end_ts_ms: int):
    """
    Try to fetch klines using binance-connector (if available).
    This function attempts to use any available futures/spot klines helper; if not supported it raises.
    NOTE: binance-connector modular API can vary; for portability we prefer direct REST fallback above.
    """
    # Many connector variants provide multiple clients. We'll try common ones gracefully.
    # If any call fails, raise an exception to let the caller fallback.
    try:
        # Spot client can fetch klines for many endpoints, but for futures we use fapi endpoint directly.
        client = Spot() # type: ignore
        # Spot.klines() calls the spot endpoint; futures data is on fapi - so this may not work for futures.
        # Try to call a generic "klines" method which some connector versions expose.
        if hasattr(client, "klines"):
            # Request in chunks if needed: many connectors accept limit/startTime/endTime
            return client.klines(symbol, interval, startTime=start_ts_ms, endTime=end_ts_ms, limit=MAX_LIMIT)
    except Exception:
        raise

    raise RuntimeError("binance-connector is installed but klines for futures not accessible via connector in this environment.")


def criptodata(symbol: str, start_date_str: str = START_DATE_STR, end_date: date = None, interval: str = TIMEFRAME, output_dir: str = "."):
    """
    Main function to extract historical OHLCV for a single symbol from Binance USDT-M futures,
    convert timestamp to readable Date index and save to CSV.

    Parameters:
        - symbol: ticker string, e.g. 'BTCUSDT'
        - start_date_str: start date (inclusive) as 'YYYY-MM-DD' (default 2021-01-01)
        - end_date: python.date object for the final inclusive date. If None, defaults to yesterday.
        - interval: klines interval (default '1d')
        - output_dir: directory where CSV files will be saved
    Returns:
        - pandas.DataFrame with Date as index and columns [open, high, low, close, volume]
    """
    # Determine end date (yesterday if not provided)
    if end_date is None:
        end_date = date.today() - timedelta(days=1)

    # Convert to datetimes in UTC
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    # interpret start as start of day UTC
    start_dt_utc = datetime(start_dt.year, start_dt.month, start_dt.day, 0, 0, 0)
    # end as end of day UTC
    end_dt_utc = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

    start_ms = _to_millis(start_dt_utc)
    end_ms = _to_millis(end_dt_utc)

    raw_klines = None

    # If connector is available and not forced off, attempt to use it (best-effort)
    if BINANCE_CONNECTOR_AVAILABLE and not _FORCE_REQUESTS_FALLBACK:
        try:
            raw_klines = _fetch_klines_connector(symbol, interval, start_ms, end_ms)
        except Exception:
            # Fall back silently to requests-based approach (robustness)
            raw_klines = None

    # Fallback to direct requests if connector not available or failed
    if raw_klines is None:
        raw_klines = _fetch_klines_requests(symbol, interval, start_ms, end_ms)

    if not raw_klines:
        raise RuntimeError(f"No kline data returned for {symbol} between {start_date_str} and {end_date.isoformat()}.")

    # Parse and convert to DataFrame
    df = _parse_klines_response(raw_klines)

    # Ensure the DataFrame covers the requested date range (there may be missing days if symbol unlisted)
    # Keep only rows within our start and end datetimes (inclusive)
    df = df[(df.index >= start_dt_utc) & (df.index <= end_dt_utc)]

    # Save CSV file
    os.makedirs(output_dir, exist_ok=True)
    csv_filename = os.path.join(output_dir, f"{symbol}.csv")
    df.to_csv(csv_filename, index=True, float_format="%.8f")

    # Return the DataFrame for further processing or validation
    return df


if __name__ == "__main__":
    # Entry point: process the provided list of tickers
    api_key, api_secret = _ensure_api_keys()
    if api_key and api_secret:
        # If keys exist we could instantiate connector clients that require auth; currently the script
        # uses public futures klines endpoint which does not require authentication.
        pass # kept for future extension where auth is needed

    tickers = DEFAULT_TICKERS.copy()
    output_directory = "binance_futures_csvs"

    print(f"Starting data extraction for tickers: {', '.join(tickers)}")
    print(f"Timeframe: {TIMEFRAME}, start date: {START_DATE_STR}, end date: {(date.today() - timedelta(days=1)).isoformat()}")

    for t in tickers:
        try:
            print(f"Downloading {t} ...")
            df_t = criptodata(t, start_date_str=START_DATE_STR, interval=TIMEFRAME, output_dir=output_directory)
            print(f"  -> {t}: {len(df_t)} rows saved to {os.path.join(output_directory, t + '.csv')}")
            # small pause to be gentle with API rate limits
            time.sleep(0.3)
        except Exception as e:
            print(f"Error processing {t}: {e}")

    print("Data extraction finished :)")
