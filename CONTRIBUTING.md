# Contributing (Docs & Prompts Focus)

Thank you for your interest in contributing! This repository is primarily a learning and documentation project about prompt engineering for financial tooling. Contributions that improve the pedagogical quality of the materials (prompts, docs, iteration notes, evaluations) are especially welcome.

Please follow these guidelines to make review and merging smoother.

What we welcome
- Improvements to prompt templates and model-variant prompts.
- Clearer documentation, tutorials, and walkthroughs that explain the thought process behind prompt changes.
- Better evaluation artifacts (structured metadata for runs, sample golden outputs, evaluation JSON).
- Corrections to prose, typos, and organization of docs.

What to avoid in contributions
- Adding real API keys or secrets (never commit secrets).
- Large binary files or full datasets (add references or small samples only).
- Changes that assume the repo provides runnable production code—our primary goal is educational clarity.

How to contribute
1. Fork the repo and create a branch: `docs/your-change` or `prompts/your-change`.
2. Make documentation or prompt edits. Small PRs merge faster.
3. If you change a prompt or evaluation, include:
   - The prompt_id or version
   - Model parameters used (if available)
   - A short note describing the intended improvement
4. Open a PR against `main` with a descriptive title and summary.

Documentation conventions
- Language: English for all user-facing docs.
- Each updated prompt should include a provenance header: prompt_id, version, date, and a short changelog entry.
- Keep examples short and focused; prefer small, annotated snippets rather than large executable scripts.

Testing & CI
- As this repo is documentation-first, tests should focus on validating parsing logic in small unit-tests only (if present).
- If you modify tests or code examples, ensure the change is accompanied by an explanation in the PR.

Code of Conduct & Security
- Please follow the project's CODE_OF_CONDUCT.md.
- Report sensitive security issues privately following SECURITY.md (do not open a public issue with secrets).

Thanks — your documentation-first improvements make this resource more valuable for learners.
```
