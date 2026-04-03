"""Seed data for development environment."""

import asyncio
import random
from datetime import datetime, timezone

from src.orchestrator.config import settings
from src.orchestrator.observability.logging_config import get_logger

logger = get_logger("seed")


async def seed_users():
    """Create test users."""
    logger.info("Seeding users...")
    users = [
        {"email": "admin@example.com", "name": "Admin User", "role": "admin"},
        {"email": "developer@example.com", "name": "Developer User", "role": "developer"},
        {"email": "viewer@example.com", "name": "Viewer User", "role": "viewer"},
    ]
    logger.info(f"Created {len(users)} test users")
    return users


async def seed_projects(users: list[dict]):
    """Create test projects."""
    logger.info("Seeding projects...")
    projects = [
        {
            "name": "Code Review Automation",
            "description": "Automated code review for repositories",
            "owner_id": users[0]["id"],
            "budget": {"total_tokens": 100000, "warning_threshold": 0.8},
        },
        {
            "name": "Data Analysis Pipeline",
            "description": "ETL pipeline with AI analysis",
            "owner_id": users[1]["id"],
            "budget": {"total_tokens": 50000, "warning_threshold": 0.75},
        },
        {
            "name": "Content Generation",
            "description": "Automated content creation workflow",
            "owner_id": users[1]["id"],
            "budget": {"total_tokens": 200000, "warning_threshold": 0.85},
        },
    ]
    logger.info(f"Created {len(projects)} test projects")
    return projects


async def seed_configs(projects: list[dict]):
    """Create test AFL configs."""
    logger.info("Seeding configs...")
    configs = []
    for project in projects:
        config = {
            "project_id": project["id"],
            "version": "1.0.0",
            "content": f"""
version: "1.0"
project: "{project['name']}"
budget:
  total_tokens: {project['budget']['total_tokens']}
  warning_threshold: {project['budget']['warning_threshold']}
agents:
  - id: "agent_1"
    type: "llm"
    model: "gpt-4"
workflow:
  - step: "step_1"
    agent: "agent_1"
""",
            "format": "yaml",
        }
        configs.append(config)
    logger.info(f"Created {len(configs)} test configs")
    return configs


async def seed_workflows(projects: list[dict], configs: list[dict]):
    """Create test workflows."""
    logger.info("Seeding workflows...")
    statuses = ["completed", "completed", "completed", "running", "failed"]
    workflows = []
    for i in range(20):
        project = random.choice(projects)
        config = random.choice(configs)
        status = random.choice(statuses)
        workflow = {
            "project_id": project["id"],
            "config_version_id": config["id"],
            "status": status,
            "priority": random.choice(["low", "normal", "high"]),
            "tokens_used": random.randint(1000, 50000),
            "cost_usd": round(random.uniform(0.01, 5.0), 4),
        }
        workflows.append(workflow)
    logger.info(f"Created {len(workflows)} test workflows")
    return workflows


async def seed_agents():
    """Create test agents."""
    logger.info("Seeding agents...")
    agents = [
        {
            "name": "code_analyzer_1",
            "type": "llm",
            "model": "gpt-4",
            "status": "idle",
        },
        {
            "name": "review_writer_1",
            "type": "llm",
            "model": "claude-3-opus",
            "status": "idle",
        },
        {
            "name": "data_processor_1",
            "type": "llm",
            "model": "gpt-3.5-turbo",
            "status": "busy",
        },
    ]
    logger.info(f"Created {len(agents)} test agents")
    return agents


async def run_seed():
    """Run all seed operations."""
    logger.info("=" * 50)
    logger.info("Starting database seeding...")
    logger.info("=" * 50)

    # Run seeding
    users = await seed_users()
    projects = await seed_projects(users)
    configs = await seed_configs(projects)
    workflows = await seed_workflows(projects, configs)
    agents = await seed_agents()

    logger.info("=" * 50)
    logger.info("Seeding completed!")
    logger.info(f"  Users: {len(users)}")
    logger.info(f"  Projects: {len(projects)}")
    logger.info(f"  Configs: {len(configs)}")
    logger.info(f"  Workflows: {len(workflows)}")
    logger.info(f"  Agents: {len(agents)}")
    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(run_seed())
