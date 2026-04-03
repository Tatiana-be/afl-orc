"""Prometheus metrics for AFL Orchestrator."""

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# ============================================
# Workflow Metrics
# ============================================

workflow_started_total = Counter(
    "afl_workflow_started_total",
    "Total number of workflows started",
    ["project_id", "config_version"],
)

workflow_completed_total = Counter(
    "afl_workflow_completed_total",
    "Total number of workflows completed successfully",
    ["project_id"],
)

workflow_failed_total = Counter(
    "afl_workflow_failed_total",
    "Total number of workflows failed",
    ["project_id", "error_code"],
)

workflow_execution_duration = Histogram(
    "afl_workflow_execution_duration_seconds",
    "Time spent executing workflows",
    ["project_id"],
    buckets=[10, 30, 60, 120, 300, 600, 1800, 3600],
)

workflow_active = Gauge(
    "afl_workflow_active",
    "Number of currently active workflows",
    ["status"],  # running, paused, queued
)

# ============================================
# Agent Metrics
# ============================================

agent_execution_total = Counter(
    "afl_agent_execution_total",
    "Total number of agent executions",
    ["agent_id", "status"],  # success, failed
)

agent_execution_duration = Histogram(
    "afl_agent_execution_duration_seconds",
    "Time spent executing agent tasks",
    ["agent_id", "model"],
    buckets=[0.5, 1, 2, 5, 10, 30, 60],
)

agent_active = Gauge(
    "afl_agent_active",
    "Number of active agents",
    ["status"],  # idle, busy, error
)

# ============================================
# Budget Metrics
# ============================================

token_usage_total = Counter(
    "afl_token_usage_total",
    "Total number of tokens used",
    ["project_id", "provider", "model"],
)

cost_usd_total = Counter(
    "afl_cost_usd_total",
    "Total cost in USD",
    ["project_id", "provider"],
)

budget_remaining = Gauge(
    "afl_budget_remaining",
    "Remaining budget",
    ["project_id", "type"],  # tokens, usd
)

# ============================================
# Guardrail Metrics
# ============================================

guardrail_check_total = Counter(
    "afl_guardrail_check_total",
    "Total number of guardrail checks",
    ["guardrail_id", "result"],  # pass, fail
)

guardrail_violations_total = Counter(
    "afl_guardrail_violations_total",
    "Total number of guardrail violations",
    ["guardrail_id", "action"],  # block, flag, modify
)

# ============================================
# API Metrics
# ============================================

api_request_total = Counter(
    "afl_api_request_total",
    "Total number of API requests",
    ["method", "endpoint", "status_code"],
)

api_request_duration = Histogram(
    "afl_api_request_duration_seconds",
    "API request duration",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

# ============================================
# Integration Metrics
# ============================================

integration_request_total = Counter(
    "afl_integration_request_total",
    "Total number of integration requests",
    ["integration", "status"],
)

integration_request_duration = Histogram(
    "afl_integration_request_duration_seconds",
    "Integration request duration",
    ["integration"],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60],
)

integration_circuit_breaker = Gauge(
    "afl_integration_circuit_breaker",
    "Circuit breaker state for integrations",
    ["integration"],
)

# ============================================
# Queue Metrics
# ============================================

queue_length = Gauge(
    "afl_queue_length",
    "Current queue length",
    ["queue_name"],
)

queue_processing_time = Histogram(
    "afl_queue_processing_time_seconds",
    "Time spent processing queue items",
    ["queue_name"],
    buckets=[0.1, 0.5, 1, 5, 10, 30],
)

# ============================================
# System Metrics
# ============================================

error_rate = Gauge(
    "afl_error_rate",
    "Current error rate (errors per minute)",
    ["component"],
)

uptime_seconds = Gauge(
    "afl_uptime_seconds",
    "Application uptime in seconds",
)


def metrics_endpoint():
    """Generate Prometheus metrics response."""
    return generate_latest(), CONTENT_TYPE_LATEST
