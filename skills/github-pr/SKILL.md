---
name: github-pr
description: Commit staged or local changes, push the branch, then open a Pull Request on GitHub using the GitHub MCP by default, falling back to the gh CLI when MCP tools are unavailable. Use when the user says "open a PR", "create a pull request", or "submit for review".
---

# Pull Request Workflow

Execute the following steps **in order**. Stop and report clearly if any step fails.

## Step 0 — Determine GitHub access method

Use the **GitHub MCP server by default**; fall back to the **`gh` CLI** only when the GitHub MCP tools are not available.

**Preferred: GitHub MCP.** If GitHub MCP tools (such as `create_pull_request`) are available in the current environment, use them for all GitHub operations in this skill.

**Fallback: gh CLI.** If the GitHub MCP tools are not available, use the `gh` CLI instead:

```bash
gh --version
```

If `gh` is not found:

1. Tell the user: "`gh` CLI is required for this skill when the GitHub MCP server is not available."
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

Do not mix methods within a single run: pick one access method in this step and use it consistently.

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

If the branch has no upstream yet:

```bash
git push --set-upstream origin HEAD
```

**GitHub MCP (preferred):** call the GitHub MCP `create_pull_request` tool with the owner, repo, head branch, base branch, title, and body/description. Report the returned PR URL.

**gh CLI (fallback):**

```bash
gh pr create \
  --base <base-branch> \
  --title "<title>" \
  --body "<description>"
```

If the push failed because the branch had no upstream, retry after `git push --set-upstream origin HEAD`.

## Step 5 — Report

Print:

- Title, base branch
- PR URL (returned by `create_pull_request` via MCP, or by `gh pr create` via CLI)
