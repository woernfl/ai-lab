---
name: doc
description: Add or improve documentation for code using the idiomatic doc format for the language (JSDoc, Python docstrings, GoDoc, Rustdoc, etc.), focusing on why rather than what. Use when the user says "document this function", "add docstrings", "improve the docs", "document this module", or otherwise wants code documentation added or improved.
---

# Code Documentation

Add or improve documentation for the current file or the function/class the user showed you.

Guidelines:

- Use the idiomatic doc format for the language (JSDoc, Python docstrings, GoDoc, Rustdoc, etc.)
- Document **why**, not just **what** — the code already shows what; the docs should explain intent
- Include parameter descriptions, return values, and types where not obvious from the signature
- Add usage examples for non-trivial public APIs
- Flag any parameters with surprising behavior or important constraints

Do not add noise — skip obvious things like `// increments i by 1`.
