---
description: Implement a spec end-to-end with a verification feedback loop
argument-hint: "<spec-path-or-text>"
---

Implement the following spec end-to-end:

$@

If the first argument looks like a readable file path, read that file first and use it as the primary spec source. Otherwise, treat the provided arguments as the spec text.

Workflow:

1. Understand the spec before changing anything.
   - Restate the goal in your own words.
   - Break the spec into a concrete checklist of discrete requirements.
   - Call out any ambiguity, dependency, or missing assumption before implementation.

2. Plan the implementation.
   - Identify the files, modules, tests, configs, and docs that likely need changes.
   - Decide the smallest safe implementation order.
   - Keep the work scoped to the spec.

3. Implement incrementally.
   - Complete one requirement or closely related requirement group at a time.
   - Keep edits minimal, coherent, and easy to review.
   - Update tests, fixtures, and documentation when the spec requires them.

4. Run a verification feedback loop after each implemented requirement.
   - Re-read the relevant checklist item from the spec.
   - Compare the implementation directly against that requirement.
   - Run the best available validation for that change, such as tests, linting, build steps, smoke checks, or targeted inspection.
   - Mark the checklist item as:
     - Implemented and verified
     - Implemented but not yet verified
     - Not fully implemented
   - If anything is incomplete, incorrect, or unverified, fix it before moving on.

5. Perform a final spec coverage review.
   - Re-walk the full checklist from top to bottom.
   - Confirm every requested feature is actually present, not just partially coded.
   - Confirm related validation passed, or clearly explain any gap.
   - Highlight edge cases, regressions avoided, and any follow-up work still needed.

6. Report the result clearly.
   - Summarize what changed.
   - Provide a requirement coverage table in this format:

     | Requirement | Status | Verification |
     | ----------- | ------ | ------------ |

   - List the exact validation steps performed and their outcomes.
   - Explicitly state whether the spec is fully implemented.

Important emphasis:

- Do not assume a feature is complete just because code was written.
- Use the spec as the source of truth throughout the task.
- Double-check that each implemented feature behaves as requested before declaring completion.
- If the spec and the code diverge, continue iterating until they match or clearly explain the blocker.
