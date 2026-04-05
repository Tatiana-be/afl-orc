"""Unit tests for AFL Parser."""

import pytest

from src.orchestrator.parser.afl_parser import AFLParser
from src.orchestrator.parser.schema import AFLConfig


@pytest.fixture
def parser():
    """Create parser instance."""
    return AFLParser()


@pytest.fixture
def valid_yaml_config():
    """Valid YAML configuration."""
    return """
version: "1.0"
project: "Test Project"
budget:
  total_tokens: 100000
  warning_threshold: 0.8
agents:
  - id: "test_agent"
    type: "llm"
    model: "gpt-4"
workflow:
  - step: "test_step"
    agent: "test_agent"
"""


def test_parse_yaml(parser, valid_yaml_config):
    """Test YAML parsing."""
    config = parser.parse_yaml(valid_yaml_config)
    assert isinstance(config, AFLConfig)
    assert config.version == "1.0"
    assert config.project == "Test Project"


def test_parse_json(parser):
    """Test JSON parsing."""
    json_config = """
{
    "version": "1.0",
    "project": "Test Project",
    "agents": [],
    "workflow": []
}
"""
    config = parser.parse_json(json_config)
    assert isinstance(config, AFLConfig)
    assert config.version == "1.0"


def test_validate_valid_config(parser, valid_yaml_config):
    """Test validation of valid configuration."""
    config = parser.parse_yaml(valid_yaml_config)
    errors = parser.validate(config)
    assert len(errors) == 0


def test_validate_invalid_agent_reference(parser):
    """Test validation with invalid agent reference."""
    yaml_config = """
version: "1.0"
project: "Test"
agents:
  - id: "agent_a"
    type: "llm"
workflow:
  - step: "step1"
    agent: "nonexistent_agent"
"""
    config = parser.parse_yaml(yaml_config)
    errors = parser.validate(config)
    assert len(errors) == 1
    assert "nonexistent_agent" in errors[0]["message"]


# ============================================
# YAML Anchors & Aliases Tests (PARSER-003)
# ============================================


