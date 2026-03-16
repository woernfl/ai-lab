"""ArgoCD skill tools.

Each tool is defined as an OpenAI-compatible function schema in
TOOL_DEFINITIONS and implemented using the ArgoCD REST API via requests.

Configuration:
    ARGOCD_SERVER   – ArgoCD server hostname or URL (e.g. "argocd.example.com").
    ARGOCD_TOKEN    – ArgoCD API token (create via Settings → Accounts → Generate Token).
    ARGOCD_INSECURE – Set to "true" to skip TLS verification (not recommended in production).
"""

import os
from typing import Any

import requests

# ---------------------------------------------------------------------------
# OpenAI-compatible tool definitions
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "list_apps",
            "description": "List all ArgoCD applications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Filter by ArgoCD project name (optional)."},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_app_status",
            "description": "Get the status and health of an ArgoCD application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "ArgoCD application name."},
                },
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sync_app",
            "description": "Trigger a sync for an ArgoCD application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "ArgoCD application name."},
                    "revision": {"type": "string", "description": "Target revision (branch, tag, or commit SHA)."},
                    "prune": {"type": "boolean", "description": "Prune resources no longer tracked (default false)."},
                    "dry_run": {"type": "boolean", "description": "Perform a dry-run sync (default false)."},
                },
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_app",
            "description": "Create a new ArgoCD application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "ArgoCD application name."},
                    "repo_url": {"type": "string", "description": "Source Git repository URL."},
                    "path": {"type": "string", "description": "Path within the repository containing Kubernetes manifests."},
                    "dest_namespace": {"type": "string", "description": "Target Kubernetes namespace."},
                    "dest_server": {"type": "string", "description": "Target Kubernetes API server URL."},
                    "project": {"type": "string", "description": "ArgoCD project name (default 'default')."},
                    "revision": {"type": "string", "description": "Target revision/branch (default 'HEAD')."},
                },
                "required": ["app_name", "repo_url", "path", "dest_namespace"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_app",
            "description": "Delete an ArgoCD application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "ArgoCD application name."},
                    "cascade": {"type": "boolean", "description": "Cascade-delete managed Kubernetes resources (default false)."},
                },
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rollback_app",
            "description": "Roll back an ArgoCD application to a previous deployed revision.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "ArgoCD application name."},
                    "revision_id": {"type": "integer", "description": "History revision ID to roll back to."},
                },
                "required": ["app_name", "revision_id"],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _base_url() -> str:
    server = os.environ.get("ARGOCD_SERVER", "")
    if not server:
        raise EnvironmentError("ARGOCD_SERVER environment variable is not set.")
    if not server.startswith("http"):
        server = f"https://{server}"
    return server.rstrip("/") + "/api/v1"


def _headers() -> dict[str, str]:
    token = os.environ.get("ARGOCD_TOKEN", "")
    if not token:
        raise EnvironmentError("ARGOCD_TOKEN environment variable is not set.")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _verify_tls() -> bool:
    return os.environ.get("ARGOCD_INSECURE", "false").lower() != "true"


def _raise_for_status(response: requests.Response) -> None:
    if not response.ok:
        raise RuntimeError(
            f"ArgoCD API error {response.status_code}: {response.text}"
        )


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def _list_apps(project: str | None = None) -> list[dict]:
    url = f"{_base_url()}/applications"
    params = {}
    if project:
        params["project"] = project
    resp = requests.get(url, headers=_headers(), params=params, verify=_verify_tls(), timeout=30)
    _raise_for_status(resp)
    items = resp.json().get("items") or []
    return [
        {
            "name": a["metadata"]["name"],
            "project": a["spec"].get("project", "default"),
            "sync_status": a["status"].get("sync", {}).get("status", "Unknown"),
            "health_status": a["status"].get("health", {}).get("status", "Unknown"),
            "repo_url": a["spec"].get("source", {}).get("repoURL", ""),
            "target_revision": a["spec"].get("source", {}).get("targetRevision", "HEAD"),
        }
        for a in items
    ]


def _get_app_status(app_name: str) -> dict:
    url = f"{_base_url()}/applications/{app_name}"
    resp = requests.get(url, headers=_headers(), verify=_verify_tls(), timeout=30)
    _raise_for_status(resp)
    a = resp.json()
    return {
        "name": a["metadata"]["name"],
        "project": a["spec"].get("project", "default"),
        "sync_status": a["status"].get("sync", {}).get("status", "Unknown"),
        "health_status": a["status"].get("health", {}).get("status", "Unknown"),
        "revision": a["status"].get("sync", {}).get("revision", ""),
        "repo_url": a["spec"].get("source", {}).get("repoURL", ""),
        "path": a["spec"].get("source", {}).get("path", ""),
        "dest_namespace": a["spec"].get("destination", {}).get("namespace", ""),
        "dest_server": a["spec"].get("destination", {}).get("server", ""),
    }


def _sync_app(
    app_name: str,
    revision: str | None = None,
    prune: bool = False,
    dry_run: bool = False,
) -> dict:
    url = f"{_base_url()}/applications/{app_name}/sync"
    payload: dict[str, Any] = {"prune": prune, "dryRun": dry_run}
    if revision:
        payload["revision"] = revision
    resp = requests.post(url, headers=_headers(), json=payload, verify=_verify_tls(), timeout=60)
    _raise_for_status(resp)
    r = resp.json()
    return {
        "status": "sync_initiated",
        "app_name": app_name,
        "sync_status": r.get("status", {}).get("sync", {}).get("status", "Unknown"),
        "health_status": r.get("status", {}).get("health", {}).get("status", "Unknown"),
    }


def _create_app(
    app_name: str,
    repo_url: str,
    path: str,
    dest_namespace: str,
    dest_server: str = "https://kubernetes.default.svc",
    project: str = "default",
    revision: str = "HEAD",
) -> dict:
    url = f"{_base_url()}/applications"
    payload = {
        "metadata": {"name": app_name},
        "spec": {
            "project": project,
            "source": {
                "repoURL": repo_url,
                "path": path,
                "targetRevision": revision,
            },
            "destination": {
                "server": dest_server,
                "namespace": dest_namespace,
            },
            "syncPolicy": {"automated": None},
        },
    }
    resp = requests.post(url, headers=_headers(), json=payload, verify=_verify_tls(), timeout=30)
    _raise_for_status(resp)
    return {"status": "created", "app_name": app_name}


def _delete_app(app_name: str, cascade: bool = False) -> dict:
    url = f"{_base_url()}/applications/{app_name}"
    params = {"cascade": str(cascade).lower()}
    resp = requests.delete(url, headers=_headers(), params=params, verify=_verify_tls(), timeout=30)
    _raise_for_status(resp)
    return {"status": "deleted", "app_name": app_name}


def _rollback_app(app_name: str, revision_id: int) -> dict:
    url = f"{_base_url()}/applications/{app_name}/rollback"
    payload = {"id": revision_id}
    resp = requests.post(url, headers=_headers(), json=payload, verify=_verify_tls(), timeout=60)
    _raise_for_status(resp)
    return {"status": "rollback_initiated", "app_name": app_name, "revision_id": revision_id}


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_HANDLERS = {
    "list_apps": _list_apps,
    "get_app_status": _get_app_status,
    "sync_app": _sync_app,
    "create_app": _create_app,
    "delete_app": _delete_app,
    "rollback_app": _rollback_app,
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
        raise ValueError(f"Unknown ArgoCD tool: '{tool_name}'")
    return handler(**kwargs)
