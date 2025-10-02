## Data Extraction Request

### Audience
This document is intended for maintainers, contributors, and developers working on the Binance Futures OHLCV extractor. It assumes familiarity with Python, REST APIs, and quantitative research workflows.

### How to Use This Document
Use this specification as a reference when implementing, reviewing, or extending the extractor. It defines functional and technical requirements, validation criteria, and non‑functional expectations to ensure reproducibility and reliability.

### Objective
Specify an AI‑driven, production‑minded data extractor for Binance USDT‑M futures OHLCV that guarantees a reliable CSV foundation for quantitative research.

### Domain Context
- **Role:** Software developer with FinTech and exchange API experience  
- **Output:** Date‑indexed OHLCV tables with float types  
- **Notes:** Model outputs and test notes are captured under `testing_validation_by_model`

### Functional Requirements
- **Data source:** Binance Futures public klines  
- **Assets:** One or more symbols, e.g., `BTCUSDT`, `ETHUSDT`, `ADAUSDT`, `XRPUSDT`  
- **Fields:** Date, Open, High, Low, Close, Volume  
- **Window:** From `YYYY‑MM‑DD` to yesterday  
- **Timeframes:** 1m, 5m, 15m, 1h, 4h, 1d  

### Technical Requirements
- **Language:** Python 3.10+ (standardized across the repository)  
- **Libraries:** `pandas`, `requests`  
- **Security:** No hardcoded secrets. Keys are optional for future extensions via environment variables  
- **Output:** One CSV per symbol with Date as index and float OHLCV columns  
- **Code structure:**  
  - Core function:  
    ```python
    criptodata(symbol, start_date_str, end_date=None, interval="1d", output_dir=".")
    ```  
  - REST pagination with `MAX_LIMIT=1000` and `next_start` increment  
  - Deterministic type casting and window filtering  

### Validation Criteria
- **Determinism:** Repeated runs over the same window produce identical rows (unless upstream data changes)  
- **Types:** OHLCV numeric columns are floats; Date is a `DatetimeIndex`  
- **Integrity:** No duplicate or overlapping timestamps; window boundaries are respected  
- **Robustness:** Transient network failures handled by short backoff; connector failure never blocks REST path  

### Non‑Functional Requirements (NFRs)
- **Reliability:** Connector → REST fallback, minimal sleeps to respect rate limits  
- **Portability:** Works without `binance‑connector` installed  
- **Observability:** Concise console progress and actionable error messages  

### Human–AI Collaboration Evidence
- The initial prompt and iterative refinements informed both the pagination logic and the fallback strategy.  
- Model outputs and test notes are captured under `testing_validation_by_model`.  
- **Model provenance:** The prompt version used to generate the code is documented here:  
  [financial_framework_template.md](https://github.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/blob/main/prompts/financial_framework_template.md)
