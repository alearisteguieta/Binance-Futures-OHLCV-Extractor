# AI-Powered FinTech Tools with Prompt Engineering for retail in

## 📜 Overview

This project is a portfolio that demonstrates the power of **Prompt Engineering** in human-AI collaboration to develop tailored financial tools. The goal is to show how an independent investor or venture capitalist can, with programming knowledge and the assistance of an LLM, create robust solutions for investment analysis, risk management, and more.

This repository is a case study on **AI Fluency**, applying a **Structured Framework** for code generation and validation with Python tool to download daily OHLCV (Open, High, Low, Close, Volume) historical data from the Binance USDT-M futures market and save it to CSV files. Providing a clean, structured dataset ready for quantitative analysis, backtesting of algorithmic strategies, and training of machine learning models for time series.

---

## 🚀 Key Features

* **Cryptoasset DATA Extraction**: A script that extracts market data into a .cvs file.
* **Stock Portfolio Optimization**: A tool for building and supporting market strategies with historical data.
* **Reusable Prompt Templates**: Creation of prompt templates for code refinement and reuse.

---

## 🤖 The Human-AI Collaboration Framework

The core of this project is an iterative working method. You can learn more about it in our [methodology document](docs/project_methodology.md).

1. **Requirement Definition**: A solution to a clear and practical financial need.
2. **Prompt Design**: A detailed prompt is designed using one of our [base templates](prompts/templates/).
3. **AI-Assisted Code Generation**: The LLM generates a draft of the Python code.
4. **Human Validation and Refinement**: The code is reviewed, debugged, and validated by the developer. This includes writing [unit tests](tests/) to ensure robustness.
5. **Iteration**: The process is repeated, progressively improving the code and prompts.

---

## 🛠️ How to Get Started

```
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
```

### Prerequisites

* Python 3.8+
* An Binance or other futures-broker API key
* The example is built with ChatGPT5-5

### Instaling

#### Python Libraries

```
pip install pandas
```

## 🔑 Configuración (Opcional)

Las claves API de Binance **no son obligatorias** para acceder al endpoint público de *klines* (`/fapi/v1/klines`) utilizado, pero se recomienda configurar las variables de entorno para una futura extensión del script a endpoints privados:

```golpecito
exportar BINANCE_API_KEY="SU_CLAVE_AQUI"
exportar BINANCE_API_SECRET="SU_SECRETO_AQUI"

Configure your API keys in a file `.env`.
```
---

## 📦Installation

1. **Clone the repository:**
``` pip
git clone [https://github.com/YourUser/binance-futures-data-downloader.git](https://github.com/YourUser/binance-futures-data-downloader.git)
cd binance-futures-data-downloader
```
2. **Install dependencies:**
``` pip
pip install -r requirements.txt
```
---

## 💡 Use Case Examples
```
python binance_futures_ohlcv_to_csv.py
```
### Use Case 1: BTC Extracting DATA

1. **The Prompt**: This is the [detailed prompt](prompts/use_cases/uc001_crypto_volatility_analysis.md) used to generate the data extraction code.
2. **The Generated Code**: The result of the AI-Human collaboration is the [`risk_analyzer.py`](src/financial_tools/risk_analyzer.py) script.
3. **Execution**:
```bash
python -m src.financial_tools.risk_analyzer --asset BTC --period 365
```
4. **Results**: The script will generate a .csv file with all the asset's historical data between 2021 and 2025 in real time. You can see an example of the process in [this notebook](notebooks/03_results_visualization.ipynb).

---

📁 Output
CSV files will be saved in the binance_futures_csvs/ directory.

binance_futures_csvs/BTCUSDT.csv

binance_futures_csvs/ETHUSDT.csv

...and so on.

📝 Code Reference
The script uses a dual approach to the API:

It attempts to use the binance-connector library if it's installed.

If it fails or is unavailable, it falls back to direct requests to the URL https://fapi.binance.com/fapi/v1/klines. This design ensures robustness and fault tolerance when fetching data.

---

## ✅ Testing

Validation is crucial. All tools have been tested using `pytest`.

```bash
pytest
