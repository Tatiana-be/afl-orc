"""Unit tests for Workflow State Machine."""

import pytest

from src.orchestrator.engine.state_machine import WorkflowState, WorkflowStateMachine


@pytest.fixture
def state_machine():
    """Create state machine instance."""
    return WorkflowStateMachine()


def test_initial_state(state_machine):
    """Test initial state is PENDING."""
    assert state_machine.state == WorkflowState.PENDING


def test_valid_transition_pending_to_queued(state_machine):
    """Test valid transition from PENDING to QUEUED."""
    assert state_machine.can_transition(WorkflowState.QUEUED)
    state_machine.transition(WorkflowState.QUEUED)
    assert state_machine.state == WorkflowState.QUEUED


def test_valid_transition_queued_to_running(state_machine):
    """Test valid transition from QUEUED to RUNNING."""
    state_machine.transition(WorkflowState.QUEUED)
    state_machine.transition(WorkflowState.RUNNING)
    assert state_machine.state == WorkflowState.RUNNING


def test_valid_transition_running_to_paused(state_machine):
    """Test valid transition from RUNNING to PAUSED."""
    state_machine.transition(WorkflowState.QUEUED)
    state_machine.transition(WorkflowState.RUNNING)
    state_machine.transition(WorkflowState.PAUSED)
    assert state_machine.state == WorkflowState.PAUSED


def test_invalid_transition(state_machine):
    """Test invalid transition raises ValueError."""
    with pytest.raises(ValueError, match="Invalid transition"):
        state_machine.transition(WorkflowState.COMPLETED)


def test_completed_is_terminal(state_machine):
    """Test COMPLETED state has no outgoing transitions."""
    state_machine.transition(WorkflowState.QUEUED)
    state_machine.transition(WorkflowState.RUNNING)
    state_machine.transition(WorkflowState.COMPLETED)

    assert not state_machine.can_transition(WorkflowState.RUNNING)
    assert not state_machine.can_transition(WorkflowState.PENDING)
