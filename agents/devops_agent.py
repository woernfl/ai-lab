"""DevOps Agent.

An OpenAI function-calling agent that orchestrates GitHub Actions,
Kubernetes, ArgoCD, and Ansible skills to fulfil natural language requests.

Usage::

    import os
    from agents.devops_agent import DevOpsAgent

    os.environ["OPENAI_API_KEY"] = "sk-..."
    os.environ["GITHUB_TOKEN"] = "ghp_..."
    # Set additional environment variables as needed for each skill.

    agent = DevOpsAgent()
    response = agent.run("Trigger the CI workflow on main for repo myorg/myapp")
    print(response)

Environment variables:
    OPENAI_API_KEY  – Required. OpenAI API key.
    OPENAI_MODEL    – Optional. Model override (default: gpt-4o).

    See each skill's tools.py for skill-specific environment variables.
"""

from __future__ import annotations

import importlib
import json
import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

_CONFIG_PATH = Path(__file__).parent / "devops_agent.yaml"


class DevOpsAgent:
    """Agent that routes natural-language requests to DevOps skill tools.

    Args:
        config_path: Path to the agent YAML configuration file.
            Defaults to ``agents/devops_agent.yaml``.
        model: LLM model override. Takes precedence over the config file.
        max_iterations: Maximum number of LLM ↔ tool call iterations.
            Takes precedence over the config file.
    """

    def __init__(
        self,
        config_path: str | Path | None = None,
        model: str | None = None,
        max_iterations: int | None = None,
    ) -> None:
        cfg_path = Path(config_path) if config_path else _CONFIG_PATH
        with cfg_path.open() as fh:
            self._cfg = yaml.safe_load(fh)

        self._model: str = model or os.environ.get("OPENAI_MODEL") or self._cfg.get("model", "gpt-4o")
        self._max_iter: int = max_iterations or self._cfg.get("max_iterations", 10)
        self._system_prompt: str = self._cfg.get("system_prompt", "You are a helpful DevOps assistant.")

        self._tools, self._skill_map = self._load_skills()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, user_message: str) -> str:
        """Process a natural-language DevOps request.

        Args:
            user_message: The user's request in plain English.

        Returns:
            The agent's final text response.
        """
        try:
            from openai import OpenAI  # lazy import – only needed at runtime
        except ImportError as exc:
            raise ImportError(
                "openai package is required. Install it with: pip install openai"
            ) from exc

        client = OpenAI()
        messages: list[dict] = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_message},
        ]

        for iteration in range(self._max_iter):
            logger.debug("Iteration %d/%d", iteration + 1, self._max_iter)
            response = client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=self._tools,
                tool_choice="auto",
            )
            choice = response.choices[0]
            messages.append(choice.message.model_dump())

            if choice.finish_reason == "stop":
                return choice.message.content or ""

            if choice.finish_reason == "tool_calls":
                for tool_call in choice.message.tool_calls or []:
                    result = self._dispatch(tool_call)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        }
                    )

        return "Maximum iterations reached without a final response."

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _load_skills(self) -> tuple[list[dict], dict[str, Any]]:
        """Import skill modules and collect their tool definitions.

        Returns:
            A tuple of (all_tool_definitions, tool_name_to_module_mapping).
        """
        all_tools: list[dict] = []
        skill_map: dict[str, Any] = {}

        for skill_cfg in self._cfg.get("skills", []):
            module_path: str = skill_cfg["module"]
            try:
                module = importlib.import_module(module_path)
            except ImportError as exc:
                logger.warning("Could not import skill module '%s': %s", module_path, exc)
                continue

            for tool_def in getattr(module, "TOOL_DEFINITIONS", []):
                all_tools.append(tool_def)
                tool_name = tool_def["function"]["name"]
                skill_map[tool_name] = module

        return all_tools, skill_map

    def _dispatch(self, tool_call: Any) -> Any:
        """Execute a tool call and return the result.

        Args:
            tool_call: An OpenAI ``ChatCompletionMessageToolCall`` object.

        Returns:
            The result from the skill's ``execute`` function, or an error dict.
        """
        tool_name: str = tool_call.function.name
        try:
            kwargs: dict = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as exc:
            return {"error": f"Failed to parse tool arguments: {exc}"}

        module = self._skill_map.get(tool_name)
        if module is None:
            return {"error": f"No handler found for tool '{tool_name}'"}

        try:
            return module.execute(tool_name, **kwargs)
        except Exception as exc:  # noqa: BLE001
            logger.error("Tool '%s' raised an exception: %s", tool_name, exc)
            return {"error": str(exc)}
