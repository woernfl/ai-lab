---
name: commit-push
description: Stage uncommitted changes, generate a Conventional Commit message, commit, then push to the remote. Use when the user says "commit and push", "ship this", or "push my changes".
---

# Commit & Push Workflow

Execute the following steps **in order**. Stop and report clearly if any step fails.

## Step 1 — Check working tree

```bash
git status --short
```

- If the output is empty → tell the user there is nothing to commit and stop.
- If files are already staged → proceed directly to Step 2.

## Step 2 — Inspect the diff

```bash
git diff --cached --stat
git diff --cached
```

Read the full diff to understand what changed before writing the message.

## Step 3 — Generate and apply the commit message

Produce a **Conventional Commit** message:

```text
<type>(<scope>): <short summary>

<body — optional, explain the why not the what>

<footer — optional, e.g. Closes #123>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `build`, `style`

Rules:

- Summary line: imperative mood, max 72 chars, no period at end
- Body: wrap at 100 chars, explain _why_ the change was made
- If the change is trivial, omit the body

Then commit.

Show the user the exact message used.

## Step 4 — Push

```bash
git push -u origin HEAD
```

- If the push is **rejected** (non-fast-forward) → stop immediately, explain why, and ask the user how to proceed. **Never force-push without explicit user confirmation.**

## Step 5 — Report

Print a short summary:

- Commit hash (short) and message
- Branch and remote pushed to
- Remote URL (if available via `git remote get-url origin`)
