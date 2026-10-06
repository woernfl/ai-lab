---
description: Review code for bugs, security issues, and quality
argument-hint: "[file or description]"
---

Review ${1:-the current code or staged diff (`git diff --cached`)} carefully. Structure your feedback as follows:

## Bugs & Logic Errors

List any bugs, off-by-one errors, null/undefined issues, or incorrect assumptions.

## Security Issues

Look for injection vulnerabilities, exposed secrets, insecure defaults, or missing input validation.

## Error Handling

Flag missing error handling, silent failures, or cases where errors are swallowed.

## Design & Maintainability

Note anything that will be hard to extend or understand in 6 months.

## Positives

Briefly mention what's done well.

Be specific: quote the relevant lines and explain _why_ each issue matters.

## Finding IDs

Assign every finding (except Positives) a unique ID so it can be referenced later (e.g. "post BUG-1, SEC-2 inline"):

- Prefix per section: `BUG-` (Bugs & Logic Errors), `SEC-` (Security Issues), `ERR-` (Error Handling), `DES-` (Design & Maintainability).
- Number sequentially within each section, starting at 1 (`BUG-1`, `BUG-2`, ...). Do not reuse or renumber IDs within the same review.
- Start each finding with its ID in bold, e.g. `**BUG-1 — Short title** — \`file:line\``.
- Use the same IDs in any follow-up summary, and when posting a finding as a PR comment, start the comment with its ID in brackets, e.g. `[BUG-1]`.
