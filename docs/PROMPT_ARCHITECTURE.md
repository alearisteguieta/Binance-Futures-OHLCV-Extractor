# Architecture / Design Notes

- `src/binance_futures_ohlcv/extractor.py` — core extraction functions:
  - `_fetch_klines_requests` (requests-based)
  - `_fetch_klines_connector` (attempt connector)
  - `parse_klines_to_df` — parse raw klines into pandas DataFrame
  - `fetch_symbol_ohlcv` — orchestrates fetching and saving CSV

- `src/binance_futures_ohlcv/cli.py` — CLI wrapper that uses argparse,
  configures logging, and calls `fetch_symbol_ohlcv`.

Logging is used for progress and errors (instead of print statements) to
support production usage and easier testability. See the original
Financial Prompt Framework for requirements used to design the code.
