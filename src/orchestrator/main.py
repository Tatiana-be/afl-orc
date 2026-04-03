# mypy: ignore-errors
"""AFL Orchestrator - Main Application Entry Point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.orchestrator.api.routes import router as api_router
from src.orchestrator.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting AFL Orchestrator v{settings.VERSION}")
    yield
    # Shutdown
    print("Shutting down AFL Orchestrator")


app = FastAPI(
    title="AFL Orchestrator",
    description="AI-пайплайны оркестрации мульти-агентных рабочих процессов",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AFL Orchestrator",
        "version": settings.VERSION,
        "docs": "/docs",
    }
