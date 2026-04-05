"""AFL Config schema definitions."""

from pydantic import BaseModel, Field

# Latest schema version
SCHEMA_VERSION = "1.0"

# Supported schema versions and their descriptions
SCHEMA_VERSIONS: dict[str, str] = {
    "1.0": "Initial schema version",
}


class BudgetConfig(BaseModel):
    """Budget configuration."""

    total_tokens: int = Field(..., gt=0)
    warning_threshold: float = Field(0.8, ge=0, le=1)
    hard_limit: int | None = None


class AgentConfig(BaseModel):
    """Agent configuration."""

    id: str
    type: str
    model: str | None = None
    tools: list[str] = []
    guardrails: list[str] = []


class ArtifactConfig(BaseModel):
    """Artifact configuration."""

    id: str
    type: str
    url: str | None = None
    path: str | None = None


class GuardrailConfig(BaseModel):
    """Guardrail configuration."""

    id: str
    type: str
    action: str = "block"


class WorkflowStep(BaseModel):
    """Workflow step configuration."""

    step: str
    agent: str
    depends_on: list[str] = []
    artifact: str | None = None


class AFLConfig(BaseModel):
    """Main AFL configuration schema."""

    version: str = Field(..., pattern=r"^\d+\.\d+$")
    project: str
    budget: BudgetConfig | None = None
    agents: list[AgentConfig] = []
    artifacts: list[ArtifactConfig] = []
    guardrails: list[GuardrailConfig] = []
    workflow: list[WorkflowStep] = []
