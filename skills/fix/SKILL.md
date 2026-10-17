---
name: fix
description: Diagnose and fix a bug or error by identifying the root cause, applying the minimal correct change, verifying the fix, and suggesting a regression guard. Use when the user says "fix this bug", "diagnose this error", "why is this failing", "this is broken", or otherwise wants a bug or error fixed.
---

# Bug Fix Workflow

Diagnose and fix the bug or error the user described.

Follow this process:

1. **Root cause** — identify exactly what is going wrong and why
2. **Fix** — apply the minimal correct change; do not refactor unrelated code
3. **Verify** — explain how to confirm the fix works (test command, expected output, etc.)
4. **Prevent** — if relevant, suggest a guard (assertion, type check, test) to prevent regression

If multiple plausible causes exist, address the most likely one first and briefly note the others.
