"""Ansible skill tools.

Each tool is defined as an OpenAI-compatible function schema in
TOOL_DEFINITIONS and implemented by invoking Ansible CLI commands
(ansible-playbook, ansible, ansible-inventory) via subprocess.

Configuration:
    ANSIBLE_CONFIG      – Optional path to an ansible.cfg file.
    ANSIBLE_PRIVATE_KEY – Optional path to the SSH private key.
    ANSIBLE_USER        – Optional remote user override.
"""

import json
import os
import subprocess
from typing import Any

# ---------------------------------------------------------------------------
# OpenAI-compatible tool definitions
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "run_playbook",
            "description": "Run an Ansible playbook against an inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "playbook": {"type": "string", "description": "Absolute path to the playbook YAML file."},
                    "inventory": {"type": "string", "description": "Inventory file path or comma-separated host list."},
                    "extra_vars": {"type": "object", "description": "Extra variables passed as --extra-vars."},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Limit execution to specific tags.",
                    },
                    "skip_tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags to skip during execution.",
                    },
                    "limit": {"type": "string", "description": "Limit execution to a subset of hosts."},
                    "verbose": {"type": "boolean", "description": "Enable verbose output (default false)."},
                },
                "required": ["playbook"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_adhoc_command",
            "description": "Run an Ansible ad-hoc command on target hosts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hosts": {"type": "string", "description": "Host pattern (e.g. 'all', 'web')."},
                    "module": {"type": "string", "description": "Ansible module name (e.g. 'shell', 'ping')."},
                    "args": {"type": "string", "description": "Module arguments string."},
                    "inventory": {"type": "string", "description": "Inventory file path or comma-separated host list."},
                },
                "required": ["hosts", "module"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_inventory",
            "description": "List all hosts and groups in an Ansible inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "inventory": {"type": "string", "description": "Inventory file path or directory."},
                },
                "required": ["inventory"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_playbook_syntax",
            "description": "Check the syntax of an Ansible playbook without executing it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "playbook": {"type": "string", "description": "Absolute path to the playbook YAML file."},
                    "inventory": {"type": "string", "description": "Inventory file path (optional)."},
                },
                "required": ["playbook"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ping_hosts",
            "description": "Ping target hosts using the Ansible ping module to verify connectivity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hosts": {"type": "string", "description": "Host pattern (e.g. 'all', 'web', 'db')."},
                    "inventory": {"type": "string", "description": "Inventory file path or comma-separated host list."},
                },
                "required": ["hosts"],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run(cmd: list[str]) -> dict:
    """Execute a command and return stdout/stderr/returncode."""
    env = os.environ.copy()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "success": result.returncode == 0,
    }


def _inventory_args(inventory: str | None) -> list[str]:
    if not inventory:
        return []
    return ["-i", inventory]


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def _run_playbook(
    playbook: str,
    inventory: str | None = None,
    extra_vars: dict | None = None,
    tags: list[str] | None = None,
    skip_tags: list[str] | None = None,
    limit: str | None = None,
    verbose: bool = False,
) -> dict:
    cmd = ["ansible-playbook", playbook] + _inventory_args(inventory)

    if extra_vars:
        cmd += ["--extra-vars", json.dumps(extra_vars)]
    if tags:
        cmd += ["--tags", ",".join(tags)]
    if skip_tags:
        cmd += ["--skip-tags", ",".join(skip_tags)]
    if limit:
        cmd += ["--limit", limit]
    if verbose:
        cmd.append("-v")

    result = _run(cmd)
    if not result["success"]:
        raise RuntimeError(
            f"ansible-playbook failed (rc={result['returncode']}): {result['stderr']}"
        )
    return result


def _run_adhoc_command(
    hosts: str,
    module: str,
    args: str | None = None,
    inventory: str | None = None,
) -> dict:
    cmd = ["ansible", hosts, "-m", module] + _inventory_args(inventory)
    if args:
        cmd += ["-a", args]

    result = _run(cmd)
    if not result["success"]:
        raise RuntimeError(
            f"ansible ad-hoc failed (rc={result['returncode']}): {result['stderr']}"
        )
    return result


def _list_inventory(inventory: str) -> dict:
    cmd = ["ansible-inventory", "-i", inventory, "--list"]
    result = _run(cmd)
    if not result["success"]:
        raise RuntimeError(
            f"ansible-inventory failed (rc={result['returncode']}): {result['stderr']}"
        )
    try:
        data = json.loads(result["stdout"])
    except json.JSONDecodeError:
        data = result["stdout"]
    return {"inventory": data}


def _check_playbook_syntax(
    playbook: str,
    inventory: str | None = None,
) -> dict:
    inv = inventory or "localhost,"
    cmd = ["ansible-playbook", "--syntax-check", "-i", inv, playbook]
    result = _run(cmd)
    if not result["success"]:
        raise RuntimeError(
            f"Syntax check failed (rc={result['returncode']}): {result['stderr']}"
        )
    return {"status": "syntax_ok", "playbook": playbook, "output": result["stdout"]}


def _ping_hosts(
    hosts: str,
    inventory: str | None = None,
) -> dict:
    cmd = ["ansible", hosts, "-m", "ping"] + _inventory_args(inventory)
    result = _run(cmd)
    if not result["success"]:
        raise RuntimeError(
            f"Ping failed (rc={result['returncode']}): {result['stderr']}"
        )
    return result


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_HANDLERS = {
    "run_playbook": _run_playbook,
    "run_adhoc_command": _run_adhoc_command,
    "list_inventory": _list_inventory,
    "check_playbook_syntax": _check_playbook_syntax,
    "ping_hosts": _ping_hosts,
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
        raise ValueError(f"Unknown Ansible tool: '{tool_name}'")
    return handler(**kwargs)
