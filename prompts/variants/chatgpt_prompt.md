# Variant Prompt: ChatGPT 5

**Metadata**  
- **Model:** ChatGPT 5  
- **Prompt version:** v1.0 (financial framework integration)  
- **Date:** 2025‑10‑02  

---

## Message Template

### System
You are an assistant expert in Python and financial APIs.  
Produce **ONLY** the requested Python code.  
Do not include explanations, comments, or additional text outside the code block.  

### User
Use the financial template (`prompts/financial_framework_template.md`).  
Generate a complete Python script implementing `extract_ohlcv(...)` and `main()`.  
- Use environment variables for API keys.  
- Handle pagination and retries.  
- Ensure the CSV columns are: `Date, Open, High, Low, Close, Volume`.  
- `Date` must be a `DatetimeIndex` in UTC.  

### Expected Output Format
- The model must return **only one fenced code block** containing the complete Python script.  
- No prose, explanations, or additional formatting outside the code block.  

---

## Recommended API Parameters
- **temperature:** 0.0  
- **max_tokens:** 2500  
- **top_p:** 1.0  
- **stop:** null  

---

## Notes
- This prompt ensures reproducibility by explicitly defining the **system + user** message template.  
- The expected output format is constrained to a single code block for deterministic parsing.  
- Pagination, retries, and environment‑based API key handling are mandatory.  
- This version corrects truncation issues and includes the full specification, including stop sequences and constraints.
