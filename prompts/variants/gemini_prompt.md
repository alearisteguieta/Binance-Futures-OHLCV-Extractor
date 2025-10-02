# Gemini variant prompt:

```markdown
# Variant Prompt: Gemini

**Metadata**  
- **Model:** Gemini  
- **Prompt version:** v1.0 (financial framework integration)  
- **Date:** 2025‑10‑02  
- **Provenance:** Derived from `prompts/financial_framework_template.md`  
- **Generated file naming convention:**  
  - Scripts: `extractor_gemini_<date>.py` (e.g., `extractor_gemini_2025-10-02.py`)  
  - CSV outputs: `<symbol>_<interval>_<start>_<end>.csv` (e.g., `ETHUSDT_1d_2021-01-01_2021-12-31.csv`)  

---

## Message Template

### System
Generate **ONLY** Python code.  
Be concise and precise.  
Do not include explanations, comments, or text outside the code block.  

### User
Follow the template exactly and implement the required function structure.  
- Include logging with levels and messages per asset.  
- Do not print API keys.  
- Assume Python 3.10+.  
- Implement error handling and retries.  
- Ensure CSV columns are: `Date, Open, High, Low, Close, Volume`.  
- `Date` must be a `DatetimeIndex` in UTC.  

### Expected Output Format
- The model must return **only one fenced code block** containing the complete Python script.  
- If the model returns prose or any text outside the code block, **re‑prompt until only a single code block is returned**.  

---

## Recommended API Parameters
- **temperature:** 0.0  
- **max_output_tokens:** set sufficiently high depending on the API (e.g., 2500)  
- **top_p:** 1.0  
- **stop:** null  

---

## Example System + User Message Pair

**System:**  
```
Generate ONLY Python code. Be concise and precise.
```

**User:**  
```
Follow the template exactly and implement the required function structure.
Include logging with levels and messages per asset.
Do not print keys.
Assume Python 3.10+.
Implement error handling and retries.
Ensure CSV columns are Date, Open, High, Low, Close, Volume and that Date is a DatetimeIndex in UTC.
```

---

## Notes
- This version corrects truncation issues and ensures the full prompt text is included.  
- Explicit **system + user message pair** is documented for reproducibility.  
- Metadata and provenance are included for version tracking.  
- Stakes are added: if the model returns prose, re‑prompt until only a single code block is produced.  
- File naming conventions are standardized for generated scripts and CSV outputs.  
```
