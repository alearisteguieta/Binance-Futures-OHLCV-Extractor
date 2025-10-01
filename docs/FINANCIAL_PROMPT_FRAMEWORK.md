## Data Extraction Request

### Objective

Specify an AI‑driven, production‑minded data extractor for Binance USDT‑M futures OHLCV that guarantees a reliable CSV foundation for quant research.

Domain Context

- Role: Software developer with FinTech and exchange API experience
- Output: Date‑indexed OHLCV tables with float types
Model outputs and test notes are captured under testing_validation_by_model

### Functional Requirements

- Data source: Binance Futures public klines
- Assets: One or more symbols, e.g., BTCUSDT ETHUSDT ADAUSDT XRPUSDT
- Fields: Date, Open, High, Low, Close, Volume
- Window: From YYYY‑MM‑DD to yesterday
- Timeframes: 1m 5m 15m 1h 4h 1d

### Technical Requirements

- Language: Python 3.9+
- Libraries: pandas, requests
- Security: No hardcoded secrets. Keys are optional for future extensions via environment variables
- Output: One CSV per symbol with Date as index and float OHLCV columns
- Code structure:
    - Core function: criptodata(symbol, start_date_str, end_date=None, interval="1d", output_dir=".")
    - REST pagination with MAX_LIMIT=1000 and next_start increment
    - Deterministic type casting and window filtering

### Validation Criteria

- Determinism: repeated runs over the same window produce identical rows (unless upstream data changes)
- Types: OHLCV numeric columns are floats, Date is a DatetimeIndex
- Integrity: no duplicate or overlapping timestamps; window is respected
- Robustness: transient network failures handled by short backoff; connector failure never blocks REST path

### Non‑Functional Requirements (NFRs)

- Reliability: connector→REST fallback, minimal sleeps to respect rate limits
- Portability: works without binance‑connector installed
- Observability: concise console progress, actionable error messages

### Human–AI Collaboration Evidence

- The initial prompt and iterative refinements informed both the pagination logic and the fallback strategy.[[1]](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/README.md)
- Model outputs and test notes are captured under testing_validation_by_model
