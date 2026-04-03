#!/bin/bash
# AFL Orchestrator - Development Environment Setup Script
# This script sets up the git repository with all necessary hooks and configurations

set -e

echo "🚀 AFL Orchestrator - Setting up Git repository..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" != "3.11" ]] && [[ "$PYTHON_VERSION" != "3.12" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Python 3.11 or 3.12 is recommended (found: $PYTHON_VERSION)${NC}"
fi

# Remove old venv if it exists but is broken
if [ -d ".venv" ] && [ ! -f ".venv/bin/activate" ]; then
    echo "🗑️  Removing broken virtual environment..."
    rm -rf .venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install pre-commit
echo ""
echo "📦 Installing pre-commit..."
pip install pre-commit

# Install pre-commit hooks
echo ""
echo "🔧 Installing Git hooks..."
pre-commit install
echo -e "${GREEN}✅ Pre-commit hooks installed${NC}"

# Install pre-commit hooks for all repositories (optional)
echo ""
read -p "Install pre-commit hooks globally for all repositories? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pre-commit install --install-hooks
    echo -e "${GREEN}✅ Global pre-commit hooks installed${NC}"
fi

# Initialize .secrets.baseline if detect-secrets is available
echo ""
echo "🔒 Scanning for existing secrets..."
if ! [ -f ".secrets.baseline" ]; then
    pip install detect-secrets
    detect-secrets scan --baseline .secrets.baseline || true
    echo -e "${GREEN}✅ Secrets baseline created${NC}"
else
    echo -e "${GREEN}✅ Secrets baseline already exists${NC}"
fi

# Check Git configuration
echo ""
echo "📋 Checking Git configuration..."

if ! git config user.name &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git user.name not configured${NC}"
    read -p "Enter your Git username: " git_username
    git config --global user.name "$git_username"
fi

if ! git config user.email &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git user.email not configured${NC}"
    read -p "Enter your Git email: " git_email
    git config --global user.email "$git_email"
fi

echo -e "${GREEN}✅ Git configured: $(git config user.name) <$(git config user.email)>${NC}"

# Set default branch to develop
echo ""
echo "🌿 Setting default branch to 'develop'..."
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/develop 2>/dev/null || true
echo -e "${GREEN}✅ Default branch configured${NC}"

# Create initial branches if they don't exist
echo ""
if ! git show-ref --verify --quiet refs/heads/main; then
    echo "📋 Creating main branch..."
    git checkout -b main
    git commit --allow-empty -m "Initial commit on main"
    echo -e "${GREEN}✅ Main branch created${NC}"
fi

if ! git show-ref --verify --quiet refs/heads/develop; then
    echo "📋 Creating develop branch..."
    git checkout -b develop
    git commit --allow-empty -m "Initial commit on develop"
    echo -e "${GREEN}✅ Develop branch created${NC}"
fi

# Show branch structure
echo ""
echo "🌳 Current branch structure:"
git branch -a

# Install development dependencies
echo ""
echo "📦 Installing development dependencies..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    echo -e "${GREEN}✅ Development dependencies installed${NC}"
else
    # Install common dev tools
    pip install \
        pytest \
        pytest-cov \
        pytest-asyncio \
        black \
        isort \
        ruff \
        mypy \
        bandit \
        sqlfluff
    echo -e "${GREEN}✅ Common development tools installed${NC}"
fi

# Run initial pre-commit on all files
echo ""
echo "🔍 Running initial pre-commit checks..."
pre-commit run --all-files || true

# Summary
echo ""
echo "=================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Create feature branch: git checkout -b feature/YOUR-TICKET-description"
echo "  3. Start coding!"
echo ""
echo "Useful commands:"
echo "  - Run all pre-commit hooks: pre-commit run --all-files"
echo "  - Run tests: pytest"
echo "  - Run linting: ruff check src/"
echo "  - Run type checking: mypy src/"
echo ""
echo "Documentation:"
echo "  - Git Flow: See GIT_FLOW.md"
echo "  - Pre-commit: https://pre-commit.com"
echo ""
