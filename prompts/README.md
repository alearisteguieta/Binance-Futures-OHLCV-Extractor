## Financial Prompt Framework:

This comprehensive prompt methodically deconstructs the problem space and articulates the solution requirements in a clear, accessible format for the LLM to generate complete Python code without unnecessary limitations or ambiguities. The carefully structured framework provides the AI with precise instructions regarding the financial domain context, specific programming requirements, and detailed code generation expectations. By organizing information into distinct sections covering domain context, functional requirements, technical specifications, and explicit instructions, the prompt creates a robust foundation for the AI to work from. This methodically organized approach enables thorough validation of the AI's decision-making process and allows the generated code to be rigorously tested and evaluated prior to actual implementation in a production environment. The prompt's clarity and comprehensive nature significantly enhance the likelihood of receiving high-quality, production-ready code that meets all specified requirements.

##  Prompts folder — Quick Guide

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
