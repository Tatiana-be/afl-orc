"""Unit tests for storage layer."""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.orm import DeclarativeBase

from src.orchestrator.storage.models import Base


class TestBaseModel:
    """Tests for SQLAlchemy Base model."""

    def test_base_inherits_declarative_base(self):
        """Test Base inherits from DeclarativeBase."""
        assert issubclass(Base, DeclarativeBase)

    def test_base_is_abstract(self):
        """Test Base can be used as base for models."""
        # Base should be usable for model inheritance
        assert hasattr(Base, "metadata")


class TestDatabase:
    """Tests for database connection."""

    def test_database_module_import(self):
        """Test database module can be imported."""
        import src.orchestrator.storage.database as db_module

        assert hasattr(db_module, "engine")
        assert hasattr(db_module, "async_session")

    def test_get_db_function_exists(self):
        """Test get_db async generator exists."""
        from src.orchestrator.storage.database import get_db

        assert callable(get_db)

    @pytest.mark.asyncio
    async def test_get_db_yields_session(self):
        """Test get_db generator yields session."""
        from src.orchestrator.storage.database import get_db

        # Mock the session
        mock_session = AsyncMock()
        with patch("src.orchestrator.storage.database.async_session") as mock_sessionmaker:
            mock_sessionmaker.return_value.__aenter__.return_value = mock_session

            # Get the generator
            gen = get_db()
            session = await gen.__anext__()

            # Should yield the session
            assert session is not None
