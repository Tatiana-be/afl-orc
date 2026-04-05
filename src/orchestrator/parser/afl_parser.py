"""AFL Config parser."""

import json
from typing import Any

import yaml

from src.orchestrator.parser.schema import AFLConfig


class AFLParser:
    """Parser for AFL configuration files."""

    def __init__(self) -> None:
        self._raw_content: str = ""

    def parse_yaml(self, content: str) -> AFLConfig:
        """Parse YAML content into AFLConfig.

        Supports YAML anchors (&), aliases (*), and merge keys (<<:).
        Uses FullLoader for safe merging support.
        """
        self._raw_content = content
        data = yaml.load(content, Loader=yaml.FullLoader)  # nosec B506
        return AFLConfig(**data)

    def parse_json(self, content: str) -> AFLConfig:
        """Parse JSON content into AFLConfig."""
        self._raw_content = content
        data = json.loads(content)
        return AFLConfig(**data)

    def parse(self, content: str, format: str = "yaml") -> AFLConfig:
        """Parse configuration content."""
        if format == "yaml":
            return self.parse_yaml(content)
        elif format == "json":
            return self.parse_json(content)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def validate(self, config: AFLConfig) -> list[dict[str, Any]]:
        """Validate AFL configuration.

        Checks:
        - Agent references in workflow steps
        - Artifact references in workflow steps
        - Guardrail references in agents
        - Dependency references in workflow steps
        - Circular dependencies in workflow
        """
        errors: list[dict[str, Any]] = []

        # Build lookup sets
        agent_ids = {agent.id for agent in config.agents}
        artifact_ids = {artifact.id for artifact in config.artifacts}
        guardrail_ids = {g.id for g in config.guardrails}
        step_ids = {step.step for step in config.workflow}

        # Validate agent references in workflow steps
        errors.extend(self._validate_agent_references(config, agent_ids))

        # Validate artifact references in workflow steps
        errors.extend(self._validate_artifact_references(config, artifact_ids))

        # Validate guardrail references in agents
        errors.extend(self._validate_guardrail_references(config, guardrail_ids))

        # Validate dependency references
        errors.extend(self._validate_dependency_references(config, step_ids))

        # Check for circular dependencies
        errors.extend(self._detect_circular_dependencies(config))

        # Enrich errors with line/column info
        self._enrich_with_line_column(errors)

        return errors

    def _validate_agent_references(
        self, config: AFLConfig, agent_ids: set[str]
    ) -> list[dict[str, Any]]:
        """Validate that workflow steps reference valid agents."""
        errors = []
        for step in config.workflow:
            if step.agent not in agent_ids:
                errors.append(
                    {
                        "type": "invalid_reference",
                        "field": "agent",
                        "step": step.step,
                        "value": step.agent,
                        "message": (
                            f"Step '{step.step}' references " f"unknown agent '{step.agent}'"
                        ),
                    }
                )
        return errors

    def _validate_artifact_references(
        self, config: AFLConfig, artifact_ids: set[str]
    ) -> list[dict[str, Any]]:
        """Validate that workflow steps reference valid artifacts."""
        errors = []
        for step in config.workflow:
            if step.artifact is not None and step.artifact not in artifact_ids:
                errors.append(
                    {
                        "type": "invalid_reference",
                        "field": "artifact",
                        "step": step.step,
                        "value": step.artifact,
                        "message": (
                            f"Step '{step.step}' references " f"unknown artifact '{step.artifact}'"
                        ),
                    }
                )
        return errors

    def _validate_guardrail_references(
        self, config: AFLConfig, guardrail_ids: set[str]
    ) -> list[dict[str, Any]]:
        """Validate that agents reference valid guardrails."""
        errors = []
        for agent in config.agents:
            for guardrail_id in agent.guardrails:
                if guardrail_id not in guardrail_ids:
                    errors.append(
                        {
                            "type": "invalid_reference",
                            "field": "guardrail",
                            "agent": agent.id,
                            "value": guardrail_id,
                            "message": (
                                f"Agent '{agent.id}' references "
                                f"unknown guardrail '{guardrail_id}'"
                            ),
                        }
                    )
        return errors

    def _validate_dependency_references(
        self, config: AFLConfig, step_ids: set[str]
    ) -> list[dict[str, Any]]:
        """Validate that workflow steps reference valid dependencies."""
        errors = []
        for step in config.workflow:
            for dep in step.depends_on:
                if dep not in step_ids:
                    errors.append(
                        {
                            "type": "invalid_reference",
                            "field": "depends_on",
                            "step": step.step,
                            "value": dep,
                            "message": (f"Step '{step.step}' depends on " f"unknown step '{dep}'"),
                        }
                    )
        return errors

    def _detect_circular_dependencies(self, config: AFLConfig) -> list[dict[str, Any]]:
        """Detect circular dependencies in workflow using DFS."""
        errors = []

        # Build adjacency list
        graph: dict[str, list[str]] = {}
        for step in config.workflow:
            graph[step.step] = list(step.depends_on)

        # DFS cycle detection
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = dict.fromkeys(graph, WHITE)
        cycles: list[list[str]] = []

        def dfs(node: str, path: list[str]) -> None:
            color[node] = GRAY
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    # Reference to non-existent step (caught elsewhere)
                    continue
                if color[neighbor] == GRAY:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
                elif color[neighbor] == WHITE:
                    dfs(neighbor, path)

            path.pop()
            color[node] = BLACK

        for step_id in graph:
            if color[step_id] == WHITE:
                dfs(step_id, [])

        # Report cycles
        for cycle in cycles:
            cycle_str = " -> ".join(cycle)
            errors.append(
                {
                    "type": "circular_dependency",
                    "field": "depends_on",
                    "cycle": cycle,
                    "message": (f"Circular dependency detected: {cycle_str}"),
                }
            )

        return errors

    def _enrich_with_line_column(self, errors: list[dict[str, Any]]) -> None:
        """Add line and column information to validation errors.

        Searches the raw content for the referenced value and adds
        ``line`` and ``column`` fields to each error dict.
        """
        lines = self._raw_content.splitlines() if self._raw_content else []

        for error in errors:
            value = error.get("value", "")
            if not value or not lines:
                error["line"] = None
                error["column"] = None
                continue

            # Find the value in raw content
            for line_num, line in enumerate(lines, start=1):
                col_idx = line.find(value)
                if col_idx >= 0:
                    error["line"] = line_num
                    error["column"] = col_idx + 1  # 1-based
                    break
            else:
                error["line"] = None
                error["column"] = None
