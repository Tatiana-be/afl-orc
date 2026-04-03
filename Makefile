.PHONY: help install dev test lint format migrate docker-up docker-down clean

# Default target
help:
	@echo "AFL Orchestrator - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install       Install all dependencies"
	@echo "  dev           Start development environment"
	@echo ""
	@echo "Testing:"
	@echo "  test          Run all tests"
	@echo "  test-unit     Run unit tests"
	@echo "  test-integration  Run integration tests"
	@echo "  test-cov      Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint          Run all linters"
	@echo "  format        Format code with black and isort"
	@echo "  check         Check code formatting"
	@echo "  pre-commit    Run pre-commit hooks"
	@echo ""
	@echo "Database:"
	@echo "  migrate       Run database migrations"
	@echo "  migrate-make  Create new migration"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up     Start all services"
	@echo "  docker-down   Stop all services"
	@echo "  docker-logs   View service logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean         Remove generated files"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Start development server
dev:
	uvicorn src.orchestrator.main:app --reload --host 0.0.0.0 --port 8000

# Run all tests
test:
	pytest tests/ -v

# Run unit tests
test-unit:
	pytest tests/unit/ -v

# Run integration tests
test-integration:
	pytest tests/integration/ -v

# Run tests with coverage
test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Run all linters
lint:
	ruff check src/ tests/
	mypy src/
	bandit -r src/ -ll

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Check code formatting
check:
	black --check src/ tests/
	isort --check src/ tests/
	ruff check src/ tests/

# Run pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Run database migrations
migrate:
	alembic upgrade head

# Create new migration
migrate-make:
	@read -p "Migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# Start Docker services
docker-up:
	docker-compose up -d

# Stop Docker services
docker-down:
	docker-compose down

# View Docker logs
docker-logs:
	docker-compose logs -f orchestrator

# Clean generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
