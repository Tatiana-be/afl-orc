"""Unit tests for AlertManager."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from src.orchestrator.observability.alerts import (
    Alert,
    AlertChannel,
    AlertManager,
    AlertSeverity,
    alert_budget_exceeded,
    alert_error_rate_high,
    alert_sla_breach,
    alert_workflow_failed,
)


@pytest.fixture
def alert_manager():
    """Create alert manager instance."""
    return AlertManager()


@pytest.fixture
def sample_alert():
    """Create sample alert."""
    return Alert(
        name="test_alert",
        severity=AlertSeverity.WARNING,
        message="Test alert message",
        details={"key": "value"},
    )


class TestAlert:
    """Tests for Alert dataclass."""

    def test_alert_creation(self):
        """Test creating an alert."""
        alert = Alert(
            name="test",
            severity=AlertSeverity.INFO,
            message="Test message",
        )
        assert alert.name == "test"
        assert alert.severity == AlertSeverity.INFO
        assert alert.message == "Test message"
        assert alert.details == {}
        assert alert.timestamp is not None

    def test_alert_with_details(self):
        """Test creating alert with details."""
        details = {"project_id": "proj_123"}
        alert = Alert(
            name="budget_alert",
            severity=AlertSeverity.CRITICAL,
            message="Budget exceeded",
            details=details,
        )
        assert alert.details == details

    def test_alert_post_init_sets_timestamp(self):
        """Test alert sets timestamp on creation."""
        alert = Alert(
            name="test",
            severity=AlertSeverity.WARNING,
            message="Test",
        )
        assert isinstance(alert.timestamp, datetime)

    def test_alert_post_init_sets_empty_details(self):
        """Test alert sets empty dict when details is None."""
        alert = Alert(
            name="test",
            severity=AlertSeverity.INFO,
            message="Test",
            details=None,
        )
        assert alert.details == {}


class TestAlertManager:
    """Tests for AlertManager."""

    def test_configure_channel(self, alert_manager):
        """Test configuring an alert channel."""
        alert_manager.configure_channel(AlertChannel.SLACK, "https://slack.webhook.url")
        assert AlertChannel.SLACK in alert_manager.channels
        assert alert_manager.channels[AlertChannel.SLACK] == "https://slack.webhook.url"

    def test_alert_history_empty(self, alert_manager):
        """Test alert history is initially empty."""
        assert len(alert_manager.alert_history) == 0

    def test_suppression_window_default(self, alert_manager):
        """Test suppression window is 5 minutes by default."""
        assert alert_manager.suppression_window_seconds == 300

    @pytest.mark.asyncio
    async def test_send_alert_without_channels(self, alert_manager, sample_alert):
        """Test sending alert without configured channels."""
        await alert_manager.send_alert(sample_alert)
        assert len(alert_manager.alert_history) == 1
        assert alert_manager.alert_history[0].name == "test_alert"

    @pytest.mark.asyncio
    async def test_alert_suppression(self, alert_manager, sample_alert):
        """Test duplicate alerts are suppressed within window."""
        # First alert should be sent
        await alert_manager.send_alert(sample_alert)
        assert len(alert_manager.alert_history) == 1

        # Second alert immediately should be suppressed
        await alert_manager.send_alert(sample_alert)
        assert len(alert_manager.alert_history) == 1  # Still 1, second was suppressed

    @pytest.mark.asyncio
    async def test_alert_suppression_expires(self, alert_manager, sample_alert):
        """Test alerts are sent again after suppression window expires."""
        # First alert
        await alert_manager.send_alert(sample_alert)
        assert len(alert_manager.alert_history) == 1

        # Manually set timestamp to past to expire suppression
        key = f"{sample_alert.name}:{sample_alert.message}"
        past_time = datetime.now(UTC) - timedelta(seconds=600)  # 10 minutes ago
        alert_manager.suppressed_alerts[key] = past_time

        # Second alert should be sent after window expires
        await alert_manager.send_alert(sample_alert)
        assert len(alert_manager.alert_history) == 2

    @pytest.mark.asyncio
    async def test_is_suppressed_new_key(self, alert_manager):
        """Test new alert key is not suppressed."""
        assert alert_manager._is_suppressed("new_alert:test") is False

    @pytest.mark.asyncio
    async def test_is_suppressed_within_window(self, alert_manager):
        """Test alert is suppressed within window."""
        key = "test:alert"
        alert_manager.suppressed_alerts[key] = datetime.now(UTC)
        assert alert_manager._is_suppressed(key) is True

    @pytest.mark.asyncio
    async def test_is_suppressed_expired_window(self, alert_manager):
        """Test alert is not suppressed after window expires."""
        key = "test:alert"
        past_time = datetime.now(UTC) - timedelta(seconds=600)
        alert_manager.suppressed_alerts[key] = past_time
        assert alert_manager._is_suppressed(key) is False


class TestAlertChannelSending:
    """Tests for sending alerts to different channels."""

    @pytest.mark.asyncio
    async def test_send_to_slack(self, alert_manager):
        """Test sending alert to Slack."""
        alert_manager.configure_channel(AlertChannel.SLACK, "https://slack.webhook.url")
        alert = Alert(
            name="slack_test",
            severity=AlertSeverity.CRITICAL,
            message="Critical issue",
        )

        with patch("src.orchestrator.observability.alerts.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock()
            await alert_manager.send_alert(alert)

    @pytest.mark.asyncio
    async def test_send_to_webhook(self, alert_manager):
        """Test sending alert to webhook."""
        alert_manager.configure_channel(AlertChannel.WEBHOOK, "https://webhook.url")
        alert = Alert(
            name="webhook_test",
            severity=AlertSeverity.INFO,
            message="Info message",
        )

        with patch("src.orchestrator.observability.alerts.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock()
            await alert_manager.send_alert(alert)


class TestPredefinedAlerts:
    """Tests for predefined alert helper functions."""

    @pytest.mark.asyncio
    async def test_alert_budget_exceeded(self):
        """Test budget exceeded alert."""
        await alert_budget_exceeded("proj_123", 85.5)

    @pytest.mark.asyncio
    async def test_alert_workflow_failed(self):
        """Test workflow failed alert."""
        await alert_workflow_failed("wf_123", "Task failed")

    @pytest.mark.asyncio
    async def test_alert_error_rate_high(self):
        """Test error rate high alert."""
        await alert_error_rate_high("api", 0.15)

    @pytest.mark.asyncio
    async def test_alert_sla_breach(self):
        """Test SLA breach alert."""
        await alert_sla_breach("/api/v1/workflows", 5000.0, 3000.0)
