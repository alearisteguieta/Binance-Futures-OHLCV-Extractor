# Variant Prompt: Claude

**Metadata**  
- **Model:** Claude  
- **Prompt version:** v1.0 (financial framework integration)  
- **Date:** 2025‑10‑02  
- **Provenance:** Derived from `prompts/financial_framework_template.md`  
- **Generated file naming convention:**  
  - Scripts should be saved as `extractor_claude_<date>.py` (e.g., `extractor_claude_2025-10-02.py`)  
  - CSV outputs should follow `<symbol>_<interval>_<start>_<end>.csv` (e.g., `BTCUSDT_1h_2021-01-01_2021-12-31.csv`)  

---

## Message Template

### System
You are a developer experienced in FinTech.  
Return **ONLY** executable Python code.  
Do not include explanations, comments, or text outside the code block.  

### User
Include all template requirements. Claude often benefits from explicit step instructions:  
1. Declare imports  
2. Define utility functions  
3. Implement extraction with pagination  
4. Validate and export CSV  

Additional requirements:  
- Implement error handling and retries.  
- Use environment variables for API keys (no hardcoded secrets).  
- Ensure CSV columns are: `Date, Open, High, Low, Close, Volume`.  
- `Date` must be a `DatetimeIndex` in UTC.  

### Expected Output Format
- The model must return **only one fenced code block** containing the complete Python script.  
- No prose, explanations, or additional formatting outside the code block.  

---

## Recommended Settings
- **temperature:** 0.0–0.2 (low, for determinism)  
- **max_tokens:** 2500  
- **top_p:** 1.0  
- **stop:** null  

---

## Example System + User Message Pair

**System:**  
```
You are a developer experienced in FinTech. Return ONLY executable Python code.
```

**User:**  

Include all template requirements. Claude often benefits from explicit step instructions:
1) declare imports
2) define utility functions
3) implement extraction with pagination
4) validate and export CSV
Implement error handling and retries.
Use environment variables for API keys.
Ensure CSV columns are Date, Open, High, Low, Close, Volume and that Date is a DatetimeIndex in UTC.


---

## Notes
- This version corrects truncation issues and ensures the full specification is present.  
- Explicit **system + user message pair** is documented for reproducibility.  
- Metadata and provenance are included for version tracking.  
- File naming conventions are standardized for generated scripts and CSV outputs.  

