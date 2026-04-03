# mypy: ignore-errors
"""Projects API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_projects():
    """List all projects."""
    return {"data": [], "pagination": {}}


@router.post("/")
async def create_project():
    """Create a new project."""
    return {"project_id": "placeholder"}


@router.get("/{project_id}")
async def get_project(project_id: str):
    """Get project details."""
    return {"project_id": project_id}
