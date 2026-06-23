# AI Toolbox

A central repository that groups **skills**, **agents**, **prompts**, and **MCP configurations** into a single place, making them easy to plug into any project.

## Table of Contents

- [Overview](#overview)
- [Skills Catalog](#skills-catalog)
- [Prompts Catalog](#prompts-catalog)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`AI Toolbox` is a living library of reusable AI building blocks for Claude AI:

- **Skills** — self-contained prompt instructions (`SKILL.md`) that guide Claude's behavior for a specific domain, bundled with optional scripts, reference docs, and assets.
- **Agents** — specialized sub-agents that can be orchestrated by skills or called directly.
- **Prompts** — standalone prompt templates that can be used directly in conversations without requiring a skill wrapper.
- **MCP Configurations** — ready-to-use Model Context Protocol configurations to wire tools and context providers into your projects.

Skills follow a **three-level progressive loading** model:

| Level | What is loaded | When |
|-------|---------------|------|
| 1 | Skill name + description (~100 words) | Always |
| 2 | `SKILL.md` body (<500 lines ideal) | When the skill is triggered |
| 3 | Bundled resources (scripts, references, assets) | On demand |

---

## Skills Catalog

| Skill | Description | Trigger phrases |
|-------|-------------|-----------------|
| 🔍 **ai-prompt-engineering-safety-review** | Analyzes AI prompts for safety, bias, security vulnerabilities, and effectiveness. Scores prompts across multiple dimensions and produces an improved version with testing recommendations. | "review my prompt", "is this prompt safe", "improve this prompt" |
| 🎯 **clarify** | Relentlessly interviews users about plans or designs until shared understanding is reached, resolving every branch of the decision tree one question at a time. | "clarify", "review my plan", "stress-test my design" |
| 📤 **commit-push** | Stages uncommitted changes, generates a Conventional Commit message, commits, then pushes to the remote branch in one workflow. | "commit and push", "ship this", "push my changes" |
| 📝 **doc-coauthoring** | Structured three-stage workflow (context gathering → section drafting → reader testing) for collaboratively writing proposals, specs, decision docs, and RFCs. | "write a doc", "draft a proposal", "create a spec", "PRD", "design doc" |
| 🐳 **docker-expert** | Advanced Docker containerization expertise covering multi-stage builds, security hardening, Compose orchestration, image optimization, and production deployment patterns. | "Dockerfile", "containerize", "docker compose", "optimize image" |
| 📌 **git-commit** | Creates git commits following the Conventional Commits standard (`type(scope): subject`) with enforced scope, imperative tense, and 50-character subject limit. | "commit", "create commit", "save work", "stage and commit" |
| 🔄 **github-pr-review** | Fetches PR review comments, classifies them by severity (CRITICAL → LOW), applies fixes with user confirmation, commits with proper format, and replies to threads. | "resolve PR comments", "handle review feedback", "fix review comments", "address PR review" |
| ☸️ **kubernetes-architect** | Expert Kubernetes architect covering cluster design, advanced GitOps (ArgoCD/Flux), service mesh (Istio, Linkerd), RBAC/NetworkPolicy, and observability stacks. | "kubernetes architecture", "k8s design", "gitops", "service mesh" |
| 🚀 **kubernetes-deployment** | End-to-end Kubernetes deployment workflow across seven phases: container prep, manifests, Helm charts, service mesh, security, observability, and CI/CD. | "deploy to kubernetes", "helm chart", "k8s deployment", "production deployment" |
| 🔀 **pr** | Commits staged or local changes, pushes the branch, then opens a Pull Request on GitHub using the `gh` CLI in one end-to-end workflow. | "open a PR", "create a pull request", "submit for review" |
| 🛠️ **skill-creator** | Meta-skill for creating, improving, and benchmarking other skills. Runs evaluation loops, benchmarks with variance analysis, and optimizes skill descriptions for better triggering. | "create a skill", "improve this skill", "benchmark skill", "optimize skill description" |

---

## Prompts Catalog

| Prompt | Description | When to use |
|--------|-------------|-------------|
| 📄 **doc** | Add or improve documentation for code using the idiomatic doc format for the language (JSDoc, Python docstrings, GoDoc, etc.), focusing on *why* rather than *what*. | "document this function", "add docstrings", "improve the docs" |
| 🐛 **fix** | Diagnose and fix a bug or error: identify the root cause, apply the minimal correct change, verify the fix, and suggest a regression guard. | "fix this bug", "diagnose this error", "why is this failing" |
| 🔎 **review** | Review code for bugs, security issues, error handling gaps, and design/maintainability concerns, structured into labelled sections with specific line references. | "review this code", "check for issues", "audit this diff" |

---

## Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/woernfl/ai-lab.git
   ```

2. **Point your AI agent at the `skills/` directory** (or the `.agents/` symlink) so it can discover and load skills.

3. **Invoke a skill** by using one of its trigger phrases in your conversation. The agent will load the relevant `SKILL.md` and any supporting resources automatically.

4. **Create a new skill** using the `skill-creator` skill, which walks you through the entire authoring, evaluation, and optimization process.

---

## Contributing

Contributions are welcome! To add or improve a **skill**:

1. Fork the repository and create a feature branch.
2. Place your skill in a new folder under `skills/` following the standard layout.
3. Keep `SKILL.md` under 500 lines; move large content to `references/`.
4. Write a few test prompts and validate the skill using the `skill-creator` evaluation tooling.
5. Open a pull request with a clear description of what the skill does and when it should trigger.

To add or improve a **prompt**:

1. Fork the repository and create a feature branch.
2. Create a new `.md` file under `prompts/` named after the action (e.g., `prompts/refactor.md`).
3. Add a YAML front-matter block at the top with `description` and (optionally) `argument-hint` fields.
4. Keep the prompt body focused and concise — one clear task per prompt.
5. Open a pull request with a description of the use case and example trigger phrases.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright © 2026 Florian Woerner