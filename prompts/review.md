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
