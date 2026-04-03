"""Workflow State Machine implementation."""

from enum import Enum


class WorkflowState(str, Enum):
    """Workflow states."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Valid state transitions
TRANSITIONS = {
    WorkflowState.PENDING: [WorkflowState.QUEUED, WorkflowState.CANCELLED],
    WorkflowState.QUEUED: [WorkflowState.RUNNING, WorkflowState.CANCELLED],
    WorkflowState.RUNNING: [
        WorkflowState.PAUSED,
        WorkflowState.COMPLETED,
        WorkflowState.FAILED,
        WorkflowState.CANCELLED,
    ],
    WorkflowState.PAUSED: [WorkflowState.RUNNING, WorkflowState.CANCELLED],
    WorkflowState.FAILED: [WorkflowState.QUEUED],  # For retry
}


class WorkflowStateMachine:
    """State machine for workflow execution."""

    def __init__(self, initial_state: WorkflowState = WorkflowState.PENDING):
        self.state = initial_state

    def can_transition(self, target: WorkflowState) -> bool:
        """Check if transition is valid."""
        return target in TRANSITIONS.get(self.state, [])

    def transition(self, target: WorkflowState) -> bool:
        """Perform state transition."""
        if not self.can_transition(target):
            raise ValueError(f"Invalid transition: {self.state} -> {target}")
        self.state = target
        return True
