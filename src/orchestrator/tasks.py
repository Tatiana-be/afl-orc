# mypy: ignore-errors
"""Celery task definitions."""

from celery import Celery

from src.orchestrator.config import settings

celery_app = Celery(
    "afl_orchestrator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3)
def execute_agent_task(self, agent_id: str, context: dict) -> dict:
    """Execute an agent task."""
    # TODO: Implement agent execution
    return {"status": "completed"}


@celery_app.task(bind=True, max_retries=3)
def check_guardrail_task(self, content: str, guardrail_id: str) -> dict:
    """Run a guardrail check."""
    # TODO: Implement guardrail check
    return {"passed": True}
