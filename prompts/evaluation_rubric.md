# Evaluation Rubric for Generated Outputs

Version: 2025-10-02
Purpose: Provide a clear, reproducible scoring rubric for assessing code artifacts produced by LLMs
and for tracking improvements between prompt iterations and model runs.

Total score: 100 points

Scoring breakdown
1. DataFrame and CSV correctness (0–40)
   - 40: DataFrame uses a DatetimeIndex in UTC, columns are exactly: Date, Open, High, Low, Close, Volume
     and numeric OHLCV columns are float dtypes. CSV preserves Date in ISO 8601 (UTC) format.
   - 20: DataFrame columns correct but timezone handling or formatting is inconsistent.
   - 0: Missing or incorrect DataFrame/CSV structure.

2. Robustness (0–20)
   - 10: Retries implemented for transient HTTP errors (429, 5xx) with exponential backoff.
   - 10: Correct pagination handling for long windows (uses MAX_LIMIT and advances next_start correctly).

3. Security (0–10)
   - 10: No hardcoded secrets in the code. Uses environment variables (or .env) and documents what to set.
   - 0: Any secrets, credentials or tokens found in repository or generated code.

4. Code Quality (0–20)
   - 10: Modular structure (small reusable functions, clear public API functions).
   - 10: Clear inline comments and a module-level docstring describing purpose, inputs and outputs.

5. Console UX & Documentation (0–10)
   - 10: Clear progress messages, final confirmation message ("Data extraction finished :)"), and README usage examples.
   - 0: Poor or missing user-facing messaging and documentation.

Additional evaluation metadata to record with each run
- model: e.g., chatgpt-5, claude-2
- prompt_file: prompts/financial_framework_template.md
- prompt_version: yyyy-mm-dd or git commit SHA
- model_parameters: temperature, max_tokens, top_p, etc.
- run_timestamp: ISO 8601
- generated_filename: path to saved code sample (golden_outputs/.../*.py)
- evaluation_score: integer 0–100
- evaluator_notes: free-text observations

Example scoring snippet (for maintainers)
- data_correctness: 32/40
- robustness: 15/20
- security: 10/10
- code_quality: 16/20
- ux_docs: 8/10
- total: 81/100

Where to store results
- Save evaluations under: testing_validation_by_model/evaluations/<model>/<timestamp>.json
- Each evaluation file should include the metadata above and the computed numeric scores.

How to use this rubric
1. Run the generated script in an isolated environment (no real API keys required for public klines).
2. Verify DataFrame programmatically (unit tests or small validation script).
3. Assign scores according to the criteria and save a JSON evaluation file with the metadata.
4. Use evaluation files to drive prompt and model iteration decisions.
