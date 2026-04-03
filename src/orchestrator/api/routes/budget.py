"""Budget API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/projects/{project_id}")
async def get_project_budget(project_id: str):
    """Get project budget information."""
    return {"project_id": project_id, "budget": {}}


@router.post("/alerts")
async def create_budget_alert():
    """Create a budget alert."""
    return {"alert_id": "placeholder"}
