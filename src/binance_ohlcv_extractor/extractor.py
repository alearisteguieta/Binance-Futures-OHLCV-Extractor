import os
import time
from datetime import datetime, date, timedelta
from typing import List, Optional

import pandas as pd
import requests

MAX_LIMIT = 1000
TIMEFRAME_DEFAULT = "1d"
​
def _to_millis(dt: datetime) -> int:
return int(dt.timestamp() * 1000)
def _parse_klines_response(klines: List[list]) -> pd.DataFrame:
df = pd.DataFrame(
klines,
columns=[
"open_time", "open", "high", "low", "close", "volume",
"close_time", "quote_asset_volume", "num_trades",
"taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore",
],
)
df["Date"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_convert(None)
df = df[["Date", "open", "high", "low", "close", "volume"]]
df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
df.set_index("Date", inplace=True)
return df
def _fetch_klines_requests(symbol: str, interval: str, start_ts_ms: int, end_ts_ms: int) -> List[list]:
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
if end_date is None:
end_date = date.today() - timedelta(days=1)
start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
start_dt_utc = datetime(start_dt.year, start_dt.month, start_dt.day, 0, 0, 0)
end_dt_utc = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
start_ms = _to_millis(start_dt_utc)
end_ms = _to_millis(end_dt_utc)
raw_klines = _fetch_klines_requests(symbol, interval, start_ms, end_ms)
if not raw_klines:
raise RuntimeError(f"No kline data returned for {symbol} between {start_date_str} and {end_date.isoformat()}")
df = _parse_klines_response(raw_klines)
df = df[(df.index >= start_dt_utc) & (df.index <= end_dt_utc)]
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, f"{symbol}.csv"), index=True, float_format="%.8f")
return df
