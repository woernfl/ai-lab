"""GitHub Actions skill tools.

Each tool is defined as an OpenAI-compatible function schema in
TOOL_DEFINITIONS and implemented in the corresponding ``_<name>`` function.
The ``execute`` dispatcher maps tool names to their implementations.

Configuration:
    GITHUB_TOKEN environment variable must be set with a Personal Access Token
    (or a GitHub App installation token) that has *workflow* scope for write
    operations and *repo* scope for read operations.
"""

import os
from typing import Any

import requests

_BASE = "https://api.github.com"

# ---------------------------------------------------------------------------
# OpenAI-compatible tool definitions
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "list_workflows",
            "description": "List all workflows defined in a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner (user or organisation)."},
                    "repo": {"type": "string", "description": "Repository name."},
                },
                "required": ["owner", "repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_workflow",
            "description": "Manually trigger a workflow run (workflow_dispatch event).",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner."},
                    "repo": {"type": "string", "description": "Repository name."},
                    "workflow_id": {"type": "string", "description": "Workflow file name (e.g. ci.yml) or numeric ID."},
                    "ref": {"type": "string", "description": "Branch or tag name to run the workflow on."},
                    "inputs": {"type": "object", "description": "Key/value pairs of workflow_dispatch inputs."},
                },
                "required": ["owner", "repo", "workflow_id", "ref"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_workflow_runs",
            "description": "List recent runs for a specific workflow.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner."},
                    "repo": {"type": "string", "description": "Repository name."},
                    "workflow_id": {"type": "string", "description": "Workflow file name or numeric workflow ID."},
                    "branch": {"type": "string", "description": "Filter by branch name (optional)."},
                    "status": {"type": "string", "description": "Filter by status (optional)."},
                    "per_page": {"type": "integer", "description": "Number of results (default 10, max 100)."},
                },
                "required": ["owner", "repo", "workflow_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_workflow_run",
            "description": "Get details and status of a specific workflow run.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner."},
                    "repo": {"type": "string", "description": "Repository name."},
                    "run_id": {"type": "integer", "description": "Numeric workflow run ID."},
                },
                "required": ["owner", "repo", "run_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_workflow_run",
            "description": "Cancel a workflow run that is queued or in progress.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner."},
                    "repo": {"type": "string", "description": "Repository name."},
                    "run_id": {"type": "integer", "description": "Numeric workflow run ID."},
                },
                "required": ["owner", "repo", "run_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rerun_workflow",
            "description": "Re-run all jobs in a failed or cancelled workflow run.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner."},
                    "repo": {"type": "string", "description": "Repository name."},
                    "run_id": {"type": "integer", "description": "Numeric workflow run ID."},
                },
                "required": ["owner", "repo", "run_id"],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN environment variable is not set.")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _raise_for_status(response: requests.Response) -> None:
    if not response.ok:
        raise RuntimeError(
            f"GitHub API error {response.status_code}: {response.text}"
        )


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def _list_workflows(owner: str, repo: str) -> list[dict]:
    url = f"{_BASE}/repos/{owner}/{repo}/actions/workflows"
    resp = requests.get(url, headers=_headers(), timeout=30)
    _raise_for_status(resp)
    data = resp.json()
    return [
        {"id": w["id"], "name": w["name"], "path": w["path"], "state": w["state"]}
        for w in data.get("workflows", [])
    ]


def _trigger_workflow(
    owner: str,
    repo: str,
    workflow_id: str,
    ref: str,
    inputs: dict | None = None,
) -> dict:
    url = f"{_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    payload: dict[str, Any] = {"ref": ref}
    if inputs:
        payload["inputs"] = inputs
    resp = requests.post(url, headers=_headers(), json=payload, timeout=30)
    _raise_for_status(resp)
    return {"status": "triggered", "workflow_id": workflow_id, "ref": ref}


def _list_workflow_runs(
    owner: str,
    repo: str,
    workflow_id: str,
    branch: str | None = None,
    status: str | None = None,
    per_page: int = 10,
) -> list[dict]:
    url = f"{_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
    params: dict[str, Any] = {"per_page": min(per_page, 100)}
    if branch:
        params["branch"] = branch
    if status:
        params["status"] = status
    resp = requests.get(url, headers=_headers(), params=params, timeout=30)
    _raise_for_status(resp)
    data = resp.json()
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "status": r["status"],
            "conclusion": r["conclusion"],
            "branch": r["head_branch"],
            "created_at": r["created_at"],
            "html_url": r["html_url"],
        }
        for r in data.get("workflow_runs", [])
    ]


def _get_workflow_run(owner: str, repo: str, run_id: int) -> dict:
    url = f"{_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}"
    resp = requests.get(url, headers=_headers(), timeout=30)
    _raise_for_status(resp)
    r = resp.json()
    return {
        "id": r["id"],
        "name": r["name"],
        "status": r["status"],
        "conclusion": r["conclusion"],
        "branch": r["head_branch"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
        "html_url": r["html_url"],
    }


def _cancel_workflow_run(owner: str, repo: str, run_id: int) -> dict:
    url = f"{_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}/cancel"
    resp = requests.post(url, headers=_headers(), timeout=30)
    _raise_for_status(resp)
    return {"status": "cancel_requested", "run_id": run_id}


def _rerun_workflow(owner: str, repo: str, run_id: int) -> dict:
    url = f"{_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}/rerun"
    resp = requests.post(url, headers=_headers(), timeout=30)
    _raise_for_status(resp)
    return {"status": "rerun_requested", "run_id": run_id}


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_HANDLERS = {
    "list_workflows": _list_workflows,
    "trigger_workflow": _trigger_workflow,
    "list_workflow_runs": _list_workflow_runs,
    "get_workflow_run": _get_workflow_run,
    "cancel_workflow_run": _cancel_workflow_run,
    "rerun_workflow": _rerun_workflow,
}


def execute(tool_name: str, **kwargs: Any) -> Any:
    """Dispatch a tool call to its implementation.

    Args:
        tool_name: One of the tool names declared in TOOL_DEFINITIONS.
        **kwargs: Tool-specific keyword arguments.

    Returns:
        The result returned by the tool implementation.

    Raises:
        ValueError: If ``tool_name`` is not recognised.
    """
    handler = _HANDLERS.get(tool_name)
    if handler is None:
        raise ValueError(f"Unknown GitHub Actions tool: '{tool_name}'")
    return handler(**kwargs)
