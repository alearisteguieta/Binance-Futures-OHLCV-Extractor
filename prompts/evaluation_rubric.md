# Evaluation rubric for generated outputs

Total score: 100 points

1. DataFrame and CSV correctness (0–40)
- 40: DataFrame has Date as DatetimeIndex in UTC; columns exact and types correct.
- 20: DataFrame correct but timezone wrong or date format inconsistent.
- 0: Fails to generate DataFrame or incorrect columns.

2. Robustness (0–20)
- Retries for 429/5xx responses: 10 points
- Correct pagination for long ranges: 10 points

3. Security (0–10)
- No hardcoded secrets and correct use of environment variables: 10 points

4. Code quality (0–20)
- Modularity (reusable functions): 10 points
- Comments and clarity: 10 points

5. Console UX (0–10)
- Progress messages and final message: 10 points
