# Binance Futures OHLCV Extractor — Human-AI Co‑Development Showcase  (Currently under construction)

This repository serves as a practical case study in Prompt Engineering and AI Fluency, demonstrating the power of Human-AI Collaboration for the accelerated development of robust financial tools. It embodies a structured approach to Prompt Framework Architecture Design—a core focus of this portfolio—for creating high-utility software tailored for individual and large-scale investors.

At its core, the project is a robust Python utility designed for extracting historical Open, High, Low, Close, and Volume (OHLCV) candlestick data from the Binance USDT-M Futures API and saving it to clean, ready-to-use CSV files. This codebase has the possibility of being optimized and adapted to new requirements using AI assistance if desired.

This tool is engineered for high reliability, featuring an automated fallback to direct REST API calls if the official Binance connector library is not installed or fails, ensuring maximum data retrieval stability for your Quantitative Finance and Machine Learning projects.

## 💡 Prompt Engineering & AI Fluency: The High-Reliability Framework

This repository demonstrates Prompt Engineering for robust financial tooling, including dependency-fallback architecture, pagination safety, and data quality guarantees.

### Framework Methodology: Engineering for Robustness and Dependencies

The prompt architecture was strategically designed to mandate not just the *functionality* but also the *resilience* of the final script.

| Layer | Objective | Key Prompt Strategy | Demonstration in Code Analysis |
| :--- | :--- | :--- | :--- |
| **1. Strategic Intent: Robustness** | Define the complete architecture, prioritizing **maximum data retrieval stability** by mandating a primary method and a **guaranteed *fallback***. | **Constraint-Driven Prompting:** Used to set the **core engineering requirement**: "If the `binance-connector` is unavailable or fails, implement a separate, native `requests`-based function to handle the entire pagination and API call logic." | Focus on the `try/except` block and the `_fetch_klines_connector` / `_fetch_klines_requests` functions in `criptodata`. |
| **2. Modular Engineering: Time Series Logic** | Develop precise, reusable helper functions for core time-series and data handling logic, independent of the fetching mechanism. | **Abstraction & Helper Prompting:** Mandated the creation of utility functions for common tasks like *timestamp* conversion (`_to_millis`) and complex response parsing (`_parse_klines_response`). | Focus on `_parse_klines_response`, which handles *all* 12 fields of the raw API response and prepares the final `pandas` `DataFrame` with `Date` index. |
| **3. Reliability Implementation: Pagination & Rate Limits** | Ensure the *fallback* REST API logic correctly handles Binance's pagination and includes rate-limiting safeguards. | **Chain-of-Thought (CoT) Prompting:** Requesting the AI to detail the logic for iterative fetching using `startTime`/`endTime` parameters and calculating the `next_start` value from the last candle's open time. | Focus on the `while True` loop, `limit` checks, and the crucial `next_start = last_open_time + 1` logic within `_fetch_klines_requests`. |

This approach demonstrates **AI Fluency** by leveraging the model to generate not just working code, but code that addresses **non-functional requirements** (robustness, dependency management) and best practices (docstrings, type hints, security via environment variables).

1.  **Translate Complex Financial Requirements** into modular, production-ready Python code via structured prompts (AI Fluency).
2.  **Architect Robust Code:** The tool is engineered for high reliability, featuring an automated fallback to direct REST API calls (using `requests`) if the official Binance connector library is unavailable or fails, ensuring maximum data retrieval stability.
3.  **Establish a Data Foundation** for advanced **Quantitative Finance** and **Machine Learning** projects by enforcing data quality standards (DatetimeIndex, Float types).

By focusing on prompt structure and iterative refinement, this repository validates a crucial workflow for **financial software engineers** operating in the AI-centric era.

## Prompt Engineering Methodology

This repository demonstrates a 4-step process for AI-assisted financial tool development:

1. **Prompt Design**: Create structured prompts using the Financial Prompt Framework
2. **Code Generation**: Obtain initial code implementation from AI assistant
3. **Validation & Testing**: Rigorously test and validate the generated code
4. **Iteration**: Refine prompts and implementations for production-ready solutions

## Features

- Fetch historical OHLCV (Date, Open, High, Low, Close, Volume) from Binance
  USDT-M futures public klines endpoint.
- Saves per-symbol CSV files (e.g. `BTCUSDT.csv`).
- Configurable start/end dates, list of tickers, timeframe and output folder.
- Graceful fallback if `binance-connector` is not installed.
- Robust pagination and rate-safety.

## Case Studies

### 1. Crypto Data Extraction

