## Data Extraction Request

### Financial Prompt Framework:

This comprehensive prompt methodically deconstructs the problem space and articulates the solution requirements in a clear, accessible format for the LLM to generate complete Python code without unnecessary limitations or ambiguities. The carefully structured framework provides the AI with precise instructions regarding the financial domain context, specific programming requirements, and detailed code generation expectations. By organizing information into distinct sections covering domain context, functional requirements, technical specifications, and explicit instructions, the prompt creates a robust foundation for the AI to work from. This methodically organized approach enables thorough validation of the AI's decision-making process and allows the generated code to be rigorously tested and evaluated prior to actual implementation in a production environment. The prompt's clarity and comprehensive nature significantly enhance the likelihood of receiving high-quality, production-ready code that meets all specified requirements.

# 1) Domain Context

**Role:** You are a software developer with experience in FinTech and financial market APIs.

**Objective:** Create a Python script to extract historical market data (candlestick data) from the Binance API and export them to a CSV file.

## 2) Functional Requirements

**Data Sources:** The Binance API for USDT futures.

**Assets:** The function should be capable of processing a list of assets, specifically BTCUSDT, ETHUSDT, ADAUSDT, and XRPUSDT.

**Data to Extract:** Date, Open, High, Low, Close, Volume.

**Date Range:** From January 1, 2021 until the day before the script execution.

**Timeframe:** Daily (1d).

**Data Processing:** Convert the timestamp from the Date column to a readable date format and set it as the DataFrame index.

## 3) Technical Requirements

**Language:** Python.

**Libraries:** binance-connector, pandas, datetime.

**API Keys Handling:** The script must handle API keys securely.

**Output Format:** A separate CSV file for each asset, named with the asset's ticker (e.g., BTCUSDT.csv).

**Code Structure:** The code should be modular, with a main function (criptodata) that can be called within a loop to process multiple assets.

## 4) Specific Instructions to the Assistant (Prompt)

Write only the Python code in a single code block.

Include clear comments to explain each step, such as data conversion and DataFrame handling.

Ensure the script can be executed directly from the console.

Include a confirmation message at the end, such as "Data extraction finished :)".

## 5) Validation

The function logic should be reproducible and generate a correct pandas DataFrame before exporting it to a CSV.

The code should be robust to handle the provided list of assets without errors.
