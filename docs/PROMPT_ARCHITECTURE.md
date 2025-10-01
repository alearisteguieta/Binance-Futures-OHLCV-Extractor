# Prompt‑Driven Architecture and Dependency‑Fallback Design

## Scope

This document explains how prompt requirements shaped the code structure, why reliability is a first‑class concern, and how the connector→REST fallback guarantees successful extraction under imperfect environments.[[1]](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/docs/PROMPT_ARCHITECTURE.md)

### Module Layout

- src/binance_ohlcv_extractor/[extractor.py](http://extractor.py)
    - _fetch_klines_requests(symbol, interval, start_ts_ms, end_ts_ms) — robust REST path with pagination and safety sleeps
    - _parse_klines_response(klines) — canonicalizes types and sets a DatetimeIndex
    - criptodata(symbol, start_date_str, end_date=None, interval="1d", output_dir=".") — orchestration, window filtering, CSV write
- src/binance_ohlcv_extractor/[cli.py](http://cli.py)
    - argparse‑based CLI that accepts multiple symbols and date windows, prints a short progress log, and exits with a clear status

### Design Principles

- Reliability over convenience
    - Always prefer a deterministic data shape with strong typing and indexing
    - Pagination logic avoids overlaps via next_start = last_open_time + 1
- Explicit inputs, explicit outputs
    - Date window is normalized to a closed range [start, end]
    - Outputs are separate CSV files per symbol to ease batch pipelines
- Safe defaults
    - Defaults to the public REST endpoint (no API keys required)
    - Optional connector path is “best‑effort” and never blocks the REST fallback

### Fallback Flow

See README “Architecture: Dependency‑Fallback Flow” for the ASCII diagram.

Why this architecture supports the portfolio story

- Prompt‑to‑code traceability: each non‑functional requirement from the Financial Prompt Framework (robustness, data integrity, dependency fallback) is reflected structurally in the code and demonstrably testable.[[2]](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/docs/FINANCIAL_PROMPT_FRAMEWORK.md)
- Portability: works on fresh environments without binance‑connector installed while remaining future‑proof for authenticated paths.

### Testing Notes

- Unit tests exercise parsing determinism and minimal pagination scenarios
- CI runs linters and tests for each Python version in the matrix
