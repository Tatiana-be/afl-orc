"""Test configuration and fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.orchestrator.main import app


@pytest.fixture
async def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_config():
    """Sample AFL configuration for testing."""
    return {
        "version": "1.0",
        "project": "Test Project",
        "budget": {"total_tokens": 100000, "warning_threshold": 0.8},
        "agents": [
            {
                "id": "test_agent",
                "type": "llm",
                "model": "gpt-4",
            }
        ],
        "workflow": [
            {
                "step": "test_step",
                "agent": "test_agent",
            }
        ],
    }
