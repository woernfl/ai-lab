---
name: commit-push
description: Stage current git changes, generate a Conventional Commit message, commit, and push safely to the remote. Use when the user says "commit and push", "push my changes", "ship this", "save and push", "wrap this up", "commit my work", or otherwise wants the current work committed and pushed. Before committing, make sure the work is not going straight to a shared branch; if HEAD is on main, master, develop, trunk, or a release branch, create and switch to a feature branch first.
---

# Commit & Push Workflow

Execute the following steps in order. Stop and report clearly if any step fails. Prefer safe, explicit behavior over guessing.

## Step 0 — Make sure we are on a feature branch

Check the current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

- If the output is HEAD → stop. Explain that the repository is in a detached HEAD state and ask the user how to proceed.
- If the branch is main, master, develop, trunk, or matches release/*:
  - Derive a short kebab-case slug from the current change, for example update-readme-links.
  - Create and switch to a feature branch named feat/<slug>.
  - If that branch name already exists, append a short timestamp suffix.
  - Tell the user which branch was created before continuing.
- Otherwise → continue.

## Step 1 — Check working tree

```bash
git status --short
```

- If the output is empty → tell the user there is nothing to commit and stop.
- If files are already staged → proceed directly to Step 2.
- If there are unstaged or untracked changes → stage them first:

```bash
git add -A
git status --short
```

Quickly inspect the staged paths. If anything looks unintended, risky, or surprising for a commit (for example generated artifacts, secrets, or large binaries), stop and ask the user before continuing.

## Step 2 — Inspect the diff

```bash
git diff --cached --stat
git diff --cached
```

Read the full staged diff to understand what changed before writing the message.

## Step 3 — Generate and apply the commit message

Produce a Conventional Commit message:

```text
<type>(<scope>): <short summary>

<body — optional, explain the why not the what>

<footer — optional, e.g. Closes #123>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci, build, style

Rules:

- Summary line: imperative mood, max 72 chars, no period at end
- Body: wrap at 100 chars, explain why the change was made
- If the change is trivial, omit the body

Show the user the exact message that will be used before committing.

Then commit using that message.

Show the user the exact message used.

## Step 4 — Push

First make sure origin exists:

```bash
git remote get-url origin
```

- If origin does not exist → stop, report the issue clearly, and do not guess a different remote.

Then push:

```bash
git push -u origin HEAD
```

- If the push is rejected because it is non-fast-forward → stop immediately, explain that the remote has commits that are not present locally, and ask the user how to proceed.
- Never force-push without explicit user confirmation, because force-pushing can rewrite shared history.
- If authentication fails → stop and show the exact error.

## Step 5 — Report

Print a short summary:

- Commit hash (short) and message
- Branch pushed
- Remote pushed to
- Remote URL, if available via git remote get-url origin

Use these commands where helpful:

```bash
git rev-parse --short HEAD
git rev-parse --abbrev-ref HEAD
git log -1 --pretty=%s
git remote get-url origin
```

If the remote is GitHub, GitLab, or Bitbucket, also include a compare or pull-request URL when it can be derived safely from the remote URL and branch name.
 
