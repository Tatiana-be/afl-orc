"""Unit tests for AFL Parser."""

import json

import pytest
from pydantic import ValidationError

from src.orchestrator.parser.afl_parser import AFLParser
from src.orchestrator.parser.schema import (
    AFLConfig,
    AgentConfig,
    ArtifactConfig,
    GuardrailConfig,
    WorkflowStep,
)


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


def test_parse_method_dispatch_json(parser):
    """Test parse() method dispatches to parse_json."""
    json_config = """
{
    "version": "1.0",
    "project": "Dispatch Test",
    "agents": [{"id": "agent_a", "type": "llm"}],
    "workflow": [{"step": "s1", "agent": "agent_a"}]
}
"""
    config = parser.parse(json_config, format="json")
    assert isinstance(config, AFLConfig)
    assert config.agents[0].id == "agent_a"


# ============================================
# JSON Parsing Tests (PARSER-004)
# ============================================


class TestJSONParsing:
    """Tests for JSON configuration parsing."""

    def test_parse_full_json_config(self, parser):
        """Test parsing a complete JSON configuration."""
        json_config = """
{
    "version": "1.0",
    "project": "Full JSON Config Test",
    "budget": {
        "total_tokens": 100000,
        "warning_threshold": 0.8
    },
    "agents": [
        {
            "id": "reviewer",
            "type": "llm",
            "model": "gpt-4",
            "tools": ["file_read", "diff"],
            "guardrails": ["no_secrets"]
        }
    ],
    "artifacts": [
        {"id": "report", "type": "json"}
    ],
    "guardrails": [
        {"id": "no_secrets", "type": "regex"}
    ],
    "workflow": [
        {
            "step": "review",
            "agent": "reviewer",
            "artifact": "report",
            "depends_on": []
        }
    ]
}
"""
        config = parser.parse_json(json_config)
        assert config.version == "1.0"
        assert config.project == "Full JSON Config Test"
        assert config.budget.total_tokens == 100000
        assert len(config.agents) == 1
        assert config.agents[0].tools == ["file_read", "diff"]
        assert config.agents[0].guardrails == ["no_secrets"]
        assert len(config.artifacts) == 1
        assert config.guardrails[0].id == "no_secrets"
        assert config.workflow[0].step == "review"

    def test_json_validation_passes(self, parser):
        """Test that valid JSON config passes validation."""
        json_config = """
{
    "version": "1.0",
    "project": "JSON Validation Test",
    "agents": [{"id": "a1", "type": "llm"}],
    "workflow": [{"step": "s1", "agent": "a1"}]
}
"""
        config = parser.parse_json(json_config)
        errors = parser.validate(config)
        assert len(errors) == 0

    def test_json_validation_catches_invalid_refs(self, parser):
        """Test that JSON config validation catches invalid references."""
        json_config = """
{
    "version": "1.0",
    "project": "Invalid JSON Test",
    "agents": [{"id": "a1", "type": "llm"}],
    "workflow": [
        {"step": "s1", "agent": "nonexistent"},
        {"step": "s2", "agent": "a1", "depends_on": ["ghost_step"]}
    ]
}
"""
        config = parser.parse_json(json_config)
        errors = parser.validate(config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        dep_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(agent_errors) == 1
        assert len(dep_errors) == 1

    def test_json_schema_validation(self, parser):
        """Test that JSON schema validation catches type errors."""
        json_config = """
{
    "version": "bad-version",
    "project": "Schema Test",
    "agents": [],
    "workflow": []
}
"""
        with pytest.raises(ValidationError):
            parser.parse_json(json_config)

    def test_json_malformed(self, parser):
        """Test that malformed JSON raises JSONDecodeError."""
        malformed = '{"version": "1.0", "project":}'
        with pytest.raises(json.JSONDecodeError):
            parser.parse_json(malformed)

    def test_json_unicode_strings(self, parser):
        """Test that JSON with unicode strings parses correctly."""
        json_config = """
{
    "version": "1.0",
    "project": "Тест Юникод Проект 🚀",
    "agents": [{"id": "агент_1", "type": "llm", "model": "gpt-4"}],
    "workflow": [{"step": "анализ", "agent": "агент_1"}]
}
"""
        config = parser.parse_json(json_config)
        assert config.project == "Тест Юникод Проект 🚀"
        assert config.agents[0].id == "агент_1"
        assert config.workflow[0].step == "анализ"

    def test_json_empty_arrays(self, parser):
        """Test JSON with empty arrays for optional fields."""
        json_config = """
{
    "version": "1.0",
    "project": "Empty Arrays Test",
    "agents": [],
    "artifacts": [],
    "guardrails": [],
    "workflow": []
}
"""
        config = parser.parse_json(json_config)
        assert config.agents == []
        assert config.artifacts == []
        assert config.guardrails == []
        assert config.workflow == []

    def test_json_minimal_config(self, parser):
        """Test minimal valid JSON config (required fields only)."""
        json_config = """
{"version": "1.0", "project": "Minimal", "agents": [], "workflow": []}
"""
        config = parser.parse_json(json_config)
        assert config.version == "1.0"
        assert config.project == "Minimal"
        assert config.budget is None


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


# ============================================
# Link Validation Tests (PARSER-005)
# ============================================


class TestAgentReferenceValidation:
    """Tests for validating agent references in workflow steps."""

    def test_valid_agent_references(self, parser):
        """Valid agent references should produce no errors."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(id="agent_a", type="llm", model="gpt-4"),
                AgentConfig(id="agent_b", type="llm", model="claude-3"),
            ],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
                WorkflowStep(step="step_2", agent="agent_b"),
            ],
        )
        errors = parser.validate(config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 0

    def test_invalid_agent_reference_in_step(self, parser):
        """Step referencing unknown agent should produce error."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
                WorkflowStep(step="step_2", agent="nonexistent_agent"),
            ],
        )
        errors = parser.validate(config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 1
        assert agent_errors[0]["step"] == "step_2"
        assert agent_errors[0]["value"] == "nonexistent_agent"

    def test_multiple_invalid_agent_references(self, parser):
        """Multiple invalid agent references should all be reported."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_1", agent="ghost_1"),
                WorkflowStep(step="step_2", agent="ghost_2"),
            ],
        )
        errors = parser.validate(config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 2

    def test_no_agents_defined(self, parser):
        """Workflow steps with no agents defined should all fail."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[],
            workflow=[
                WorkflowStep(step="step_1", agent="any_agent"),
            ],
        )
        errors = parser.validate(config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 1
        assert agent_errors[0]["value"] == "any_agent"


class TestArtifactReferenceValidation:
    """Tests for validating artifact references in workflow steps."""

    def test_valid_artifact_references(self, parser):
        """Valid artifact references should produce no errors."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            artifacts=[
                ArtifactConfig(id="artifact_x", type="file"),
                ArtifactConfig(id="artifact_y", type="json"),
            ],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a", artifact="artifact_x"),
                WorkflowStep(step="step_2", agent="agent_a", artifact="artifact_y"),
            ],
        )
        errors = parser.validate(config)
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        assert len(artifact_errors) == 0

    def test_invalid_artifact_reference_in_step(self, parser):
        """Step referencing unknown artifact should produce error."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            artifacts=[ArtifactConfig(id="artifact_x", type="file")],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a", artifact="ghost_artifact"),
            ],
        )
        errors = parser.validate(config)
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        assert len(artifact_errors) == 1
        assert artifact_errors[0]["step"] == "step_1"
        assert artifact_errors[0]["value"] == "ghost_artifact"

    def test_step_without_artifact(self, parser):
        """Step without artifact reference should be valid."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            artifacts=[ArtifactConfig(id="artifact_x", type="file")],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
            ],
        )
        errors = parser.validate(config)
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        assert len(artifact_errors) == 0

    def test_no_artifacts_defined(self, parser):
        """Steps with artifact reference but no artifacts defined should fail."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            artifacts=[],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a", artifact="some_artifact"),
            ],
        )
        errors = parser.validate(config)
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        assert len(artifact_errors) == 1


