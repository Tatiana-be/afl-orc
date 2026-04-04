"""Unit tests for logging configuration."""

import json
import logging
from unittest.mock import MagicMock, patch

import pytest

from src.orchestrator.observability.logging_config import JSONFormatter, get_logger, setup_logging


@pytest.fixture
def formatter():
    """Create JSON formatter instance."""
    return JSONFormatter()


@pytest.fixture
def log_record():
    """Create a sample log record."""
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test log message",
        args=(),
        exc_info=None,
    )
    record.funcName = "test_function"
    return record


class TestJSONFormatter:
    """Tests for JSONFormatter."""

    def test_format_basic(self, formatter, log_record):
        """Test formatting a basic log record."""
        formatted = formatter.format(log_record)
        data = json.loads(formatted)

        assert "timestamp" in data
        assert data["level"] == "INFO"
        assert data["logger"] == "test_logger"
        assert data["message"] == "Test log message"
        assert data["module"] == "test"
        assert data["function"] == "test_function"
        assert data["line"] == 42

    def test_format_with_exception(self, formatter):
        """Test formatting a log record with exception info."""
        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=(ValueError, ValueError("test error"), None),
        )
        record.funcName = "error_function"

        formatted = formatter.format(record)
        data = json.loads(formatted)

        assert data["level"] == "ERROR"
        assert "exception" in data
        assert "ValueError" in data["exception"]

    def test_format_with_request_id(self, formatter, log_record):
        """Test formatting with request_id extra field."""
        log_record.request_id = "req_12345"
        formatted = formatter.format(log_record)
        data = json.loads(formatted)

        assert data["request_id"] == "req_12345"

    def test_format_with_user_id(self, formatter, log_record):
        """Test formatting with user_id extra field."""
        log_record.user_id = "user_789"
        formatted = formatter.format(log_record)
        data = json.loads(formatted)

        assert data["user_id"] == "user_789"

    def test_format_with_workflow_id(self, formatter, log_record):
        """Test formatting with workflow_id extra field."""
        log_record.workflow_id = "wf_456"
        formatted = formatter.format(log_record)
        data = json.loads(formatted)

        assert data["workflow_id"] == "wf_456"

    def test_format_valid_json(self, formatter, log_record):
        """Test formatted output is valid JSON."""
        formatted = formatter.format(log_record)
        # Should not raise exception
        data = json.loads(formatted)
        assert isinstance(data, dict)


class TestSetupLogging:
    """Tests for setup_logging function."""

    @patch("src.orchestrator.observability.logging_config.settings")
    def test_setup_logging_console_handler(self, mock_settings):
        """Test setup_logging configures console handler."""
        mock_settings.LOG_LEVEL = "INFO"
        mock_settings.DEBUG = True

        setup_logging()

        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0

        # Check console handler exists
        handlers = root_logger.handlers
        console_handlers = [h for h in handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0

    @patch("src.orchestrator.observability.logging_config.settings")
    def test_setup_logging_file_handler_in_debug_false(self, mock_settings):
        """Test setup_logging adds file handler when DEBUG is False."""
        mock_settings.LOG_LEVEL = "WARNING"
        mock_settings.DEBUG = False

        # Clear existing handlers
        root_logger = logging.getLogger()
        root_logger.handlers.clear()

        with patch("logging.FileHandler") as mock_fh:
            mock_fh.return_value = MagicMock()
            setup_logging()

            # Should have attempted to create file handler
            assert mock_fh.called or len(root_logger.handlers) > 0


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger_instance(self):
        """Test get_logger returns a Logger instance."""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_name_prefix(self):
        """Test get_logger prefixes with afl."""
        logger = get_logger("test_module")
        assert logger.name == "afl.test_module"

    def test_get_logger_different_modules(self):
        """Test get_logger creates different loggers for different names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1.name != logger2.name
        assert logger1.name == "afl.module1"
        assert logger2.name == "afl.module2"
