"""Unit tests for stub services."""

import pytest

from src.orchestrator.services.budget_tracker import BudgetTracker
from src.orchestrator.services.context_manager import ContextManager
from src.orchestrator.services.guardrail_engine import GuardrailEngine

# ============================================
# Budget Tracker Tests
# ============================================


class TestBudgetTracker:
    """Tests for BudgetTracker service."""

    @pytest.fixture
    def budget_tracker(self):
        """Create budget tracker instance."""
        return BudgetTracker()

    @pytest.mark.asyncio
    async def test_check_budget_allowed(self, budget_tracker):
        """Test budget check returns allowed."""
        result = await budget_tracker.check_budget("proj_123")
        assert result["allowed"] is True
        assert "remaining" in result

    @pytest.mark.asyncio
    async def test_record_usage_success(self, budget_tracker):
        """Test recording usage returns True."""
        result = await budget_tracker.record_usage(
            project_id="proj_123",
            tokens=1000,
            cost=0.50,
        )
        assert result is True


# ============================================
# Context Manager Tests
# ============================================


class TestContextManager:
    """Tests for ContextManager service."""

    @pytest.fixture
    def context_manager(self):
        """Create context manager instance."""
        return ContextManager()

    @pytest.mark.asyncio
    async def test_get_context_returns_dict(self, context_manager):
        """Test get_context returns a dict."""
        result = await context_manager.get_context(
            execution_id="exec_123",
            step_id="step_1",
        )
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_update_context_returns_true(self, context_manager):
        """Test update_context returns True."""
        result = await context_manager.update_context(
            execution_id="exec_123",
            context={"data": "test"},
        )
        assert result is True


# ============================================
# Guardrail Engine Tests
# ============================================


class TestGuardrailEngine:
    """Tests for GuardrailEngine service."""

    @pytest.fixture
    def guardrail_engine(self):
        """Create guardrail engine instance."""
        return GuardrailEngine()

    @pytest.mark.asyncio
    async def test_check_passes_by_default(self, guardrail_engine):
        """Test guardrail check returns passed by default."""
        result = await guardrail_engine.check(
            content="Test content",
            guardrails=[],
        )
        assert result["passed"] is True
        assert result["violations"] == []

    @pytest.mark.asyncio
    async def test_check_with_guardrules(self, guardrail_engine):
        """Test guardrail check with guardrails."""
        guardrails = [
            {"id": "regex_check", "type": "regex", "pattern": ".*"},
        ]
        result = await guardrail_engine.check(
            content="Test content",
            guardrails=guardrails,
        )
        assert "passed" in result
        assert "violations" in result
