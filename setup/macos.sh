#!/bin/bash
# macOS Setup Script for OkCupid Automation (Python)
# Run: chmod +x setup/macos.sh && ./setup/macos.sh

echo "=== OkCupid Automation - macOS Setup ==="
echo ""

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✓ Python found: $PYTHON_VERSION"
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo "✗ Python is not installed!"
    echo "Install using Homebrew: brew install python3"
    echo "Or download from: https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "✗ Python 3.8+ is required!"
    exit 1
fi

# Check if pip is installed
echo "Checking pip installation..."
if ! command -v $PIP_CMD &> /dev/null; then
    echo "✗ pip is not installed!"
    exit 1
fi
echo "✓ pip found"

# Create virtual environment if it doesn't exist
echo ""
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
$PIP_CMD install --upgrade pip
$PIP_CMD install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "✗ Failed to install Playwright browsers"
    exit 1
fi

# Create .env file if it doesn't exist
echo ""
echo "Checking .env file..."
if [ ! -f .env ]; then
    echo "Creating .env file..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ .env file created from .env.example"
        echo "⚠ Please update .env file with your settings!"
    else
        cat > .env << EOF
# NST Browser
NST_BROWSER_URL=ws://localhost:3000

# WebSocket Endpoints
PROFILE_DATA_WS_URL=ws://localhost:8001
CONSUMING_APPS_WS_URL=ws://localhost:8002
STATE_TRANSFER_WS_URL=ws://localhost:8003

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/okcupid

# Development
DEV_MODE=false
EOF
        echo "✓ .env file created"
        echo "⚠ Please update DATABASE_URL in .env file!"
    fi
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Make sure PostgreSQL is running (brew services start postgresql)"
echo "2. Update .env file with your PostgreSQL connection string"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Run: python src/main.py"
