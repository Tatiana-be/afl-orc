"""Agents API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_agents():
    """List all active agents."""
    return {"data": [], "summary": {}}


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details."""
    return {"agent_id": agent_id}
