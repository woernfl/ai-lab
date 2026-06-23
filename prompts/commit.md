---
description: Generate a conventional commit message from staged changes
---
Look at the staged git changes (`git diff --cached`) and generate a commit message following the Conventional Commits specification.

Format:
```
<type>(<scope>): <short summary>

<body — optional, explain the why not the what>

<footer — optional, e.g. Closes #123>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `build`, `style`

Rules:
- Summary line: imperative mood, max 72 chars, no period at end
- Body: wrap at 100 chars, explain *why* the change was made
- If the change is trivial, omit the body

Output only the commit message, no commentary.
