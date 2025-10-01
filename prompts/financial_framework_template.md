# Data Extraction

# Financial Prompt Framework — Improved Template

> Metadata
- name: Financial OHLCV Extractor Template
- owner: alearisteguieta
- version: 2025-10-01
- purpose: Prompt to generate Python scripts that extract historical OHLCV from the Binance USDT Futures API and export them to CSV.

1) Objective
You are a developer experienced in FinTech and market APIs. Produce a complete, tested, and ready-to-run Python script that:
- Extracts historical candlestick (OHLCV) data from the Binance USDT Futures API,
- For a list of assets,
- With a daily timeframe (1d),
- From 2021-01-01 up to the day before execution,
- And exports one CSV per asset with columns: Date, Open, High, Low, Close, Volume (Date in a readable format and set as the DataFrame index).

2) Expected inputs
- assets: list of tickers (e.g., ["BTCUSDT","ETHUSDT","ADAUSDT","XRPUSDT"])
- start_date: "2021-01-01"
- end_date: day before execution (calculate dynamically)
- timeframe: "1d"

3) Functional requirements (precise)
- Correct handling of pagination / API limits for long historical ranges.
- Convert timestamps to UTC timezone and ISO YYYY-MM-DD format.
- One CSV per asset named exactly: <ASSET>.csv
- Modular code with an exportable main function: def extract_ohlcv(asset, start_date, end_date, timeframe, client, out_dir) -> pandas.DataFrame
- Basic logging and exponential backoff retries for network errors and rate limits.
- Validate DataFrame schema before exporting.
- Secure handling of API keys via environment variables (e.g., BINANCE_API_KEY, BINANCE_API_SECRET). Do not print secrets.

4) Technical requirements
- Language: Python 3.10+
- Libraries: binance-connector (or python-binance if preferred), pandas, python-dotenv (optional), requests, tenacity (or custom retry implementation)
- Tests: at minimum a sanity test validating output format (see prompts/evaluation_rubric.md)

5) Expected output
- A Python script executable from the console
- Clear console messages: start, progress per asset, final: "Data extraction finished :)"
- Proper error handling and exit codes.

6) Restrictions / DOs & DON'Ts
- DO: Create small, reusable functions.
- DO: Comment complex sections (pagination, rate limit handling).
- DO: Respect token/response limits when instructing models to return only code.
- DON'T: Hardcode credentials.
- DON'T: Use unmentioned libraries without justification.

7) Example I/O (expected)
Input (parameters):
- assets = ["BTCUSDT","ETHUSDT"]
- start_date = "2021-01-01"
- timeframe = "1d"

Expected CSV: BTCUSDT.csv
Date,Open,High,Low,Close,Volume
2021-01-01,29374.15,29600.00,29000.00,29300.00,1234.56
...

8) Validation (Checklist)
- [ ] Date as DatetimeIndex in UTC.
- [ ] Columns present and types correct.
- [ ] CSV files written correctly.
- [ ] Retries implemented for 429/5xx responses.
- [ ] Code executable from console with final output message.

9) Evaluation rubric (summary)
See prompts/evaluation_rubric.md for detailed scoring:
- DataFrame correctness (0-40)
- Robustness (retries, rate limits) (0-20)
- Security (no secrets) (0-10)
- Code quality (modularity, comments) (0-20)
- Console UX and messages (0-10)

This prompt without any modification has been used to generate the 3 code examples found in: [code_output_example_by_model](https://github.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/tree/7fbfdcfba5e3043de850027e0f1d2efe4b84c924/code_output_example_by_model) with the Chat GPT-5, Gemini 2.5 pro and Claude 4 sonnet models.

## Generation prompt (example to send to an LLM)

System: You are an assistant expert in Python development and financial APIs. Respond by generating ONLY the requested Python file.
User: Implement a Python script that meets all requirements in this template. Use the official Binance USDT Futures interface, correct pagination, retries, and export one CSV per asset. Define extract_ohlcv(...) and a main() that processes a list of assets. Do not include keys in the code; use environment variables.


