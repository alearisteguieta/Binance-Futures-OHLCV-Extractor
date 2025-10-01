# Extraction Notes

### Purpose

Document practical aspects of the Binance Futures klines endpoint and the extractor’s operational choices.[[1]](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/docs/CONSIDERATION_NOTES.md)

### Pagination and Windows

- Request limit: typically 1000 candles per call
- Cursoring: advance with next_start = last_open_time + 1 to avoid overlap
- Windowing: filter the final DataFrame to [start_dt_utc, end_dt_utc] inclusively

### Rate Limits and Backoff

- Mild sleep (e.g., 200 ms) between paginated requests
- Consider exponential backoff for transient HTTP 429/5xx in long windows

### Data Shape and Types

- Canonical columns: open, high, low, close, volume as float
- Index: Date as DatetimeIndex (UTC → naïve local time for CSV clarity)
- No duplicates: assert monotonic increasing timestamps per symbol

### Error Handling

- HTTP errors: include status code and response text in the message
- Empty windows: raise a clear error indicating no data returned
- Partial history: symbols with late listings may produce shorter ranges; this is expected

### Security and Configuration

- Public klines: no API keys needed
- Future authenticated flows: use environment variables and never commit secrets
- See [SECURITY.md](http://SECURITY.md) for posture and handling

Reproducibility

- Pinned dependencies in requirements.txt
- CI runs linting and unit tests on pull requests
