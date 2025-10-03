# Extraction Notes

### Audience
Prompts Engineers, AI Fluency Workers, Software Developers, AI Enthusiastic, Maintainers and Contributors.

### Purpose
This document describes the practical aspects of the Binance Futures klines endpoint and explains the extractor’s operational choices.  
For additional context, see [CONSIDERATION_NOTES.md](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/docs/CONSIDERATION_NOTES.md).

### Pagination and Windows
- Each request is limited to a maximum of 1000 candles.  
- Pagination is handled by advancing with `next_start = last_open_time + 1` to avoid overlapping records.  
- The final DataFrame should be filtered to the inclusive range `[start_dt_utc, end_dt_utc]`.

### Rate Limits and Backoff
- Insert a short delay (for example, 200 ms) between paginated requests to respect rate limits.  
- For transient errors such as HTTP 429 or 5xx responses, consider implementing exponential backoff, especially when extracting long historical windows.

### Data Shape and Types
- Canonical columns include: `open`, `high`, `low`, `close`, and `volume`, all stored as floats.  
- The index should be a `DatetimeIndex`. For CSV exports, timestamps should be persisted as **UTC ISO 8601 strings** (e.g., `2021-01-01T00:00:00Z`) to ensure clarity and reproducibility.  
- No duplicate rows are allowed. Timestamps must be strictly monotonic and increasing for each symbol.

### Error Handling
- For HTTP errors, include both the status code and the response text in the error message.  
- If a requested window returns no data, raise a clear error indicating that the window is empty.  
- Symbols with late listing dates may produce shorter historical ranges. This is expected and should not be treated as an error.

### Security and Configuration
- Public klines do not require API keys.  
- For future authenticated flows, use environment variables for credentials and never commit secrets to the repository.  
- See [SECURITY.md](SECURITY.md) for details on security posture and handling.

### Reproducibility
- Dependencies are pinned in `requirements.txt` to ensure consistent environments.  
- Continuous Integration (CI) runs linting and unit tests on all pull requests to maintain code quality.
