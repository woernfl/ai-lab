"""Kubernetes skill tools.

Each tool is defined as an OpenAI-compatible function schema in
TOOL_DEFINITIONS and implemented using ``kubectl`` via subprocess.

Configuration:
    KUBECONFIG environment variable (optional) – path to the kubeconfig file.
    The active kubectl context is used unless ``context`` is passed explicitly.
"""

import json
import os
import subprocess
import tempfile
from typing import Any

# ---------------------------------------------------------------------------
# OpenAI-compatible tool definitions
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "get_deployment_status",
            "description": "Get the status of a Kubernetes deployment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "deployment": {"type": "string", "description": "Deployment name."},
                    "namespace": {"type": "string", "description": "Kubernetes namespace (default 'default')."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": ["deployment"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scale_deployment",
            "description": "Scale a Kubernetes deployment to the desired number of replicas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "deployment": {"type": "string", "description": "Deployment name."},
                    "replicas": {"type": "integer", "description": "Desired replica count."},
                    "namespace": {"type": "string", "description": "Kubernetes namespace (default 'default')."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": ["deployment", "replicas"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_manifest",
            "description": "Apply a Kubernetes manifest from a YAML string or file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "manifest": {"type": "string", "description": "Inline YAML content or absolute path to manifest file."},
                    "namespace": {"type": "string", "description": "Namespace override (optional)."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": ["manifest"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_resource",
            "description": "Delete a Kubernetes resource by kind and name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "description": "Resource kind (e.g. Deployment, Service)."},
                    "name": {"type": "string", "description": "Resource name."},
                    "namespace": {"type": "string", "description": "Kubernetes namespace (default 'default')."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": ["kind", "name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pod_logs",
            "description": "Retrieve logs from a specific pod.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pod": {"type": "string", "description": "Pod name."},
                    "namespace": {"type": "string", "description": "Kubernetes namespace (default 'default')."},
                    "container": {"type": "string", "description": "Container name (for multi-container pods)."},
                    "tail": {"type": "integer", "description": "Number of most recent log lines (default 100)."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": ["pod"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_pods",
            "description": "List pods in a namespace with their status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace (default 'default')."},
                    "label_selector": {"type": "string", "description": "Label selector (e.g. 'app=my-app')."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rollout_restart",
            "description": "Perform a rolling restart of a Kubernetes deployment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "deployment": {"type": "string", "description": "Deployment name."},
                    "namespace": {"type": "string", "description": "Kubernetes namespace (default 'default')."},
                    "context": {"type": "string", "description": "kubectl context to use."},
                },
                "required": ["deployment"],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _kubectl(args: list[str], input_data: str | None = None) -> str:
    """Run a kubectl command and return stdout as a string."""
    env = os.environ.copy()
    result = subprocess.run(
        ["kubectl", *args],
        input=input_data,
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"kubectl error: {result.stderr.strip()}")
    return result.stdout.strip()


def _ns_args(namespace: str | None) -> list[str]:
    return ["--namespace", namespace] if namespace else ["--namespace", "default"]


def _ctx_args(context: str | None) -> list[str]:
    return ["--context", context] if context else []


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def _get_deployment_status(
    deployment: str,
    namespace: str | None = None,
    context: str | None = None,
) -> dict:
    args = (
        ["get", "deployment", deployment, "-o", "json"]
        + _ns_args(namespace)
        + _ctx_args(context)
    )
    raw = _kubectl(args)
    d = json.loads(raw)
    status = d.get("status", {})
    return {
        "name": d["metadata"]["name"],
        "namespace": d["metadata"]["namespace"],
        "replicas": status.get("replicas", 0),
        "ready_replicas": status.get("readyReplicas", 0),
        "available_replicas": status.get("availableReplicas", 0),
        "updated_replicas": status.get("updatedReplicas", 0),
        "conditions": [
            {"type": c["type"], "status": c["status"], "reason": c.get("reason", "")}
            for c in status.get("conditions", [])
        ],
    }


def _scale_deployment(
    deployment: str,
    replicas: int,
    namespace: str | None = None,
    context: str | None = None,
) -> dict:
    args = (
        ["scale", "deployment", deployment, f"--replicas={replicas}"]
        + _ns_args(namespace)
        + _ctx_args(context)
    )
    output = _kubectl(args)
    return {"status": "scaled", "deployment": deployment, "replicas": replicas, "output": output}


def _apply_manifest(
    manifest: str,
    namespace: str | None = None,
    context: str | None = None,
) -> dict:
    ns_args = _ns_args(namespace) if namespace else []
    ctx_args = _ctx_args(context)

    if os.path.isabs(manifest) and os.path.isfile(manifest):
        args = ["apply", "-f", manifest] + ns_args + ctx_args
        output = _kubectl(args)
    else:
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as tmp:
                tmp.write(manifest)
                tmp_path = tmp.name
            args = ["apply", "-f", tmp_path] + ns_args + ctx_args
            output = _kubectl(args)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    return {"status": "applied", "output": output}


def _delete_resource(
    kind: str,
    name: str,
    namespace: str | None = None,
    context: str | None = None,
) -> dict:
    args = (
        ["delete", kind, name]
        + _ns_args(namespace)
        + _ctx_args(context)
    )
    output = _kubectl(args)
    return {"status": "deleted", "kind": kind, "name": name, "output": output}


def _get_pod_logs(
    pod: str,
    namespace: str | None = None,
    container: str | None = None,
    tail: int = 100,
    context: str | None = None,
) -> dict:
    args = (
        ["logs", pod, f"--tail={tail}"]
        + _ns_args(namespace)
        + _ctx_args(context)
    )
    if container:
        args += ["-c", container]
    logs = _kubectl(args)
    return {"pod": pod, "logs": logs}


def _list_pods(
    namespace: str | None = None,
    label_selector: str | None = None,
    context: str | None = None,
) -> list[dict]:
    args = (
        ["get", "pods", "-o", "json"]
        + _ns_args(namespace)
        + _ctx_args(context)
    )
    if label_selector:
        args += ["-l", label_selector]
    raw = _kubectl(args)
    data = json.loads(raw)
    pods = []
    for p in data.get("items", []):
        status = p.get("status", {})
        pods.append(
            {
                "name": p["metadata"]["name"],
                "namespace": p["metadata"]["namespace"],
                "phase": status.get("phase", "Unknown"),
                "ready": sum(
                    1
                    for c in status.get("containerStatuses", [])
                    if c.get("ready")
                ),
                "restarts": sum(
                    c.get("restartCount", 0)
                    for c in status.get("containerStatuses", [])
                ),
                "node": p["spec"].get("nodeName", ""),
            }
        )
    return pods


def _rollout_restart(
    deployment: str,
    namespace: str | None = None,
    context: str | None = None,
) -> dict:
    args = (
        ["rollout", "restart", f"deployment/{deployment}"]
        + _ns_args(namespace)
        + _ctx_args(context)
    )
    output = _kubectl(args)
    return {"status": "restarted", "deployment": deployment, "output": output}


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_HANDLERS = {
    "get_deployment_status": _get_deployment_status,
    "scale_deployment": _scale_deployment,
    "apply_manifest": _apply_manifest,
    "delete_resource": _delete_resource,
    "get_pod_logs": _get_pod_logs,
    "list_pods": _list_pods,
    "rollout_restart": _rollout_restart,
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
        raise ValueError(f"Unknown Kubernetes tool: '{tool_name}'")
    return handler(**kwargs)
