# mypy: ignore-errors
"""Admin API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/audit-logs")
async def list_audit_logs():
    """List audit logs."""
    return {"data": [], "pagination": {}}


@router.get("/system/health")
async def get_system_health():
    """Get system health status."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {},
    }
