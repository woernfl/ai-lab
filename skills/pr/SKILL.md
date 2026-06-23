---
name: pr
description: Commit staged or local changes, push the branch, then open a Pull Request on GitHub using the gh CLI. Use when the user says "open a PR", "create a pull request", or "submit for review".
---

# Pull Request Workflow

Execute the following steps **in order**. Stop and report clearly if any step fails.

## Step 0 — Check for gh CLI

```bash
gh --version
```

If `gh` is not found:

1. Tell the user: "`gh` CLI is required for this skill."
2. Provide the install command:
   ```bash
   brew install gh   # macOS
   # or: https://cli.github.com/
   ```
3. After install, authenticate:
   ```bash
   gh auth login
   ```
4. Then re-run this skill.

## Step 1 — Ensure changes are committed

```bash
git status --short
```

- If there are staged → run the **commit-push** workflow first:
  - Generate a Conventional Commit message from `git diff --cached`
  - Commit and push (see commit-push skill for full rules)
- If the working tree is already clean and the branch is pushed → skip to Step 2.

## Step 2 — Determine base branch

```bash
git remote show origin | grep "HEAD branch"
```

Use the result (usually `main` or `master`) as the base. If ambiguous, ask the user.

## Step 3 — Gather PR metadata

Ask the user (or infer from recent commits and branch name) for:

- **Title** — short, imperative, describes the change (default: use the last commit subject)
- **Description** — what changed and why; include any relevant issue/ticket references

## Step 4 — Open the Pull Request

```bash
gh pr create \
  --base <base-branch> \
  --title "<title>" \
  --body "<description>"
```

If the branch has no upstream yet:

```bash
git push --set-upstream origin HEAD
```

Then retry `gh pr create`.

## Step 5 — Report

Print:

- Title, base branch
- PR URL (returned by `gh pr create`)
