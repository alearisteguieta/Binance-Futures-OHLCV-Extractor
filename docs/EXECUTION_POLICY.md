# Example Code Execution Policy (short)

Purpose
This short policy clarifies the repository's stance on running the example scripts included as part of the learning materials.

Key points
- Educational only: Example scripts and model-generated code are provided for study and adaptation. They are not guaranteed to be runnable or safe by default.
- Review required: Before executing any example locally, inspect the file to:
  - Ensure no hardcoded secrets, tokens, or personal data are present.
  - Confirm required dependencies and their versions.
  - Understand any network requests or external side effects.
- Local-only execution: If you run an example, do so on a machine/environment you control. Prefer a disposable virtualenv or container.
- Responsibility: The repository authors provide examples for education. Running code is at the user’s own risk.

Suggested labeling for example files
- Add a short header at the top of each example file:

```text
# NOTE: This file is an educational example produced during prompt-engineering iterations.
# It is provided for reading and learning purposes only. Review carefully before running.
```

Recommended file organization
- Move executable-looking scripts into an `examples/` or `code_examples_readonly/` folder and rename them to `*.example.py` or embed them in markdown with syntax highlighting to discourage direct execution.

Contact
If you find examples that look unsafe or contain secrets, please open an issue or contact the maintainer.
```
