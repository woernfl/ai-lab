---
description: Diagnose and fix a bug or error
argument-hint: "<error message or description>"
---
Diagnose and fix: ${1:-the bug or error described above}.

Follow this process:
1. **Root cause** — identify exactly what is going wrong and why
2. **Fix** — apply the minimal correct change; do not refactor unrelated code
3. **Verify** — explain how to confirm the fix works (test command, expected output, etc.)
4. **Prevent** — if relevant, suggest a guard (assertion, type check, test) to prevent regression

If multiple plausible causes exist, address the most likely one first and briefly note the others.
