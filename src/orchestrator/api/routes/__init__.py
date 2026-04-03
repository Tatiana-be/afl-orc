# mypy: ignore-errors
"""API routes module."""

from fastapi import APIRouter

from src.orchestrator.api.routes import admin, agents, budget, configs, events, projects, workflows

router = APIRouter()

# Include all route modules
router.include_router(projects.router, prefix="/projects", tags=["Projects"])
router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
router.include_router(agents.router, prefix="/agents", tags=["Agents"])
router.include_router(configs.router, prefix="/projects/{project_id}/configs", tags=["Configs"])
router.include_router(budget.router, prefix="/budget", tags=["Budget"])
router.include_router(events.router, prefix="/events", tags=["Events"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
