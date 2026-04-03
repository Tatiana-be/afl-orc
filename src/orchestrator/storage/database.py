"""Database connection and session management."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.orchestrator.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    """Get database session."""
    async with async_session() as session:
        yield session
