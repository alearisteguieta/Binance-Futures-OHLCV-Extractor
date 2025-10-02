# Financial Prompt Framework — Improved Template

Metadata
- name: Financial OHLCV Extractor Template
- owner: alearisteguieta
- prompt_id: ffw-2025-10-02-v1
- version: 2025-10-02
- purpose: Generate Python scripts that extract historical OHLCV from the Binance USDT Futures API and export them to CSV.

1) Objective
You are a developer experienced in FinTech and market APIs. Produce a complete, tested, and ready-to-run Python script that:
- Extracts historical candlestick (OHLCV) data from the Binance USDT Futures API;
- Accepts a list of assets;
- Uses a daily timeframe by default (1d), but supports other intervals (1m,5m,15m,1h,4h);
- Extracts data from 2021-01-01 up to the day before execution (end date computed dynamically);
- Exports one CSV per asset with exact columns: Date, Open, High, Low, Close, Volume.
- Ensures Date is ISO 8601 (UTC) in the CSV and stored as DatetimeIndex in the returned pandas DataFrame.

2) Expected inputs
- assets: list[str] (example: ["BTCUSDT","ETHUSDT","ADAUSDT","XRPUSDT"])
- start_date: "2021-01-01"
- end_date: computed as yesterday if not provided
- timeframe: "1d" (default)

3) Functional requirements (precise)
- Correct pagination for historical ranges (Binance MAX_LIMIT=1000).
- Convert timestamps to UTC, present date strings in ISO 8601 (e.g., 2021-01-01T00:00:00Z).
- Output: one CSV per asset named <ASSET>.csv.
- API keys should be optional: support unauthenticated public klines; if auth is used, keys must come from environment variables.
- The main extraction function signature should be:
  def extract_ohlcv(asset: str, start_date: str, end_date: Optional[str], interval: str, output_dir: str) -> pandas.DataFrame

4) Technical requirements
- Language: Python 3.10+
- Libraries: pandas, requests, python-dotenv (optional), tenacity (optional)
- The code should include basic logging (logging module) and an option to enable verbose output.
- Tests: include a minimal unit test for _parse_klines_response and a validation script to assert output shape.

5) Deliverables (what the model should return)
- A single Python file implementing the extraction logic with:
  - Module-level docstring including prompt provenance (prompt_id, prompt_version, date)
  - Public function extract_ohlcv(...) described above
  - A CLI entrypoint (if __name__ == "__main__") or a separate cli.py file invocation example
  - Clear comments for steps: pagination, backoff, parsing, CSV export
- Minimal README snippet showing how to run the script and required environment variables.

6) DOs & DON'Ts
- DO: Return ONLY a single code block when asked to provide code.
- DO: Use environment variables for secrets; provide a .env.example for dev convenience.
- DO: Add provenance metadata at top of file (model name, prompt_id, generation timestamp).
- DON'T: Hardcode secrets or API keys in outputs.
- DON'T: Use proprietary or obscure libraries without justification.

7) Example I/O (expected)
Input:
- assets = ["BTCUSDT","ETHUSDT"]
- start_date = "2021-01-01"
- timeframe = "1d"

Expected CSV (BTCUSDT.csv)
Date,Open,High,Low,Close,Volume
2021-01-01T00:00:00Z,29374.15,29600.00,29000.00,29300.00,1234.56
...

8) Validation checklist
- [ ] Date column is DatetimeIndex in UTC in returned DataFrame
- [ ] CSV Date format is ISO 8601 (UTC)
- [ ] Columns present and numeric dtypes are floats
- [ ] Pagination and backoff logic present and documented
- [ ] No hardcoded secrets; usage of environment variables documented

9) Generation instructions (example to send to an LLM)
System: You are an assistant expert in Python and financial APIs. Generate ONLY the requested Python file and nothing else.
User: Implement a Python script that meets all requirements above. Include module-level provenance metadata (prompt_id, prompt_version). Use requests for REST klines fetching and provide a connector fallback only as optional. Make sure the CSVs follow the exact schema.

This prompt without any modification has been used to generate the 3 code examples found in: [code_output_example_by_model](https://github.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/tree/7fbfdcfba5e3043de850027e0f1d2efe4b84c924/code_output_example_by_model) with the Chat GPT-5, Gemini 2.5 pro and Claude 4 sonnet models.
