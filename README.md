# ai-lab

A collection of **Agent Skills** and a **DevOps Agent** for automating common
infrastructure tasks with LLMs.

---

## Overview

| Skill | Description |
|---|---|
| **GitHub Actions** | List, trigger, monitor, cancel and rerun workflow runs via the GitHub REST API |
| **Kubernetes** | Query deployment status, scale replicas, apply manifests, fetch pod logs, rolling restarts |
| **ArgoCD** | List, sync, create, delete and rollback GitOps applications via the ArgoCD REST API |
| **Ansible** | Run playbooks, execute ad-hoc commands, list inventory, check playbook syntax, ping hosts |

Each skill exposes **OpenAI-compatible function definitions** so it can be
used with any LLM that supports function/tool calling (GPT-4o, GPT-4,
Claude Sonnet, etc.).

The **DevOps Agent** (`agents/devops_agent.py`) wires all skills together into
a single conversational agent: it accepts a natural-language request, selects
the right tools, executes them, and returns a concise answer.

---

## Repository Structure

```
ai-lab/
├── requirements.txt
├── agents/
│   ├── devops_agent.yaml   ← agent configuration
│   └── devops_agent.py     ← agent implementation
└── skills/
    ├── github_actions/
    │   ├── skill.yaml       ← tool definitions (human-readable)
    │   └── tools.py         ← tool implementations + TOOL_DEFINITIONS
    ├── kubernetes/
    │   ├── skill.yaml
    │   └── tools.py
    ├── argocd/
    │   ├── skill.yaml
    │   └── tools.py
    └── ansible/
        ├── skill.yaml
        └── tools.py
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

| Variable | Skill | Required |
|---|---|---|
| `OPENAI_API_KEY` | Agent | Yes |
| `OPENAI_MODEL` | Agent | No (default: `gpt-4o`) |
| `GITHUB_TOKEN` | GitHub Actions | Yes |
| `ARGOCD_SERVER` | ArgoCD | Yes |
| `ARGOCD_TOKEN` | ArgoCD | Yes |
| `ARGOCD_INSECURE` | ArgoCD | No (set `true` to skip TLS) |
| `KUBECONFIG` | Kubernetes | No (uses default kubeconfig) |
| `ANSIBLE_CONFIG` | Ansible | No |

### 3. Run the agent

```python
import os
from agents.devops_agent import DevOpsAgent

os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["GITHUB_TOKEN"] = "ghp_..."

agent = DevOpsAgent()

# GitHub Actions
print(agent.run("List all workflows in the repo myorg/myapp"))
print(agent.run("Trigger the CI workflow on branch main in myorg/myapp"))

# Kubernetes
print(agent.run("Show me the status of the api-server deployment in namespace production"))
print(agent.run("Scale the worker deployment to 5 replicas in the staging namespace"))

# ArgoCD
print(agent.run("Sync the production ArgoCD application"))
print(agent.run("List all ArgoCD applications in the platform project"))

# Ansible
print(agent.run("Run the site.yml playbook against the web inventory"))
print(agent.run("Ping all hosts in the production inventory"))
```

---

## Using Skills Directly

Skills can also be used independently without the agent:

```python
from skills.github_actions import execute as gh_execute
from skills.kubernetes import execute as k8s_execute
from skills.argocd import execute as argocd_execute
from skills.ansible import execute as ansible_execute

# List GitHub Actions workflows
workflows = gh_execute("list_workflows", owner="myorg", repo="myapp")

# Get Kubernetes deployment status
status = k8s_execute("get_deployment_status", deployment="api-server", namespace="production")

# Sync an ArgoCD app
result = argocd_execute("sync_app", app_name="production")

# Run an Ansible playbook
result = ansible_execute("run_playbook", playbook="/playbooks/site.yml", inventory="/inventory/prod")
```

---

## Skills Reference

### GitHub Actions

| Tool | Description |
|---|---|
| `list_workflows` | List all workflows in a repository |
| `trigger_workflow` | Trigger a workflow via `workflow_dispatch` |
| `list_workflow_runs` | List recent runs for a workflow |
| `get_workflow_run` | Get details of a specific run |
| `cancel_workflow_run` | Cancel a queued or in-progress run |
| `rerun_workflow` | Re-run all jobs in a failed/cancelled run |

### Kubernetes

| Tool | Description |
|---|---|
| `get_deployment_status` | Get deployment replicas and conditions |
| `scale_deployment` | Scale a deployment to N replicas |
| `apply_manifest` | Apply a YAML manifest (inline or file path) |
| `delete_resource` | Delete a Kubernetes resource |
| `get_pod_logs` | Fetch logs from a pod |
| `list_pods` | List pods in a namespace |
| `rollout_restart` | Rolling restart of a deployment |

### ArgoCD

| Tool | Description |
|---|---|
| `list_apps` | List ArgoCD applications |
| `get_app_status` | Get sync/health status of an application |
| `sync_app` | Trigger application sync |
| `create_app` | Create a new application |
| `delete_app` | Delete an application |
| `rollback_app` | Roll back to a previous revision |

### Ansible

| Tool | Description |
|---|---|
| `run_playbook` | Run a playbook with optional tags, vars, limits |
| `run_adhoc_command` | Execute an ad-hoc module command |
| `list_inventory` | List hosts and groups in an inventory |
| `check_playbook_syntax` | Validate playbook syntax |
| `ping_hosts` | Verify host connectivity with the ping module |

---

## License

[MIT](LICENSE)
