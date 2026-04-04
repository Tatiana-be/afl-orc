"""Unit tests for Prometheus metrics."""

from src.orchestrator.observability.metrics import (
    agent_active,
    agent_execution_total,
    api_request_duration,
    api_request_total,
    budget_remaining,
    cost_usd_total,
    error_rate,
    guardrail_check_total,
    guardrail_violations_total,
    integration_circuit_breaker,
    integration_request_total,
    metrics_endpoint,
    queue_length,
    queue_processing_time,
    token_usage_total,
    uptime_seconds,
    workflow_active,
    workflow_completed_total,
    workflow_failed_total,
    workflow_started_total,
)


class TestWorkflowMetrics:
    """Tests for workflow metrics."""

    def test_workflow_started_total(self):
        """Test workflow_started_total counter."""
        workflow_started_total.labels(project_id="proj_123", config_version="1.0").inc()
        # Should not raise exception

    def test_workflow_completed_total(self):
        """Test workflow_completed_total counter."""
        workflow_completed_total.labels(project_id="proj_123").inc()

    def test_workflow_failed_total(self):
        """Test workflow_failed_total counter."""
        workflow_failed_total.labels(project_id="proj_123", error_code="TIMEOUT").inc()

    def test_workflow_active_gauge(self):
        """Test workflow_active gauge."""
        workflow_active.labels(status="running").set(5)
        assert workflow_active.labels(status="running")._value.get() == 5


class TestAgentMetrics:
    """Tests for agent metrics."""

    def test_agent_execution_total(self):
        """Test agent_execution_total counter."""
        agent_execution_total.labels(agent_id="agent_1", status="success").inc()

    def test_agent_active_gauge(self):
        """Test agent_active gauge."""
        agent_active.labels(status="idle").set(10)
        assert agent_active.labels(status="idle")._value.get() == 10


class TestBudgetMetrics:
    """Tests for budget metrics."""

    def test_token_usage_total(self):
        """Test token_usage_total counter."""
        token_usage_total.labels(project_id="proj_123", provider="openai", model="gpt-4").inc(1000)

    def test_cost_usd_total(self):
        """Test cost_usd_total counter."""
        cost_usd_total.labels(project_id="proj_123", provider="openai").inc(1.50)

    def test_budget_remaining_gauge(self):
        """Test budget_remaining gauge."""
        budget_remaining.labels(project_id="proj_123", type="usd").set(500.0)


class TestGuardrailMetrics:
    """Tests for guardrail metrics."""

    def test_guardrail_check_total(self):
        """Test guardrail_check_total counter."""
        guardrail_check_total.labels(guardrail_id="regex_check", result="pass").inc()

    def test_guardrail_violations_total(self):
        """Test guardrail_violations_total counter."""
        guardrail_violations_total.labels(guardrail_id="content_filter", action="block").inc()


class TestAPIMetrics:
    """Tests for API metrics."""

    def test_api_request_total(self):
        """Test api_request_total counter."""
        api_request_total.labels(method="GET", endpoint="/workflows", status_code="200").inc()

    def test_api_request_duration(self):
        """Test api_request_duration histogram."""
        with api_request_duration.labels(method="GET", endpoint="/workflows").time():
            pass  # Simulate request


class TestIntegrationMetrics:
    """Tests for integration metrics."""

    def test_integration_request_total(self):
        """Test integration_request_total counter."""
        integration_request_total.labels(integration="jira", status="success").inc()

    def test_integration_circuit_breaker_gauge(self):
        """Test integration_circuit_breaker gauge."""
        integration_circuit_breaker.labels(integration="jira").set(0)


class TestQueueMetrics:
    """Tests for queue metrics."""

    def test_queue_length_gauge(self):
        """Test queue_length gauge."""
        queue_length.labels(queue_name="workflow_queue").set(15)

    def test_queue_processing_time_histogram(self):
        """Test queue_processing_time histogram."""
        queue_processing_time.labels(queue_name="workflow_queue").observe(1.5)


class TestSystemMetrics:
    """Tests for system metrics."""

    def test_error_rate_gauge(self):
        """Test error_rate gauge."""
        error_rate.labels(component="api").set(0.05)

    def test_uptime_seconds_gauge(self):
        """Test uptime_seconds gauge."""
        uptime_seconds.set(3600)


class TestMetricsEndpoint:
    """Tests for metrics endpoint."""

    def test_metrics_endpoint_returns_bytes(self):
        """Test metrics endpoint returns bytes."""
        result = metrics_endpoint()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bytes)

    def test_metrics_endpoint_content_type(self):
        """Test metrics endpoint returns content type."""
        _, content_type = metrics_endpoint()
        assert "text/plain" in content_type or "application/" in content_type
