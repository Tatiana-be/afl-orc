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
