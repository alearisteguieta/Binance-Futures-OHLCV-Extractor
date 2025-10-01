# prompts folder — Quick Guide

Purpose:
- Contain templates, model-specific variants, and documentation to reproduce and compare prompt outputs.

Recommended structure:
- financial_framework_template.md  # master template (provided)
- variants/
  - chatgpt_prompt.md
  - claude_prompt.md
  - gemini_prompt.md
- evaluation_rubric.md
- golden_outputs/  # example outputs per model (optional)
- README.md (this file)

Suggested workflow:
1. Use the master template to define requirements.
2. Select a model-specific variant in variants/ and call the model with the recommended parameters.
3. Save the generated script in golden_outputs/{model}/{timestamp}.py
4. Run the evaluation rubric against the generated script.
5. Iterate on prompts to improve outputs.

Tips:
- Keep each variant structured with "system" + "user" messages (or equivalent for the model API).
- Record temperature and max_tokens used for each run.
