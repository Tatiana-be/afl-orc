"""Tests for PARSER-005: Link validation (agent/artifact/guardrail)."""

import pytest

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
def valid_config():
    """Create a fully valid config with all references correct."""
    return AFLConfig(
        version="1.0",
        project="Test Project",
        agents=[
            AgentConfig(id="agent_a", type="llm", model="gpt-4"),
            AgentConfig(id="agent_b", type="llm", model="claude-3"),
        ],
        artifacts=[
            ArtifactConfig(id="artifact_x", type="file"),
            ArtifactConfig(id="artifact_y", type="json"),
        ],
        guardrails=[
            GuardrailConfig(id="guardrail_1", type="regex"),
            GuardrailConfig(id="guardrail_2", type="llm_judge"),
        ],
        workflow=[
            WorkflowStep(step="step_1", agent="agent_a", artifact="artifact_x"),
            WorkflowStep(
                step="step_2",
                agent="agent_b",
                depends_on=["step_1"],
                artifact="artifact_y",
            ),
        ],
    )


# ============================================
# Agent Reference Validation
# ============================================


class TestAgentReferenceValidation:
    """Tests for validating agent references in workflow steps."""

    def test_valid_agent_references(self, parser, valid_config):
        """Valid agent references should produce no errors."""
        errors = parser.validate(valid_config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 0

    def test_invalid_agent_reference_in_step(self, parser, valid_config):
        """Step referencing unknown agent should produce error."""
        valid_config.workflow.append(WorkflowStep(step="step_3", agent="nonexistent_agent"))
        errors = parser.validate(valid_config)
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        assert len(agent_errors) == 1
        assert agent_errors[0]["step"] == "step_3"
        assert agent_errors[0]["value"] == "nonexistent_agent"

    def test_multiple_invalid_agent_references(self, parser, valid_config):
        """Multiple invalid agent references should all be reported."""
        valid_config.workflow.extend(
            [
                WorkflowStep(step="step_3", agent="ghost_agent"),
                WorkflowStep(step="step_4", agent="another_ghost"),
            ]
        )
        errors = parser.validate(valid_config)
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


# ============================================
# Artifact Reference Validation
# ============================================


class TestArtifactReferenceValidation:
    """Tests for validating artifact references in workflow steps."""

    def test_valid_artifact_references(self, parser, valid_config):
        """Valid artifact references should produce no errors."""
        errors = parser.validate(valid_config)
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        assert len(artifact_errors) == 0

    def test_invalid_artifact_reference_in_step(self, parser, valid_config):
        """Step referencing unknown artifact should produce error."""
        valid_config.workflow.append(
            WorkflowStep(
                step="step_3",
                agent="agent_a",
                artifact="nonexistent_artifact",
            )
        )
        errors = parser.validate(valid_config)
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        assert len(artifact_errors) == 1
        assert artifact_errors[0]["step"] == "step_3"
        assert artifact_errors[0]["value"] == "nonexistent_artifact"

    def test_step_without_artifact(self, parser, valid_config):
        """Step without artifact reference should be valid."""
        valid_config.workflow.append(WorkflowStep(step="step_3", agent="agent_a"))
        errors = parser.validate(valid_config)
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


# ============================================
# Guardrail Reference Validation
# ============================================


class TestGuardrailReferenceValidation:
    """Tests for validating guardrail references in agents."""

    def test_valid_guardrail_references(self, parser, valid_config):
        """Valid guardrail references should produce no errors."""
        valid_config.agents.append(
            AgentConfig(
                id="agent_c",
                type="llm",
                guardrails=["guardrail_1", "guardrail_2"],
            )
        )
        errors = parser.validate(valid_config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 0

    def test_invalid_guardrail_reference_in_agent(self, parser, valid_config):
        """Agent referencing unknown guardrail should produce error."""
        valid_config.agents.append(
            AgentConfig(
                id="agent_c",
                type="llm",
                guardrails=["nonexistent_guardrail"],
            )
        )
        errors = parser.validate(valid_config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 1
        assert guardrail_errors[0]["agent"] == "agent_c"
        assert guardrail_errors[0]["value"] == "nonexistent_guardrail"

    def test_multiple_invalid_guardrail_references(self, parser, valid_config):
        """Multiple invalid guardrail references should all be reported."""
        valid_config.agents.append(
            AgentConfig(
                id="agent_c",
                type="llm",
                guardrails=["ghost_1", "ghost_2"],
            )
        )
        errors = parser.validate(valid_config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 2

    def test_agent_without_guardrails(self, parser, valid_config):
        """Agent without guardrail references should be valid."""
        valid_config.agents.append(AgentConfig(id="agent_c", type="llm"))
        errors = parser.validate(valid_config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 0

    def test_no_guardrails_defined(self, parser):
        """Agents with guardrail reference but no guardrails defined should fail."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(
                    id="agent_a",
                    type="llm",
                    guardrails=["some_guardrail"],
                ),
            ],
            guardrails=[],
        )
        errors = parser.validate(config)
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        assert len(guardrail_errors) == 1


# ============================================
# Dependency Reference Validation
# ============================================


class TestDependencyReferenceValidation:
    """Tests for validating step dependency references."""

    def test_valid_dependency_references(self, parser, valid_config):
        """Valid dependency references should produce no errors."""
        errors = parser.validate(valid_config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 0

    def test_invalid_dependency_reference(self, parser, valid_config):
        """Step referencing unknown dependency should produce error."""
        valid_config.workflow.append(
            WorkflowStep(
                step="step_3",
                agent="agent_a",
                depends_on=["nonexistent_step"],
            )
        )
        errors = parser.validate(valid_config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 1
        assert dependency_errors[0]["step"] == "step_3"
        assert dependency_errors[0]["value"] == "nonexistent_step"

    def test_multiple_invalid_dependencies(self, parser, valid_config):
        """Multiple invalid dependencies should all be reported."""
        valid_config.workflow.append(
            WorkflowStep(
                step="step_3",
                agent="agent_a",
                depends_on=["ghost_1", "ghost_2"],
            )
        )
        errors = parser.validate(valid_config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 2

    def test_step_without_dependencies(self, parser, valid_config):
        """Step without dependencies should be valid."""
        valid_config.workflow.append(WorkflowStep(step="step_3", agent="agent_a"))
        errors = parser.validate(valid_config)
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        assert len(dependency_errors) == 0


# ============================================
# Circular Dependency Detection
# ============================================


class TestCircularDependencyDetection:
    """Tests for detecting circular dependencies in workflow."""

    def test_no_circular_dependencies(self, parser, valid_config):
        """Linear workflow should have no circular dependencies."""
        errors = parser.validate(valid_config)
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]
        assert len(cycle_errors) == 0

    def test_direct_circular_dependency(self, parser, valid_config):
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


# ============================================
# Comprehensive Validation
# ============================================


class TestComprehensiveValidation:
    """Tests for comprehensive validation with multiple error types."""

    def test_multiple_error_types(self, parser):
        """Config with multiple error types should report all."""
        config = AFLConfig(
            version="1.0",
            project="Test",
            agents=[
                AgentConfig(
                    id="agent_a",
                    type="llm",
                    guardrails=["ghost_guardrail"],
                ),
            ],
            artifacts=[ArtifactConfig(id="artifact_a", type="file")],
            guardrails=[],
            workflow=[
                WorkflowStep(
                    step="step_1",
                    agent="agent_a",
                    artifact="ghost_artifact",
                ),
                WorkflowStep(
                    step="step_2",
                    agent="ghost_agent",
                    depends_on=["ghost_step"],
                ),
                WorkflowStep(
                    step="step_3",
                    agent="agent_a",
                    depends_on=["step_4"],
                ),
                WorkflowStep(
                    step="step_4",
                    agent="agent_a",
                    depends_on=["step_3"],
                ),
            ],
        )
        errors = parser.validate(config)

        # Should have errors for: agent, artifact, guardrail, depends_on, cycle
        agent_errors = [e for e in errors if e.get("field") == "agent"]
        artifact_errors = [e for e in errors if e.get("field") == "artifact"]
        guardrail_errors = [e for e in errors if e.get("field") == "guardrail"]
        dependency_errors = [e for e in errors if e.get("field") == "depends_on"]
        cycle_errors = [e for e in errors if e.get("type") == "circular_dependency"]

        assert len(agent_errors) >= 1
        assert len(artifact_errors) >= 1
        assert len(guardrail_errors) >= 1
        assert len(dependency_errors) >= 1
        assert len(cycle_errors) >= 1

    def test_fully_valid_config(self, parser, valid_config):
        """Fully valid config should produce zero errors."""
        errors = parser.validate(valid_config)
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
