"""Alerting system for AFL Orchestrator."""

import asyncio
import logging
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

import httpx

from src.orchestrator.config import settings
from src.orchestrator.observability.logging_config import get_logger

logger = get_logger("alerts")


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertChannel(Enum):
    SLACK = "slack"
    EMAIL = "email"
    WEBHOOK = "webhook"
    PAGERDUTY = "pagerduty"


@dataclass
class Alert:
    """Alert definition."""

    name: str
    severity: AlertSeverity
    message: str
    details: dict = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if self.details is None:
            self.details = {}


class AlertManager:
    """Manages alert routing and delivery."""

    def __init__(self):
        self.channels: dict[AlertChannel, str] = {}
        self.alert_history: list[Alert] = []
        self.suppression_window_seconds = 300  # 5 minutes
        self.suppressed_alerts: dict[str, datetime] = {}

    def configure_channel(self, channel: AlertChannel, webhook_url: str):
        """Configure an alert channel."""
        self.channels[channel] = webhook_url
        logger.info(f"Configured alert channel: {channel.value}")

    async def send_alert(self, alert: Alert):
        """Send an alert to configured channels."""
        # Check suppression
        suppression_key = f"{alert.name}:{alert.message}"
        if self._is_suppressed(suppression_key):
            logger.debug(f"Alert suppressed: {alert.name}")
            return

        # Log alert
        log_method = getattr(logger, alert.severity.value, logger.warning)
        log_method(
            f"ALERT [{alert.severity.value.upper()}]: {alert.name} - {alert.message}",
            extra={"alert": alert.name, "severity": alert.severity.value},
        )

        # Send to channels
        tasks = []
        for channel, url in self.channels.items():
            tasks.append(self._send_to_channel(channel, url, alert))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        # Record in history
        self.alert_history.append(alert)
        self.suppressed_alerts[suppression_key] = datetime.now(timezone.utc)

    def _is_suppressed(self, key: str) -> bool:
        """Check if alert is within suppression window."""
        if key not in self.suppressed_alerts:
            return False

        last_sent = self.suppressed_alerts[key]
        elapsed = (datetime.now(timezone.utc) - last_sent).total_seconds()
        return elapsed < self.suppression_window_seconds

    async def _send_to_channel(
        self, channel: AlertChannel, url: str, alert: Alert
    ):
        """Send alert to a specific channel."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if channel == AlertChannel.SLACK:
                    await self._send_slack(client, url, alert)
                elif channel == AlertChannel.EMAIL:
                    await self._send_email(client, url, alert)
                elif channel == AlertChannel.WEBHOOK:
                    await self._send_webhook(client, url, alert)
                elif channel == AlertChannel.PAGERDUTY:
                    await self._send_pagerduty(client, url, alert)
        except Exception as e:
            logger.error(f"Failed to send alert to {channel.value}: {e}")

    async def _send_slack(self, client: httpx.AsyncClient, url: str, alert: Alert):
        """Send alert to Slack."""
        color = {
            AlertSeverity.INFO: "#36a64f",
            AlertSeverity.WARNING: "#ffaa00",
            AlertSeverity.CRITICAL: "#ff0000",
        }.get(alert.severity, "#808080")

        payload = {
            "attachments": [
                {
                    "color": color,
                    "title": f"🚨 {alert.name}",
                    "text": alert.message,
                    "fields": [
                        {"title": k, "value": str(v), "short": True}
                        for k, v in alert.details.items()
                    ],
                    "footer": "AFL Orchestrator",
                    "ts": int(alert.timestamp.timestamp()),
                }
            ]
        }

        await client.post(url, json=payload)

    async def _send_email(self, client: httpx.AsyncClient, url: str, alert: Alert):
        """Send alert via email (via webhook)."""
        payload = {
            "to": url,
            "subject": f"[{alert.severity.value.upper()}] {alert.name}",
            "body": f"{alert.message}\n\nDetails: {alert.details}",
        }
        await client.post(url, json=payload)

    async def _send_webhook(self, client: httpx.AsyncClient, url: str, alert: Alert):
        """Send alert to generic webhook."""
        payload = {
            "alert": alert.name,
            "severity": alert.severity.value,
            "message": alert.message,
            "details": alert.details,
            "timestamp": alert.timestamp.isoformat(),
        }
        await client.post(url, json=payload)

    async def _send_pagerduty(self, client: httpx.AsyncClient, url: str, alert: Alert):
        """Send alert to PagerDuty."""
        severity_map = {
            AlertSeverity.INFO: "info",
            AlertSeverity.WARNING: "warning",
            AlertSeverity.CRITICAL: "critical",
        }

        payload = {
            "routing_key": url,
            "event_action": "trigger",
            "payload": {
                "summary": alert.message,
                "severity": severity_map.get(alert.severity, "error"),
                "source": "afl-orchestrator",
                "custom_details": alert.details,
            },
        }
        await client.post("https://events.pagerduty.com/v2/enqueue", json=payload)


# Global alert manager instance
alert_manager = AlertManager()


# ============================================
# Predefined Alerts
# ============================================

async def alert_budget_exceeded(project_id: str, usage_pct: float):
    """Alert when budget exceeds threshold."""
    await alert_manager.send_alert(
        Alert(
            name="budget_exceeded",
            severity=AlertSeverity.WARNING,
            message=f"Project {project_id} budget at {usage_pct:.1f}%",
            details={"project_id": project_id, "usage_pct": usage_pct},
        )
    )


async def alert_workflow_failed(workflow_id: str, error: str):
    """Alert when workflow fails."""
    await alert_manager.send_alert(
        Alert(
            name="workflow_failed",
            severity=AlertSeverity.CRITICAL,
            message=f"Workflow {workflow_id} failed: {error}",
            details={"workflow_id": workflow_id, "error": error},
        )
    )


async def alert_error_rate_high(component: str, rate: float):
    """Alert when error rate exceeds threshold."""
    await alert_manager.send_alert(
        Alert(
            name="error_rate_high",
            severity=AlertSeverity.CRITICAL,
            message=f"Error rate for {component}: {rate:.2%}",
            details={"component": component, "error_rate": rate},
        )
    )


async def alert_sla_breach(endpoint: str, latency_ms: float, sla_ms: float):
    """Alert when SLA is breached."""
    await alert_manager.send_alert(
        Alert(
            name="sla_breach",
            severity=AlertSeverity.WARNING,
            message=f"SLA breach for {endpoint}: {latency_ms:.0f}ms > {sla_ms:.0f}ms",
            details={
                "endpoint": endpoint,
                "latency_ms": latency_ms,
                "sla_ms": sla_ms,
            },
        )
    )
