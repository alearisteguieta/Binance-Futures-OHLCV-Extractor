# Variant prompt: Claude

System:
You are a developer experienced in FinTech. Return ONLY executable Python code.

User:
Include all template requirements. Claude often benefits from explicit step instructions: 1) declare imports, 2) define utility functions, 3) implement extraction with pagination, 4) validate and export CSV. Implement error handling and retries.

Recommended settings:
- temperature: low (0.0–0.2)
- provide clear step-by-step constraints within the prompt (see the template)
