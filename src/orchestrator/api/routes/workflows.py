# mypy: ignore-errors
"""Workflows API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_workflows():
    """List all workflows."""
    return {"data": [], "pagination": {}}


@router.post("/")
async def create_workflow():
    """Create and start a new workflow."""
    return {"workflow_id": "placeholder", "status": "queued"}


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get workflow details."""
    return {"workflow_id": workflow_id}


@router.delete("/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel a workflow."""
    return {"status": "cancelled"}
