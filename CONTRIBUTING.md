# Contributing

Thank you for your interest in contributing to the Binance‑Futures‑OHLCV‑Extractor project! This document explains how to report issues, propose changes, run tests, and prepare pull requests so maintainers can review and merge your work quickly.

If you are joining for the first time, welcome — your contributions help make this project more robust and more useful for the community.

## Table of contents
- [Code of Conduct](#code-of-conduct)
- [How can I contribute?](#how-can-i-contribute)
  - [Report a bug or request a feature](#report-a-bug-or-request-a-feature)
  - [Propose a change (Pull Request)](#propose-a-change-pull-request)
- [Development setup](#development-setup)
- [Tests and CI](#tests-and-ci)
- [Coding style & linters](#coding-style--linters)
- [Commit messages and branch naming](#commit-messages-and-branch-naming)
- [Pull request checklist](#pull-request-checklist)
- [Security issues](#security-issues)
- [Maintainer contact & support](#maintainer-contact--support)

## Code of Conduct
Please read and follow the [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md). Be respectful and constructive in issues, PRs, and discussions.

## How can I contribute?

### Report a bug or request a feature
1. Search existing issues to see if someone already reported the same problem.
2. If none exists, open a new issue and include:
   - A clear title.
   - A short description of the problem or feature request.
   - Steps to reproduce (for bugs), including OS, Python version and commands used.
   - Expected behavior vs actual behavior.
   - Minimal reproducible example or logs if relevant.

Use the issue templates (if available) to make reporting easier.

### Propose a change (Pull Request)
1. Fork the repository and create a feature branch from `main`:
   - Branch name examples: `feat/add-cli-options`, `fix/pagination-bug`, `docs/update-prompts`.
2. Implement your change and add tests where appropriate.
3. Run the test suite and linters locally.
4. Push your branch and open a Pull Request against `main`.
5. In the PR description, include:
   - A summary of changes.
   - Why the change is needed (link to an issue if applicable).
   - Any migration steps or breaking changes.
   - The prompt_id or prompt file if the change affects prompt artifacts.

## Development setup
Quick start (recommended):
1. Create and activate a virtual environment:
   - Unix/macOS:
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Install base dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install dev dependencies (optional):
   ```
   pip install -r requirements-dev.txt
   ```
4. Run the CLI locally as a smoke test:
   ```
   python -m binance_ohlcv_extractor.cli --symbols BTCUSDT --start 2021-01-01 --interval 1d --out ./out
   ```

If the project uses `python-dotenv`, you can create a `.env` file (do not commit it) and copy `.env.example` for local variables.

## Tests and CI
- Run unit tests with:
  ```
  pytest -q
  ```
- The repository includes GitHub Actions CI that runs tests and linters on PRs. Ensure your branch passes CI before requesting a review.

If your change adds functionality, include tests that cover the new behavior. Prefer mocking network calls when appropriate to make tests deterministic.

## Coding style & linters
- Follow PEP 8 for Python code.
- Use `black` for formatting and `isort` for imports.
- Before opening a PR, format and lint your changes:
  ```
  black .
  isort .
  flake8
  ```
- Keep PRs small and focused to ease review.

## Commit messages and branch naming
- Use clear, imperative-style commit messages (e.g., `fix: handle empty kline response`).
- Use branch names that describe the change and include a category (e.g., `feat/`, `fix/`, `docs/`, `test/`).

## Pull request checklist
Before requesting a review, ensure your PR:
- [ ] Has a descriptive title and summary.
- [ ] References the issue it resolves (if any).
- [ ] Contains tests for new functionality or a reason why tests are not needed.
- [ ] Passes all CI checks (tests & linters).
- [ ] Includes updates to docs or prompts if behavior changed.
- [ ] Does not include secrets, credentials, or large binary files.

Example PR description template:
- Summary of changes
- Related issue: #NNN
- How to test
- Checklist (tests, lint, docs updated)

## Security issues
If you discover a security vulnerability (e.g., leaked secrets), do NOT open a public issue. Instead follow the instructions in [SECURITY.md](./SECURITY.md) or contact the maintainer directly by email if the file provides one.

## Maintainer contact & support
- Repository owner / maintainer: @alearisteguieta
- For major changes, open an issue first to discuss the approach.
- Thank you for contributing — we appreciate your time and effort!
```
