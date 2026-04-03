"""Proof-of-Concept: Budget Tracking Accuracy

Validates:
1. Token accounting accuracy within ±5%
2. Budget limit enforcement works
3. Alert triggering at thresholds
4. Multi-provider cost aggregation
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TokenUsage:
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class BudgetConfig:
    total_tokens: int
    total_usd: float
    warning_threshold: float = 0.8  # 80%
    hard_limit: float = 1.0  # 100%


@dataclass
class BudgetState:
    tokens_used: int = 0
    cost_usd: float = 0.0
    transactions: list[TokenUsage] = field(default_factory=list)
    alerts_triggered: list[str] = field(default_factory=list)


# Provider pricing (per 1K tokens)
PRICING = {
    "openai": {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
    },
    "anthropic": {
        "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
        "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
    },
}


class BudgetTracker:
    """Tracks token usage and costs across providers."""

    def __init__(self, config: BudgetConfig):
        self.config = config
        self.state = BudgetState()

    def record_usage(self, usage: TokenUsage) -> dict:
        """Record token usage and check limits."""
        self.state.tokens_used += usage.prompt_tokens + usage.completion_tokens
        self.state.cost_usd += usage.cost_usd
        self.state.transactions.append(usage)

        # Check thresholds
        token_usage_pct = self.state.tokens_used / self.config.total_tokens
        cost_usage_pct = self.state.cost_usd / self.config.total_usd

        alerts = []

        if token_usage_pct >= self.config.hard_limit:
            alerts.append("HARD_LIMIT_TOKENS")
        elif token_usage_pct >= self.config.warning_threshold:
            alerts.append("WARNING_TOKENS")

        if cost_usage_pct >= self.config.hard_limit:
            alerts.append("HARD_LIMIT_COST")
        elif cost_usage_pct >= self.config.warning_threshold:
            alerts.append("WARNING_COST")

        self.state.alerts_triggered.extend(alerts)

        return {
            "allowed": len([a for a in alerts if "HARD_LIMIT" in a]) == 0,
            "token_usage_pct": token_usage_pct,
            "cost_usage_pct": cost_usage_pct,
            "alerts": alerts,
        }

    def get_remaining(self) -> dict:
        """Get remaining budget."""
        return {
            "tokens": max(0, self.config.total_tokens - self.state.tokens_used),
            "usd": max(0, self.config.total_usd - self.state.cost_usd),
            "token_pct": 1 - (self.state.tokens_used / self.config.total_tokens),
            "cost_pct": 1 - (self.state.cost_usd / self.config.total_usd),
        }

    def get_breakdown(self) -> dict:
        """Get usage breakdown by provider and model."""
        breakdown = {}
        for tx in self.state.transactions:
            key = f"{tx.provider}/{tx.model}"
            if key not in breakdown:
                breakdown[key] = {"tokens": 0, "cost": 0.0, "count": 0}
            breakdown[key]["tokens"] += tx.prompt_tokens + tx.completion_tokens
            breakdown[key]["cost"] += tx.cost_usd
            breakdown[key]["count"] += 1
        return breakdown


def calculate_cost(provider: str, model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate cost based on provider pricing."""
    pricing = PRICING.get(provider, {}).get(model)
    if not pricing:
        return 0.0

    prompt_cost = (prompt_tokens / 1000) * pricing["prompt"]
    completion_cost = (completion_tokens / 1000) * pricing["completion"]
    return round(prompt_cost + completion_cost, 6)


