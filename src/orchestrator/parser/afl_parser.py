"""AFL Config parser."""

import json
from typing import Any

import yaml

from src.orchestrator.parser.schema import AFLConfig


class AFLParser:
    """Parser for AFL configuration files."""

    def parse_yaml(self, content: str) -> AFLConfig:
        """Parse YAML content into AFLConfig."""
        data = yaml.safe_load(content)
        return AFLConfig(**data)

    def parse_json(self, content: str) -> AFLConfig:
        """Parse JSON content into AFLConfig."""
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
        """Validate AFL configuration."""
        errors = []

        # Check workflow steps reference valid agents
        agent_ids = {agent.id for agent in config.agents}
        for step in config.workflow:
            if step.agent not in agent_ids:
                errors.append(
                    {
                        "type": "invalid_reference",
                        "message": f"Step '{step.step}' references unknown agent '{step.agent}'",
                    }
                )

        return errors
