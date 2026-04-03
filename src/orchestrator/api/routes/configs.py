"""Configs API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_configs():
    """List all config versions."""
    return {"data": []}


@router.post("/")
async def create_config():
    """Upload a new AFL config."""
    return {"config_id": "placeholder"}


@router.post("/validate")
async def validate_config():
    """Validate an AFL config without saving."""
    return {"valid": True}