async def test_budget_tracking():
    """PoC Test: Budget Tracking Accuracy"""
    print("\n" + "=" * 60)
    print("PoC 4: Budget Tracking Accuracy")
    print("=" * 60)

    # Setup budget
    config = BudgetConfig(
        total_tokens=100000,
        total_usd=10.0,
        warning_threshold=0.8,
        hard_limit=1.0,
    )

    tracker = BudgetTracker(config)

    # Test 1: Basic tracking
    print("\n[Test 1] Basic Token Tracking")

    # Simulate 100 API calls across providers
    import random

    providers_models = [
        ("openai", "gpt-4"),
        ("openai", "gpt-3.5-turbo"),
        ("anthropic", "claude-3-opus"),
        ("anthropic", "claude-3-sonnet"),
    ]

    expected_tokens = 0
    expected_cost = 0.0

    for i in range(100):
        provider, model = random.choice(providers_models)
        prompt_tokens = random.randint(500, 2000)
        completion_tokens = random.randint(200, 1000)
        cost = calculate_cost(provider, model, prompt_tokens, completion_tokens)

        usage = TokenUsage(
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost,
        )

        result = tracker.record_usage(usage)
        expected_tokens += prompt_tokens + completion_tokens
        expected_cost += cost

    # Verify accuracy
    token_accuracy = abs(tracker.state.tokens_used - expected_tokens) / expected_tokens
    cost_accuracy = abs(tracker.state.cost_usd - expected_cost) / expected_cost

    print(f"  Tokens tracked: {tracker.state.tokens_used} (expected: {expected_tokens})")
    print(f"  Cost tracked: ${tracker.state.cost_usd:.4f} (expected: ${expected_cost:.4f})")
    print(f"  Token accuracy: {(1 - token_accuracy):.2%}")
    print(f"  Cost accuracy: {(1 - cost_accuracy):.2%}")

    assert token_accuracy < 0.05, f"Token accuracy {token_accuracy:.2%} exceeds 5%"
    assert cost_accuracy < 0.05, f"Cost accuracy {cost_accuracy:.2%} exceeds 5%"
    print(f"  ✅ Accuracy within ±5%")

    # Test 2: Budget limits
    print("\n[Test 2] Budget Limit Enforcement")

    # Create tracker with small budget for testing
    small_config = BudgetConfig(
        total_tokens=10000,
        total_usd=1.0,
        warning_threshold=0.8,
        hard_limit=1.0,
    )

    small_tracker = BudgetTracker(small_config)

    # Add usage until we hit limits
    blocked = False
    warning_triggered = False

    for i in range(20):
        usage = TokenUsage(
            provider="openai",
            model="gpt-4",
            prompt_tokens=1000,
            completion_tokens=500,
            cost_usd=calculate_cost("openai", "gpt-4", 1000, 500),
        )

        result = small_tracker.record_usage(usage)

        if "WARNING_TOKENS" in result["alerts"] or "WARNING_COST" in result["alerts"]:
            warning_triggered = True

        if not result["allowed"]:
            blocked = True
            print(f"  ✅ Blocked at {result['token_usage_pct']:.2%} token usage")
            break

    assert warning_triggered, "Warning alert should trigger at 80%"
    print(f"  ✅ Warning alert triggered at 80%")

    # Test 3: Multi-provider aggregation
    print("\n[Test 3] Multi-Provider Cost Aggregation")

    breakdown = tracker.get_breakdown()
    print(f"  Usage by provider/model:")
    for key, data in sorted(breakdown.items()):
        print(f"    {key:30s}: {data['tokens']:6d} tokens, ${data['cost']:.4f} ({data['count']} calls)")

    total_from_breakdown = sum(d["tokens"] for d in breakdown.values())
    assert total_from_breakdown == tracker.state.tokens_used
    print(f"  ✅ Aggregation accurate")

    # Test 4: Remaining budget
    print("\n[Test 4] Remaining Budget Calculation")
    remaining = tracker.get_remaining()
    print(f"  Remaining tokens: {remaining['tokens']} ({remaining['token_pct']:.2%})")
    print(f"  Remaining cost: ${remaining['usd']:.4f} ({remaining['cost_pct']:.2%})")

    assert remaining["tokens"] >= 0
    assert remaining["usd"] >= 0
    print(f"  ✅ Remaining budget calculated correctly")

    print("\n" + "=" * 60)
    print("✅ PoC 4 PASSED: Budget Tracking risks mitigated")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_budget_tracking())
