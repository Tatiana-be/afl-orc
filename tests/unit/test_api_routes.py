"""Unit tests for API routes."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.orchestrator.main import app


@pytest.fixture
async def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ============================================
# Admin API Tests
# ============================================


class TestAdminRoutes:
    """Tests for admin API routes."""

    @pytest.mark.asyncio
    async def test_list_audit_logs(self, client):
        """Test listing audit logs returns empty list."""
        response = await client.get("/api/v1/admin/audit-logs")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert data["data"] == []

    @pytest.mark.asyncio
    async def test_get_system_health(self, client):
        """Test getting system health status."""
        response = await client.get("/api/v1/admin/system/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "components" in data


# ============================================
# Agents API Tests
# ============================================


class TestAgentsRoutes:
    """Tests for agents API routes."""

    @pytest.mark.asyncio
    async def test_list_agents(self, client):
        """Test listing agents returns empty list."""
        response = await client.get("/api/v1/agents/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "summary" in data
        assert data["data"] == []

    @pytest.mark.asyncio
    async def test_get_agent(self, client):
        """Test getting agent details."""
        agent_id = "test_agent_123"
        response = await client.get(f"/api/v1/agents/{agent_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["agent_id"] == agent_id


# ============================================
# Workflows API Tests
# ============================================


class TestWorkflowsRoutes:
    """Tests for workflows API routes."""

    @pytest.mark.asyncio
    async def test_list_workflows(self, client):
        """Test listing workflows returns empty list."""
        response = await client.get("/api/v1/workflows/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert data["data"] == []

    @pytest.mark.asyncio
    async def test_create_workflow(self, client):
        """Test creating a workflow returns placeholder."""
        response = await client.post("/api/v1/workflows/")
        assert response.status_code == 200
        data = response.json()
        assert "workflow_id" in data
        assert data["status"] == "queued"

    @pytest.mark.asyncio
    async def test_get_workflow(self, client):
        """Test getting workflow details."""
        workflow_id = "wf_12345"
        response = await client.get(f"/api/v1/workflows/{workflow_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["workflow_id"] == workflow_id

    @pytest.mark.asyncio
    async def test_cancel_workflow(self, client):
        """Test cancelling a workflow."""
        workflow_id = "wf_12345"
        response = await client.delete(f"/api/v1/workflows/{workflow_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"


# ============================================
# Budget API Tests
# ============================================


class TestBudgetRoutes:
    """Tests for budget API routes."""

    @pytest.mark.asyncio
    async def test_get_project_budget(self, client):
        """Test getting project budget info."""
        project_id = "proj_123"
        response = await client.get(f"/api/v1/budget/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == project_id
        assert "budget" in data

    @pytest.mark.asyncio
    async def test_create_budget_alert(self, client):
        """Test creating a budget alert."""
        response = await client.post("/api/v1/budget/alerts")
        assert response.status_code == 200
        data = response.json()
        assert "alert_id" in data


# ============================================
# Configs API Tests
# ============================================


class TestConfigsRoutes:
    """Tests for configs API routes."""

    @pytest.mark.asyncio
    async def test_list_configs(self, client):
        """Test listing configs returns empty list."""
        project_id = "proj_123"
        response = await client.get(f"/api/v1/projects/{project_id}/configs/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"] == []

    @pytest.mark.asyncio
    async def test_create_config(self, client):
        """Test creating a config returns placeholder."""
        project_id = "proj_123"
        response = await client.post(f"/api/v1/projects/{project_id}/configs/")
        assert response.status_code == 200
        data = response.json()
        assert "config_id" in data

    @pytest.mark.asyncio
    async def test_validate_config(self, client):
        """Test validating a config."""
        project_id = "proj_123"
        response = await client.post(f"/api/v1/projects/{project_id}/configs/validate")
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True


# ============================================
# Events API Tests
# ============================================


class TestEventsRoutes:
    """Tests for events API routes."""

    @pytest.mark.asyncio
    async def test_list_events(self, client):
        """Test listing events returns empty list."""
        response = await client.get("/api/v1/events/")
        assert response.status_code == 200
        data = response.json()
        assert "events" in data
        assert data["events"] == []

    @pytest.mark.asyncio
    async def test_create_webhook(self, client):
        """Test creating a webhook returns placeholder."""
        response = await client.post("/api/v1/events/webhooks")
        assert response.status_code == 200
        data = response.json()
        assert "webhook_id" in data


# ============================================
# Projects API Tests
# ============================================


class TestProjectsRoutes:
    """Tests for projects API routes."""

    @pytest.mark.asyncio
    async def test_list_projects(self, client):
        """Test listing projects returns empty list."""
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert data["data"] == []

    @pytest.mark.asyncio
    async def test_create_project(self, client):
        """Test creating a project returns placeholder."""
        response = await client.post("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert "project_id" in data

    @pytest.mark.asyncio
    async def test_get_project(self, client):
        """Test getting project details."""
        project_id = "proj_456"
        response = await client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == project_id