class TestGuardrailReferenceValidation:
    """Tests for validating guardrail references in agents."""

    def test_valid_guardrail_references(self, parser):
        """Valid guardrail references should produce no errors."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(
                    id="agent_a",
                    type="llm",
                    guardrails=["guardrail_1", "guardrail_2"],
                ),
            ],
            guardrails=[
                GuardrailConfig(id="guardrail_1", type="regex"),
                GuardrailConfig(id="guardrail_2", type="llm_judge"),
            ],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
            ],
        )
        errors = parser.validate(config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 0

    def test_invalid_guardrail_reference_in_agent(self, parser):
        """Agent referencing unknown guardrail should produce error."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(
                    id="agent_a",
                    type="llm",
                    guardrails=["nonexistent_guardrail"],
                ),
            ],
            guardrails=[GuardrailConfig(id="guardrail_1", type="regex")],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
            ],
        )
        errors = parser.validate(config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 1
        assert guardrail_errors[0]["agent"] == "agent_a"
        assert guardrail_errors[0]["value"] == "nonexistent_guardrail"

    def test_multiple_invalid_guardrail_references(self, parser):
        """Multiple invalid guardrail references should all be reported."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(
                    id="agent_a",
                    type="llm",
                    guardrails=["ghost_1", "ghost_2"],
                ),
            ],
            guardrails=[],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
            ],
        )
        errors = parser.validate(config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 2

    def test_agent_without_guardrails(self, parser):
        """Agent without guardrail references should be valid."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            guardrails=[],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
            ],
        )
        errors = parser.validate(config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 0


class TestDependencyReferenceValidation:
    """Tests for validating step dependency references."""

    def test_valid_dependency_references(self, parser):
        """Valid dependency references should produce no errors."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a"),
                WorkflowStep(step="step_b", agent="agent_a", depends_on=["step_a"]),
                WorkflowStep(step="step_c", agent="agent_a", depends_on=["step_a", "step_b"]),
            ],
        )
        errors = parser.validate(config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 0

    def test_invalid_dependency_reference(self, parser):
        """Step referencing unknown dependency should produce error."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a"),
                WorkflowStep(step="step_b", agent="agent_a", depends_on=["ghost_step"]),
            ],
        )
        errors = parser.validate(config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 1
        assert dependency_errors[0]["step"] == "step_b"
        assert dependency_errors[0]["value"] == "ghost_step"

    def test_multiple_invalid_dependencies(self, parser):
        """Multiple invalid dependencies should all be reported."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(
                    step="step_a",
                    agent="agent_a",
                    depends_on=["ghost_1", "ghost_2"],
                ),
            ],
        )
        errors = parser.validate(config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 2

    def test_step_without_dependencies(self, parser):
        """Step without dependencies should be valid."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_1", agent="agent_a"),
                WorkflowStep(step="step_2", agent="agent_a"),
            ],
        )
        errors = parser.validate(config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 0


# ============================================
# Circular Dependency Detection (PARSER-006)
# ============================================


class TestCircularDependencyDetection:
    """Tests for detecting circular dependencies in workflow."""

    def test_no_circular_dependencies(self, parser):
        """Linear workflow should have no circular dependencies."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a"),
                WorkflowStep(step="step_b", agent="agent_a", depends_on=["step_a"]),
                WorkflowStep(step="step_c", agent="agent_a", depends_on=["step_b"]),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) == 0

    def test_direct_circular_dependency(self, parser):
        """A -> B -> A should be detected as circular."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(id="agent_a", type="llm"),
                AgentConfig(id="agent_b", type="llm"),
            ],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a", depends_on=["step_b"]),
                WorkflowStep(step="step_b", agent="agent_b", depends_on=["step_a"]),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) > 0

    def test_indirect_circular_dependency(self, parser):
        """A -> B -> C -> A should be detected as circular."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a", depends_on=["step_c"]),
                WorkflowStep(step="step_b", agent="agent_a", depends_on=["step_a"]),
                WorkflowStep(step="step_c", agent="agent_a", depends_on=["step_b"]),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) > 0

    def test_self_dependency(self, parser):
        """Step depending on itself should be detected."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a", depends_on=["step_a"]),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) > 0

    def test_complex_graph_without_cycles(self, parser):
        """Complex DAG without cycles should be valid."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="step_a", agent="agent_a"),
                WorkflowStep(step="step_b", agent="agent_a", depends_on=["step_a"]),
                WorkflowStep(step="step_c", agent="agent_a", depends_on=["step_a"]),
                WorkflowStep(
                    step="step_d",
                    agent="agent_a",
                    depends_on=["step_b", "step_c"],
                ),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) == 0

    def test_multiple_cycles_detected(self, parser):
        """Multiple independent cycles should all be detected."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="a", agent="agent_a", depends_on=["b"]),
                WorkflowStep(step="b", agent="agent_a", depends_on=["a"]),
                WorkflowStep(step="c", agent="agent_a", depends_on=["d"]),
                WorkflowStep(step="d", agent="agent_a", depends_on=["c"]),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) >= 1

    def test_circular_dependency_error_structure(self, parser):
        """Circular dependency errors should have consistent structure."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            workflow=[
                WorkflowStep(step="a", agent="agent_a", depends_on=["b"]),
                WorkflowStep(step="b", agent="agent_a", depends_on=["a"]),
            ],
        )
        errors = parser.validate(config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) > 0
        err = cycle_errors[0]
        assert "field" in err
        assert "cycle" in err
        assert "message" in err
        assert err["field"] == "depends_on"
        assert isinstance(err["cycle"], list)
        assert "Circular dependency detected" in err["message"]


# ============================================
# Comprehensive Validation
# ============================================


class TestComprehensiveValidation:
    """Tests for comprehensive validation with multiple error types."""

    def test_fully_valid_config(self, parser):
        """Fully valid config should produce zero errors."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[AgentConfig(id="agent_a", type="llm")],
            artifacts=[ArtifactConfig(id="artifact_x", type="file")],
            guardrails=[GuardrailConfig(id="gr_1", type="regex")],
            workflow=[
                WorkflowStep(
                    step="step_1",
                    agent="agent_a",
                    artifact="artifact_x",
                    depends_on=[],
                ),
            ],
        )
        errors = parser.validate(config)
        assert len(errors) == 0

    def test_error_structure(self, parser):
        """Errors should have consistent structure."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[],
            workflow=[
                WorkflowStep(step="step_1", agent="ghost"),
            ],
        )
        errors = parser.validate(config)
        assert len(errors) > 0
        error = errors[0]
        assert "type" in error
        assert "message" in error
        assert error["type"] == "invalid_reference"