class TestYAMLAnchorsAndAliases:
    """Tests for YAML anchors (&), aliases (*), and merge keys (<<:)."""

    def test_anchor_and_alias_basic(self, parser):
        """Test basic YAML anchor and alias resolution."""
        yaml_content = """
version: "1.0"
project: "Anchor Test"

agents:
  - id: agent_a
    type: &agent_type "llm"
    model: "gpt-4"
  - id: agent_b
    type: *agent_type
    model: "claude-3"

workflow:
  - step: step_a
    agent: agent_a
  - step: step_b
    agent: agent_b
"""
        config = parser.parse_yaml(yaml_content)
        assert len(config.agents) == 2
        assert config.agents[0].type == "llm"
        assert config.agents[1].type == "llm"

    def test_anchor_with_full_object_reuse(self, parser):
        """Test anchor reusing entire object block."""
        yaml_content = """
version: "1.0"
project: "Object Reuse Test"

agents:
  - &agent_template
    id: agent_a
    type: llm
    model: gpt-4
  - <<: *agent_template
    id: agent_b
    model: claude-3

workflow:
  - step: s1
    agent: agent_a
  - step: s2
    agent: agent_b
"""
        config = parser.parse_yaml(yaml_content)
        assert len(config.agents) == 2
        assert config.agents[0].id == "agent_a"
        assert config.agents[0].type == "llm"
        assert config.agents[0].model == "gpt-4"
        # agent_b overrides model but inherits type via merge
        assert config.agents[1].id == "agent_b"
        assert config.agents[1].type == "llm"
        assert config.agents[1].model == "claude-3"

    def test_merge_key_single(self, parser):
        """Test merge key (<<:) with a single anchor."""
        yaml_content = """
version: "1.0"
project: "Merge Key Test"

agents:
  - &defaults
    id: agent_a
    type: llm
    tools:
      - file_read
    guardrails: []

  - <<: *defaults
    id: agent_b
    model: gpt-4

  - <<: *defaults
    id: agent_c
    tools:
      - web_search
      - code_exec

workflow:
  - step: s1
    agent: agent_a
  - step: s2
    agent: agent_b
  - step: s3
    agent: agent_c
"""
        config = parser.parse_yaml(yaml_content)
        assert len(config.agents) == 3

        # agent_a — the original
        assert config.agents[0].id == "agent_a"
        assert config.agents[0].type == "llm"
        assert config.agents[0].tools == ["file_read"]

        # agent_b — merged with override
        assert config.agents[0].type == "llm"
        assert config.agents[1].id == "agent_b"
        assert config.agents[1].model == "gpt-4"
        assert config.agents[1].tools == ["file_read"]  # inherited from defaults

        # agent_c — merged with tools override
        assert config.agents[2].id == "agent_c"
        assert config.agents[2].tools == ["web_search", "code_exec"]

    def test_merge_key_nested_objects(self, parser):
        """Test merge key with nested nested object anchors."""
        yaml_content = """
version: "1.0"
project: "Nested Merge Test"

agents:
  - &defaults
    id: agent_a
    type: llm
    model: gpt-4
    tools:
      - file_read
    guardrails: []

  - <<: *defaults
    id: agent_b
    model: claude-3
    tools:
      - web_search
      - code_exec

  - <<: *defaults
    id: agent_c

workflow:
  - step: s1
    agent: agent_a
  - step: s2
    agent: agent_b
  - step: s3
    agent: agent_c
"""
        config = parser.parse_yaml(yaml_content)
        assert len(config.agents) == 3

        # agent_b: overrides model and tools
        assert config.agents[1].id == "agent_b"
        assert config.agents[1].type == "llm"  # inherited
        assert config.agents[1].model == "claude-3"  # overridden
        assert config.agents[1].tools == ["web_search", "code_exec"]  # overridden

        # agent_c: inherits everything
        assert config.agents[2].id == "agent_c"
        assert config.agents[2].model == "gpt-4"  # inherited
        assert config.agents[2].tools == ["file_read"]  # inherited

    def test_anchor_nested_structure(self, parser):
        """Test anchors in deeply nested YAML structures."""
        yaml_content = """
version: "1.0"
project: "Nested Anchor Test"

budget: &budget
  total_tokens: 50000
  warning_threshold: 0.75
  hard_limit: 60000

agents:
  - id: agent_a
    type: llm
    model: gpt-4

workflow:
  - step: s1
    agent: agent_a
"""
        config = parser.parse_yaml(yaml_content)
        assert config.budget is not None
        assert config.budget.total_tokens == 50000
        assert config.budget.warning_threshold == 0.75
        assert config.budget.hard_limit == 60000

    def test_anchor_list_items(self, parser):
        """Test anchors on individual list items."""
        yaml_content = """
version: "1.0"
project: "List Item Anchor Test"

agents:
  - &agent_template
    id: agent_a
    type: llm
    model: gpt-4
    tools: []
    guardrails: []

  - <<: *agent_template
    id: agent_b
    model: claude-3

  - <<: *agent_template
    id: agent_c
    model: gemini-pro

workflow:
  - step: s1
    agent: agent_a
  - step: s2
    agent: agent_b
  - step: s3
    agent: agent_c
"""
        config = parser.parse_yaml(yaml_content)
        assert len(config.agents) == 3
        assert all(a.type == "llm" for a in config.agents)
        assert config.agents[0].model == "gpt-4"
        assert config.agents[1].model == "claude-3"
        assert config.agents[2].model == "gemini-pro"

    def test_anchor_with_validation(self, parser):
        """Test that merged configs still pass validation."""
        yaml_content = """
version: "1.0"
project: "Validation Test"

agents:
  - &defaults
    id: agent_a
    type: llm
    guardrails: [guardrail_1]

  - <<: *defaults
    id: agent_b

artifacts:
  - id: artifact_x
    type: file

guardrails:
  - id: guardrail_1
    type: regex

workflow:
  - step: s1
    agent: agent_a
    artifact: artifact_x
    depends_on: []
  - step: s2
    agent: agent_b
    artifact: artifact_x
    depends_on: [s1]
"""
        config = parser.parse_yaml(yaml_content)
        errors = parser.validate(config)
        assert len(errors) == 0

    def test_anchor_alias_invalid_reference(self, parser):
        """Test that validation still catches bad refs even with anchors."""
        yaml_content = """
version: "1.0"
project: "Invalid Anchor Test"

agents:
  - &defaults
    id: agent_a
    type: llm

  - <<: *defaults
    id: agent_b

workflow:
  - step: s1
    agent: agent_a
  - step: s2
    agent: nonexistent_agent
"""
        config = parser.parse_yaml(yaml_content)
        errors = parser.validate(config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 1
        assert agent_errors[0]["value"] == "nonexistent_agent"

    def test_parse_method_dispatch_yaml(self, parser):
        """Test parse() method dispatches to parse_yaml."""
        yaml_content = """
version: "1.0"
project: "Dispatch Test"
agents:
  - id: agent_a
    type: llm
workflow:
  - step: s1
    agent: agent_a
"""
        config = parser.parse(yaml_content, format="yaml")
        assert isinstance(config, AFLConfig)
        assert config.agents[0].id == "agent_a"

    def test_parse_method_invalid_format(self, parser):
        """Test parse() raises ValueError for unsupported format."""
        with pytest.raises(ValueError, match="Unsupported format: xml"):
            parser.parse("<config/>", format="xml")
