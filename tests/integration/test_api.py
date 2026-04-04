"""Integration tests for API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AFL Orchestrator"


@pytest.mark.asyncio
async def test_list_projects(client):
    """Test list projects endpoint."""
    response = await client.get("/api/v1/projects/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.asyncio
async def test_list_workflows(client):
    """Test list workflows endpoint."""
    response = await client.get("/api/v1/workflows/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
