# Security Posture and Key Handling

## Overview

### This project extracts public OHLCV data from Binance USDT‑M futures. The klines endpoint is public and does not require authentication. Nevertheless, this repository follows baseline security practices suitable for financial tooling and future extensions that might require authenticated endpoints.

### Threat Model (Scope)

- In scope
    - Accidental credential exposure in code or logs
    - Unsafe local configuration and .env handling
    - Data integrity issues due to partial downloads or pagination errors
    - Supply‑chain risks via third‑party Python dependencies
- Out of scope
    - Exchange account compromise beyond this codebase
    - Network‑level attacks, DDoS mitigation, or endpoint availability
    - Full operational security for production deployments

Secrets and Configuration

- No hardcoded secrets
    - Do not commit API keys or tokens. Avoid sample values that resemble real credentials.
- Environment variables
    - Prefer environment variables for any future authenticated extension, e.g.:
        - BINANCE_API_KEY
        - BINANCE_API_SECRET
    - Consider using a local .env file for development only. Never commit .env files.
- Secret managers (recommended for production)
    - Use your cloud secret manager or Vault‑like solution for deployed environments.
    - Rotate credentials regularly and enforce least‑privilege access.

Logging and Output

- No sensitive data in logs
    - Avoid printing secrets, headers, or signed URLs.
- Minimal logging for network calls
    - Log request parameters only when they do not contain sensitive data.
    - Prefer structured logging with levels (INFO, WARNING, ERROR).

Dependency and Build Hygiene

- Pinned dependencies
    - Use pinned versions in requirements.txt or pyproject to reduce supply‑chain drift.
- Verification
    - Review release notes before version bumps.
    - Run CI tests (lint + unit tests) on pull requests.
- Isolation
    - Use a virtual environment (venv) to isolate dependencies per project.

Network, Rate Limits, and Resilience

- Public endpoint usage
    - The klines endpoint is public; API keys are not required for extraction.
- Pagination safety
    - The extractor paginates with strict windowing and avoids overlaps via next_start = last_open_time + 1.
- Backoff
    - Use short sleeps between calls to reduce throttling risk and be a “good citizen.”
    - Consider exponential backoff for transient failures in production workloads.

Data Integrity and Validation

- Canonical types
    - Enforce float numeric types for OHLCV columns and DatetimeIndex for Date.
- Range checks
    - Filter results to requested start/end bounds to avoid partial window “bleed.”
- Determinism
    - Ensure repeated runs over the same window produce identical CSVs (unless upstream data changes).

Local Development Practices

- .env handling
    - If you use python‑dotenv locally, add .env to .gitignore and do not commit it.
- Sample configs
    - Provide examples via .env.example without real values.
- File permissions
    - Avoid world‑readable secrets; restrict to the minimum needed for local development.

Responsible Disclosure

If you discover a security issue or potential vulnerability related to this project, please open a minimal, non‑sensitive issue describing the symptom and impact. Do not include secrets. The maintainers will coordinate follow‑up and remediation.

License and Warranty

This project is provided “as is,” without warranty. Users are responsible for ensuring compliance with their organization’s security policies and regulatory requirements.
