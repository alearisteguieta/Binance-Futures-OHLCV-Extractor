## Financial Prompt Framework:

This comprehensive prompt methodically deconstructs the problem space and articulates the solution requirements in a clear, accessible format for the LLM to generate complete Python code without unnecessary limitations or ambiguities. The carefully structured framework provides the AI with precise instructions regarding the financial domain context, specific programming requirements, and detailed code generation expectations. By organizing information into distinct sections covering domain context, functional requirements, technical specifications, and explicit instructions, the prompt creates a robust foundation for the AI to work from. This methodically organized approach enables thorough validation of the AI's decision-making process and allows the generated code to be rigorously tested and evaluated prior to actual implementation in a production environment. The prompt's clarity and comprehensive nature significantly enhance the likelihood of receiving high-quality, production-ready code that meets all specified requirements.

## prompts — Quick Guide

Purpose
- Store the Financial Prompt Framework, model-specific prompt variants, evaluation rubrics, and golden outputs.
- Enable reproducible experiments and fair comparisons between LLMs.

Folder layout (recommended)
- financial_framework_template.md  — master prompt template (source of truth)
- variants/
  - chatgpt_prompt.md
  - claude_prompt.md
  - gemini_prompt.md
- evaluation_rubric.md
- golden_outputs/  — store generated code and metadata per run
- README.md (this file)

Recording policy (important)
- For each LLM run, save:
  - generated_code.py (the model output)
  - metadata.json with fields: { model, model_version, prompt_file, prompt_id, prompt_version, params, timestamp, git_commit }
- Example path: golden_outputs/chatgpt-5/2025-10-02_1200_v1/
  - code.py
  - metadata.json
  - evaluation.json

Recommended workflow
1. Edit prompts/financial_framework_template.md to change requirements.
2. Pick a variant in prompts/variants/ and run the model with the recommended parameters.
3. Save the raw model output in golden_outputs/<model>/<timestamp>/code.py plus metadata.json containing the prompt text and model params.
4. Run automated evaluation (use prompts/evaluation_rubric.md) and store results under testing_validation_by_model/evaluations/.
5. Iterate: refine the prompt, re-run, and compare evaluations.

Reproducibility tips
- Always record model parameters (temperature, max_tokens, top_p, stop).
- Keep prompt text used in metadata.json to reproduce runs exactly.
- Use a stable git commit SHA in metadata to ensure the code base version is recorded.

Example: minimal metadata.json
{
  "model": "chatgpt-5",
  "prompt_file": "prompts/financial_framework_template.md",
  "prompt_id": "ffw-2025-10-02-v1",
  "params": { "temperature": 0.0, "max_tokens": 2500 },
  "timestamp": "2025-10-02T12:00:00Z",
  "git_commit": "abcdef1234567890"
}
