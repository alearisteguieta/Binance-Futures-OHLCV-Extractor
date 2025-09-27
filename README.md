# Binance-Futures-OHLCV-Extractor

A robust Python utility designed for extracting historical Open, High, Low, Close, and Volume (OHLCV) candlestick data from the Binance USDT-M Futures API and saving it to clean, ready-to-use CSV files.

This tool is engineered for high reliability, featuring an automated fallback to direct REST API calls if the official Binance connector library is not installed or fails, ensuring maximum data retrieval stability for your Quantitative Finance and Machine Learning projects.

## Key Features

* **Robust Data Retrieval:** Prioritizes the `binance-connector` (if available) but reliably falls back to direct `requests` for guaranteed extraction.
* **Time Series Integrity:** Automatically cleans and formats raw Binance klines data into a standard pandas DataFrame with a UTC-aware datetime index.
* **Configurable:** Easy modification of target tickers, start date, and timeframe (default is daily, '1d').
* **Bulk Extraction:** Designed to process a default list of tickers in sequence, minimizing rate-limit risk with small pauses.

## Prerequisites

Before running the script, ensure you have the necessary libraries installed.

### Installation

Use the following command to install the primary dependencies:

```bash
pip install -r requirements.txt
```

# Environment Variables

While the klines (candlestick) endpoint is public and does not require authentication, the script includes logic to detect API keys for future extension (e.g., authenticated endpoints).

You can optionally set your environment variables for future use:

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

# Output

* The script will create a directory named binance_futures_csvs/ in the execution path and save a separate CSV file for each processed ticker (e.g., BTCUSDT.csv, ETHUSDT.csv).
* Example CSV Output (BTCUSDT.csv):

```bash
Date	open	high	low	close	volume
2021-01-01 00:00:00	28935.91	29596.12	28935.91	29331.05	118228.012
2021-01-02 00:00:00	29330.93	33318.00	29285.00	32185.00	367297.435
...	...	...	...	...	...
```

# Quantitative Finance and Machine Learning Context

* **Feature Engineering:** Creating technical indicators (SMA, RSI, MACD).
* **Time Series Modeling:** Applying models like ARIMA, GARCH, or more complex ML/DL models (LSTMs, Transformers) to predict future price movements.
* **Backtesting:** Simulating trading strategies over historical market conditions.
  
This extractor provides the necessary foundation for projects rooted in Financial Engineering, Discrete Models of Financial Markets, and Machine Learning for Time-Series, which require high-quality, standardized input data.

# Project Architecture & Code Breakdown

* The core script is designed to be modular and easy to maintain.

```bash
Function	Purpose
_ensure_api_keys()	Safely reads Binance API credentials from environment variables.
_to_millis(dt)	Converts Python datetime objects into Binance-required epoch milliseconds.
_parse_klines_response(klines)	Transforms the raw list-of-lists API response into a clean, indexed pandas.DataFrame.
_fetch_klines_requests(...)	Core Robustness Logic. Fetches data using the standard requests library, handling API endpoint parameters and necessary pagination (requesting data in chunks of MAX_LIMIT=1000).
_fetch_klines_connector(...)	An attempt to use the binance-connector library (if installed), providing a placeholder for potential higher-performance or authenticated retrieval.
criptodata(...)	Main Extraction Workflow. Manages the date conversion, executes the fetching (with connector/request fallback), and writes the final DataFrame to a CSV file.
```

---
