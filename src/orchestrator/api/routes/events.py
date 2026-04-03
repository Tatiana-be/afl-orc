# mypy: ignore-errors
"""Events API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_events():
    """List all available event types."""
    return {"events": []}


@router.post("/webhooks")
async def create_webhook():
    """Create a new webhook."""
    return {"webhook_id": "placeholder"}
