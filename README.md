# ai-lab

A curated collection of specialized AI skills (reusable prompts and instructions) designed to guide Claude AI across a wide range of development and engineering tasks. Each skill encapsulates domain expertise, workflows, and best practices so that consistent, high-quality results can be reproduced on demand.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Skills Catalog](#skills-catalog)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`ai-lab` is a living library of **Claude AI skills**. A skill is a self-contained folder that contains a `SKILL.md` file (the core prompt/instructions) and optional supporting resources such as reference documents, scripts, and assets.

Skills follow a **three-level progressive loading** model:

| Level | What is loaded | When |
|-------|---------------|------|
| 1 | Skill name + description (~100 words) | Always |
| 2 | `SKILL.md` body (<500 lines ideal) | When the skill is triggered |
| 3 | Bundled resources (scripts, references, assets) | On demand |

---

## Repository Structure

```
ai-lab/
├── .agents/                   # Symbolic link to skills/ (alternative access path)
├── .cspell.json               # Spell-checker configuration
├── LICENSE                    # MIT License
├── README.md                  # This file
└── skills/                    # All skills live here
    ├── ai-prompt-engineering-safety-review/
    ├── clarify/
    ├── doc-coauthoring/
    ├── docker-expert/
    ├── git-commit/
    ├── github-pr-review/
    ├── kubernetes-architect/
    ├── kubernetes-deployment/
    └── skill-creator/
```

Each skill folder follows a common layout:

```
skill-name/
├── SKILL.md          # Required — core instructions and YAML frontmatter
└── (optional)
    ├── references/   # Supporting documentation loaded as needed
    ├── scripts/      # Executable helper scripts
    ├── agents/       # Sub-agent prompt files
    └── assets/       # Templates, icons, and other file assets
```

---

## Skills Catalog

### 🔍 ai-prompt-engineering-safety-review

Comprehensive AI prompt engineering **safety review and improvement** system.

- Analyzes prompts for safety, bias, security vulnerabilities, and effectiveness
- Scores prompts across multiple dimensions (1–5 scale): safety, bias mitigation, security & privacy, effectiveness, best practices compliance
- Detects advanced prompt patterns: zero-shot, few-shot, chain-of-thought, role-based, hybrid
- Produces a structured analysis report, an improved prompt version, testing recommendations, and educational insights

**Trigger phrases:** "review my prompt", "is this prompt safe", "improve this prompt"

---

### 🎯 clarify

Relentlessly interviews users about plans or designs until **shared understanding** is reached. Resolves every branch of the decision tree one question at a time.

- Walks down each decision branch sequentially (never all at once)
- Provides a recommended answer alongside each question
- Proactively explores the codebase when helpful

**Trigger phrases:** "clarify", "review my plan", "stress-test my design"

---

### 📝 doc-coauthoring

Structured three-stage workflow for **collaborative document creation**: proposals, technical specs, decision docs, RFCs, and more.

| Stage | Description |
|-------|-------------|
| 1 – Context Gathering | Collects meta-context, audience, and desired impact; encourages info-dumping |
| 2 – Refinement & Structure | Builds the document section-by-section with brainstorming, curation, and iterative drafting |
| 3 – Reader Testing | Tests the document from a fresh-context perspective to catch blind spots and ambiguities |

**Trigger phrases:** "write a doc", "draft a proposal", "create a spec", "write up", "PRD", "design doc"

---

### 🐳 docker-expert

Advanced Docker containerization expertise for **production-ready deployments**.

Core areas:
- **Dockerfile optimization** — multi-stage builds, layer caching, minimal base images (Alpine, distroless, scratch)
- **Container security hardening** — non-root users, secrets management, capability restrictions
- **Docker Compose orchestration** — health checks, service dependencies, environment management
- **Image size optimization** — distroless images, build artifact optimization
- **Development workflow integration** — hot reloading, debug configurations, remote dev containers
- **Performance & resource management** — CPU/memory limits, health checks, signal handling

**Trigger phrases:** "Dockerfile", "containerize", "docker compose", "optimize image"

---

### 📌 git-commit

Creates git commits following the **Conventional Commits** standard (`type(scope): subject`).

- Enforces present-tense imperative verbs
- Scope required in kebab-case
- Subject ≤ 50 characters, no trailing period
- Supports an additional `security` type for vulnerability fixes

**Example:**
```bash
git commit -m "feat(validation): add URLValidator with domain whitelist"
```

**Trigger phrases:** "commit", "create commit", "save work", "stage and commit"

---

### 🔄 github-pr-review

Handles GitHub Pull Request **review comment resolution** systematically.

Workflow:
1. Fetches inline comments and PR-level reviews (including CodeRabbit structured blocks)
2. Classifies comments by severity: CRITICAL → HIGH → MEDIUM → LOW
3. Processes each comment in severity order with user confirmation before applying fixes
4. Commits functional fixes individually and batches cosmetic fixes into a single `style:` commit
5. Replies to threads and marks them as resolved

**Trigger phrases:** "resolve PR comments", "handle review feedback", "fix review comments", "address PR review"

---

### ☸️ kubernetes-architect

Expert Kubernetes architect specializing in **cloud-native infrastructure**, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration.

Areas of expertise:
- Cluster design and multi-tenancy patterns
- Advanced GitOps with ArgoCD and Flux
- Service mesh architecture (Istio, Linkerd)
- Security policies (RBAC, NetworkPolicy, PodSecurity)
- Observability stacks (Prometheus, Grafana, tracing)

**Trigger phrases:** "kubernetes architecture", "k8s design", "gitops", "service mesh"

---

### 🚀 kubernetes-deployment

End-to-end **Kubernetes deployment workflow** covering container orchestration, Helm charts, service mesh, and production-ready configurations.

Seven-phase deployment pipeline:
1. Container preparation
2. Kubernetes manifests
3. Helm chart creation
4. Service mesh integration
5. Security hardening
6. Observability setup
7. CI/CD and GitOps deployment

**Trigger phrases:** "deploy to kubernetes", "helm chart", "k8s deployment", "production deployment"

---

### 🛠️ skill-creator

Meta-skill for **creating, improving, and benchmarking** other skills.

Capabilities:
- Guides skill creation from scratch via a structured user interview
- Runs evaluation loops and benchmarks with variance analysis
- Optimizes skill descriptions for better triggering accuracy
- Includes Python scripts (`run_loop.py`, `run_eval.py`, `generate_report.py`, etc.) and an interactive HTML eval viewer

**Trigger phrases:** "create a skill", "improve this skill", "benchmark skill", "optimize skill description"

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

Contributions are welcome! To add or improve a skill:

1. Fork the repository and create a feature branch.
2. Place your skill in a new folder under `skills/` following the standard layout.
3. Keep `SKILL.md` under 500 lines; move large content to `references/`.
4. Write a few test prompts and validate the skill using the `skill-creator` evaluation tooling.
5. Open a pull request with a clear description of what the skill does and when it should trigger.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright © 2026 Florian Woerner