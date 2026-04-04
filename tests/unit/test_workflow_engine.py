"""Unit tests for Workflow Engine."""

import pytest

from src.orchestrator.engine.workflow_engine import WorkflowEngine


@pytest.fixture
def engine():
    """Create workflow engine instance."""
    return WorkflowEngine()


class TestWorkflowEngine:
    """Tests for WorkflowEngine."""

    @pytest.mark.asyncio
    async def test_start_workflow(self, engine):
        """Test starting a workflow returns workflow ID."""
        config = {
            "version": "1.0",
            "project": "test_project",
            "workflow": [{"step": "step_1", "agent": "test_agent"}],
        }
        workflow_id = await engine.start_workflow(config)
        assert isinstance(workflow_id, str)
        assert workflow_id == "workflow-id-placeholder"

    @pytest.mark.asyncio
    async def test_pause_workflow(self, engine):
        """Test pausing a workflow returns True."""
        workflow_id = "wf_123"
        result = await engine.pause_workflow(workflow_id)
        assert result is True

    @pytest.mark.asyncio
    async def test_resume_workflow(self, engine):
        """Test resuming a workflow returns True."""
        workflow_id = "wf_123"
        result = await engine.resume_workflow(workflow_id)
        assert result is True

    @pytest.mark.asyncio
    async def test_cancel_workflow(self, engine):
        """Test cancelling a workflow returns True."""
        workflow_id = "wf_123"
        result = await engine.cancel_workflow(workflow_id)
        assert result is True

    def test_engine_has_state_machine(self, engine):
        """Test engine has state machine instance."""
        assert engine.state_machine is not None
