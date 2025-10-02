# Chat GPT-5

In this section you can see the original prompt entered into Chat GPT-5

### Prompt imput: 

```bash

1) Domain Context

**Role:** You are a software developer with experience in FinTech and financial market APIs.

**Objective:** Create a Python script to extract historical market data (candlestick data) from the Binance API and export them to a CSV file.

2) Functional Requirements

**Data Sources:** The Binance API for USDT futures.

**Assets:** The function should be capable of processing a list of assets, specifically BTCUSDT, ETHUSDT, ADAUSDT, and XRPUSDT.

**Data to Extract:** Date, Open, High, Low, Close, Volume.

**Date Range:** From January 1, 2021 until the day before the script execution.

**Timeframe:** Daily (1d).

**Data Processing:** Convert the timestamp from the Date column to a readable date format and set it as the DataFrame index.

3) Technical Requirements

**Language:** Python.

**Libraries:** binance-connector, pandas, datetime.

**API Keys Handling:** The script must handle API keys securely.

**Output Format:** A separate CSV file for each asset, named with the asset's ticker (e.g., BTCUSDT.csv)

**Code Structure:** The code should be modular, with a main function (criptodata) that can be called within a loop to process multiple assets.

4) Specific Instructions to the Assistant (Prompt)

Write only the Python code in a single code block.

Include clear comments to explain each step, such as data conversion and DataFrame handling.

Ensure the script can be executed directly from the console.

Include a confirmation message at the end, such as "Data extraction finished :)".

5) Validation

The function logic should be reproducible and generate a correct pandas DataFrame before exporting it to a CSV.

The code should be robust to handle the provided list of assets without errors.

```

# ChatGPT-5 Console Print() Example

## Output explanation: 

- This Print() function represents the original output shown in the console without any modifications to the script. 
The script was reviewed before execution, and in its original response, ChatGPT-5 does not contain any errors present in the code.

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

This Print() is subject to modification based on user requirements, asset count, etc.

## .cvs file example:Download here: [BTCUSDT.csv](https://github.com/user-attachments/files/22660838/BTCUSDT.csv)

### Date,Open,High,Low,Close,Volume

```bash
- 2023-09-27 00:00:00+00:00,26221.68,26850.0,26112.06,26372.99,34771.57978
```

# Notes 

- In the case of Chat GPT - 5, there was no need to iterate the code. The code worked as it was copied and pasted from the output to Visual Studio. If you'd like to read a detailed iteration process with Claude Sonnet 4.5, you can do so at Iterations.
