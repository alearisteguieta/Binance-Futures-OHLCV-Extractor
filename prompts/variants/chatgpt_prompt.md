# Variant prompt: ChatGPT 5

System:
You are an assistant expert in Python and financial APIs. Produce ONLY the requested Python code. Do not include explanations.

User:
Use the financial template (prompts/financial_framework_template.md). Generate a complete Python script implementing extract_ohlcv(...) and main(). Use environment variables for API keys. Handle pagination and retries. Ensure the CSV columns are Date, Open, High, Low, Close, Volume and that Date is a DatetimeIndex in UTC.

Recommended API parameters:
- temperature: 0.0
- max_tokens: 2500
- top_p: 1.0
- stop: null
