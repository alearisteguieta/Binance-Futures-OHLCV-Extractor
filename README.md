# Binance Futures OHLCV Extractor — Human‑AI Prompt Engineering Case Study

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-pytests-green.svg)]()
[![Docs](https://img.shields.io/badge/docs-guides-lightgrey.svg)]()

Status: Educational guide / case study (not intended as an executable tool)

At its core, the project is a robust Python utility designed for extracting historical Open, High, Low, Close, and Volume (OHLCV) candlestick data from the Binance USDT-M Futures API and saving it to clean, ready-to-use CSV files. This codebase has the possibility of being optimized and adapted to new requirements using AI assistance if desired.

This tool is engineered for high reliability, featuring an automated fallback to direct REST API calls if the official Binance connector library is not installed or fails, ensuring maximum data retrieval stability for your Quantitative Finance and Machine Learning projects.

- Work in progress — Case study and reproducible prompt engineering workflow.

Alejandro Sanchez Aristeguieta

## 💡 Prompt Engineering & AI Fluency: The High-Reliability Framework

This repository demonstrates Prompt Engineering for robust financial tooling, including dependency-fallback architecture, pagination safety, and data quality guarantees.

### Framework Methodology: Engineering for Robustness and Dependencies

The prompt architecture was strategically designed to mandate not just the *functionality* but also the *resilience* of the final script.

| Layer | Objective | Key Prompt Strategy | Demonstration in Code Analysis |
| :--- | :--- | :--- | :--- |
| **1. Strategic Intent: Robustness** | Define the complete architecture, prioritizing **maximum data retrieval stability** by mandating a primary method and a **guaranteed *fallback***. | **Constraint-Driven Prompting:** Used to set the **core engineering requirement**: "If the `binance-connector` is unavailable or fails, implement a separate, native `requests`-based function to handle the entire pagination and API call logic." | Focus on the `try/except` block and the `_fetch_klines_connector` / `_fetch_klines_requests` functions in `criptodata`. |
| **2. Modular Engineering: Time Series Logic** | Develop precise, reusable helper functions for core time-series and data handling logic, independent of the fetching mechanism. | **Abstraction & Helper Prompting:** Mandated the creation of utility functions for common tasks like *timestamp* conversion (`_to_millis`) and complex response parsing (`_parse_klines_response`). | Focus on `_parse_klines_response`, which handles *all* 12 fields of the raw API response and prepares the final `pandas` `DataFrame` with `Date` index. |
| **3. Reliability Implementation: Pagination & Rate Limits** | Ensure the *fallback* REST API logic correctly handles Binance's pagination and includes rate-limiting safeguards. | **Chain-of-Thought (CoT) Prompting:** Requesting the AI to detail the logic for iterative fetching using `startTime`/`endTime` parameters and calculating the `next_start` value from the last candle's open time. | Focus on the `while True` loop, `limit` checks, and the crucial `next_start = last_open_time + 1` logic within `_fetch_klines_requests`. |

This approach demonstrates **AI Fluency** by leveraging the model to generate not just working code, but code that addresses **non-functional requirements** (robustness, dependency management) and best practices (docstrings, type hints, security via environment variables).

1.  **Translate Complex Financial Requirements** into modular, production-ready Python code via structured prompts (AI Fluency).
2.  **Architect Robust Code:** The tool is engineered for high reliability, featuring an automated fallback to direct REST API calls (using `requests`) if the official Binance connector library is unavailable or fails, ensuring maximum data retrieval stability.
3.  **Establish a Data Foundation** for advanced **Quantitative Finance** and **Machine Learning** projects by enforcing data quality standards (DatetimeIndex, Float types).

By focusing on prompt structure and iterative refinement, this repository validates a crucial workflow for **financial software engineers** operating in the AI-centric era.

---

### Overview
This repository demonstrates how prompt engineering accelerates the development of robust financial tooling.
It documents prompt design, model iterations, generated code examples, and a small test-suite validating parsing behavior.
The extractor focuses on Binance USDT‑M futures public klines and provides a portable, well-documented foundation for quant research.

### Quick links
- Core library: src/binance_ohlcv_extractor/
- CLI: python -m binance_ohlcv_extractor.cli
- Prompts: prompts/
- Iterations & validation: testing_validation_by_model/
- Docs: docs/

### Quickstart (1-minute)
1. Create and activate a virtual environment:
   - python -m venv .venv && source .venv/bin/activate  (Unix)
   - python -m venv .venv && .venv\Scripts\activate     (Windows)
2. Install:
   - pip install -r requirements.txt
3. Run:
   - python -m binance_ohlcv_extractor.cli --symbols BTCUSDT ETHUSDT --start 2021-01-01 --interval 1d --out ./binance_futures_csvs

### What this project contains
- A prompt-driven process that produced multiple code examples (ChatGPT-5, Claude, Gemini).
- A small, tested core module that parses Binance klines and exports CSVs.
- Documentation on prompt architecture, evaluation rubrics, and iteration logs.

Repository conventions
- Language: English for all user-facing documentation and printed messages.
- Provenance: every generated code file should include a short header with model, prompt_id, generation timestamp and run parameters.
- Golden outputs: store model outputs and metadata under testing_validation_by_model/golden_outputs/<model>/<timestamp>/

### Contributing
Contributions are welcome. Please follow these steps:
1. Fork the repository.
2. Create a topic branch for your change.
3. Add tests for any behavioral change.
4. Open a PR and reference the relevant prompt_id when contributing improvements to prompts/code generation.

### Security
- Public klines endpoint does not require API keys.
- If you use API keys for authenticated endpoints, load them from environment variables or a local .env file and never commit secrets.
- If you find secrets in the repository, report them following SECURITY.md (create if missing) or open an issue.

### License
This project is distributed under the MIT license. See LICENSE for details.

### Acknowledgements
- Demonstrates human-in-the-loop prompt engineering and evaluation for robust financial tooling.
- Examples generated using multiple LLMs; see testing_validation_by_model/ for iteration histories.

### Contact / Maintainer
- Repository owner: alearisteguieta
- For major changes or security issues please open an issue or PR.

### Architecture: Dependency‑Fallback Flow
 - The extractor prioritizes reliability by attempting a connector path and gracefully falling back to a native REST path with robust pagination.

```
+----------------------------+
|   Start Extraction (CLI)   |
+-------------+--------------+
              |
              v
     +--------+---------+
     |  Try binance-    |
     |  connector path  |
     |  (if installed)  |
     +--------+---------+
              | success?
        +-----+-----+
        |           |
       Yes         No / Error
        |           |
        v           v
+-------+--+   +----+-------------------+
| Fetch via |   |  Fallback to REST     |
| connector |   |  (requests + pagination)|
+-------+--+   +----+-------------------+
        |               |
        v               v
+-------+---------------+--------------------------+
| Parse klines -> DataFrame (Date index, floats)  |
+-----------------------+-------------------------+
                        |
                        v
         +--------------+---------------+
         |  Filter to requested window  |
         +--------------+---------------+
                        |
                        v
         +--------------+---------------+
         |  Write CSV per symbol        |
         +--------------+---------------+
                        |
                        v
                "Data extraction finished :)"
```

---
