# Prompt-driven architecture and dependency-fallback design

### Scope
This document explains how prompt requirements shaped the code structure, why reliability is a first‑class concern, and how the connector → REST fallback guarantees successful extraction in imperfect environments.  
For context, see [PROMPT_ARCHITECTURE.md](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/docs/PROMPT_ARCHITECTURE.md).

---

### Module layout
- **Extractor module:** [src/binance_ohlcv_extractor/extractor.py](https://github.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/blob/main/src/binance_ohlcv_extractor/extractor.py)  
  - **_fetch_klines_requests:** Robust REST path with pagination and safety sleeps.  
  - **_parse_klines_response:** Canonicalizes types and sets a `DatetimeIndex`.  
  - **criptodata:** Orchestrates fetching, window filtering, and CSV write.  
- **CLI module:** [src/binance_ohlcv_extractor/cli.py](https://github.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/blob/main/src/binance_ohlcv_extractor/cli.py)  
  - **argparse CLI:** Accepts multiple symbols and date windows, prints concise progress, exits with clear status codes.

---

### Design principles
- **Reliability over convenience:**  
  Always prefer a deterministic data shape with strong typing and indexing. Pagination avoids overlaps via `next_start = last_open_time + 1`.
- **Explicit inputs, explicit outputs:**  
  The date window is normalized to a closed range `[start, end]`. Outputs are separate CSV files per symbol to ease batch pipelines.
- **Safe defaults:**  
  Default to the public REST endpoint (no API keys required). The optional connector path is “best‑effort” and never blocks the REST fallback.

---

### How prompts influenced architecture
- **Prompt-to-code traceability:**  
  Non‑functional requirements from the Financial Prompt Framework (robustness, data integrity, dependency fallback) are mapped directly into modules and functions, ensuring each behavior is testable and reproducible. See [FINANCIAL_PROMPT_FRAMEWORK.md](https://raw.githubusercontent.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/main/docs/FINANCIAL_PROMPT_FRAMEWORK.md).
- **Operational choices derived from prompts:**  
  Safety sleeps, strict type casting, closed‑range window filtering, and monotonic timestamp guarantees were explicitly called for in the prompt and implemented as first‑class concerns.
- **Portfolio alignment:**  
  The architecture demonstrates production‑minded reliability while preserving extensibility (e.g., authenticated paths via environment variables) to reflect the framework’s emphasis on future‑proof design.

---

### Fallback flow
See README section “Architecture: Dependency‑Fallback Flow”: [README.md](https://github.com/alearisteguieta/Binance-Futures-OHLCV-Extractor/blob/main/README.md).

```text
               +---------------------------+
               |   CLI / criptodata()      |
               +------------+--------------+
                            |
                            v
                +-----------+-----------+
                |  Connector available? |
                +-----------+-----------+
                            | Yes
                            v
                 +----------+-----------+
                 | Try connector path   |
                 +----------+-----------+
                            |
                Success? ---+--- No -------------------+
                  | Yes                             |   |
                  v                                 |   v
        +---------+---------+                       | +-----------------------+
        | Canonicalize &    |                       | | REST path (requests)  |
        | window filter     |                       | | paginate & backoff    |
        +---------+---------+                       | +----------+------------+
                  |                                  |            |
                  v                                  |            v
        +---------+---------+                        |  +---------+----------+
        | Write CSV per     |                        |  | Canonicalize &     |
        | symbol (UTC ISO)  |                        |  | window filter       |
        +-------------------+                        |  +---------+----------+
                                                     |            |
                                                     +------------+
                                                                  |
                                                                  v
                                                      +-----------+-----------+
                                                      | Write CSV per symbol |
                                                      | (UTC ISO timestamps) |
                                                      +----------------------+
```

---

### Testing notes
- **Unit tests:** Exercise parsing determinism, pagination boundaries, and window filtering edge cases.  
- **CI matrix:** Linters and tests run across the standardized Python version(s) declared in the repository.  
- **Observability checks:** Ensure progress logs and error messages are concise, actionable, and consistent across fallback paths.