This case study demonstrates how to build a robust cryptocurrency data extraction tool using the Financial Prompt Framework. The solution extracts OHLCV data from Binance for various crypto assets and exports it to CSV files.

### Example output from AI-assisted development:
```bash
def criptodata(symbol: str, start_date_str: str = "2021-01-01", interval: str = "1d"):
    """Extract historical OHLCV data for a cryptocurrency symbol"""
    # See full implementation in code_examples/crypto_data_extractor.py
```

## Getting Started

### Prerequisites

- Basic understanding of Python
- Knowledge of financial concepts
- Access to an AI assistant (Claude, GPT, etc.)

## 1-minute Quickstart

- Install
    - python -m venv .venv && source .venv/bin/activate
    - pip install -r requirements.txt
- Run
    - python -m binance_ohlcv_extractor.cli --symbols BTCUSDT ETHUSDT --start 2021-01-01 --interval 1d --out ./binance_futures_csvs
- Output
    - One CSV per symbol with Date index and float OHLCV columns

# CLI usage

- --symbols: one or more tickers
- --start: YYYY-MM-DD
- --end: optional, defaults to yesterday
- --interval: 1m 5m 1h 4h 1d
- --out: output directory
- --force-requests: bypass connector and use REST

Rate limits and reliability

- Paginates with MAX_LIMIT=1000 per call
- Advances next_start = last_open_time + 1 to avoid overlaps
- Mild sleep between requests to stay below thresholds

# Environment Variables

- Public klines endpoint; keys are not required
- If using keys for future extensions, load from environment or .env and never commit secrets

Example:

```bash
export BINANCE_API_KEY="YOUR_API_KEY"
export BINANCE_API_SECRET="YOUR_API_SECRET"
```

# Usage

* Configure Tickers: Open the binance_futures_ohlcv_to_csv.py file and modify the DEFAULT_TICKERS list and START_DATE_STR as needed.
* Run the Script:

```bash
  python binance_futures_ohlcv_to_csv.py
```

# Output example ChatGPT-5

* The script will create a directory named binance_futures_csvs/ in the execution path and save a separate CSV file for each processed ticker (e.g., BTCUSDT.csv, ETHUSDT.csv).
* Example CSV Output (BTCUSDT.csv):

```bash
Starting data extraction for tickers: BTCUSDT, ETHUSDT, ADAUSDT, XRPUSDT
Timeframe: 1d, start date: 2021-01-01, end date: 2025-09-26
Downloading BTCUSDT ...
  -> BTCUSDT: 1729 rows saved to binance_futures_csvs\BTCUSDT.csv
Downloading ETHUSDT ...
  -> ETHUSDT: 1729 rows saved to binance_futures_csvs\ETHUSDT.csv
Downloading ADAUSDT ...
  -> ADAUSDT: 1729 rows saved to binance_futures_csvs\ADAUSDT.csv
Downloading XRPUSDT ...
  -> XRPUSDT: 1729 rows saved to binance_futures_csvs\XRPUSDT.csv
Data extraction finished :)
```
* The output result may vary depending on the LLM used. You can also modify the output format directly in the script.


# Quantitative Finance and Machine Learning Context

* **Feature Engineering:** Creating technical indicators (SMA, RSI, MACD).
* **Time Series Modeling:** Applying models like ARIMA, GARCH, or more complex ML/DL models (LSTMs, Transformers) to predict future price movements.
* **Backtesting:** Simulating trading strategies over historical market conditions.
  
This extractor provides the necessary foundation for projects rooted in Financial Engineering, Discrete Models of Financial Markets, and Machine Learning for Time-Series, which require high-quality, standardized input data.

# Project Architecture & Code Breakdown

* The core script is designed to be modular and easy to maintain.

```bash
| Function	| Purpose
| _ensure_api_keys()	| Safely reads Binance API credentials from environment variables.
| _to_millis(dt)	| Converts Python datetime objects into Binance-required epoch milliseconds.
| _parse_klines_response(klines)	| Transforms the raw list-of-lists API response into a clean, indexed pandas.DataFrame.
| _fetch_klines_requests(...)	| Core Robustness Logic. Fetches data using the standard requests library, handling API endpoint parameters and necessary pagination (requesting data in chunks of MAX_LIMIT=1000).
| _fetch_klines_connector(...)	| An attempt to use the binance-connector library (if installed), providing a placeholder for potential higher-performance or authenticated retrieval.
| criptodata(...)	| Main Extraction Workflow. Manages the date conversion, executes the fetching (with connector/request fallback), and writes the final DataFrame to a CSV file.
```

---
