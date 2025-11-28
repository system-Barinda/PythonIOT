# Windows Setup Script for OkCupid Automation (Python)
# Run this script in PowerShell: .\setup\windows.ps1

Write-Host "=== OkCupid Automation - Windows Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Check Python version
$pythonVersionOutput = python --version 2>&1
if ($pythonVersionOutput -match "Python (\d+)\.(\d+)") {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "✗ Python 3.8+ is required!" -ForegroundColor Red
        exit 1
    }
}

# Check if pip is installed
Write-Host "Checking pip installation..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version
    Write-Host "✓ pip found" -ForegroundColor Green
} catch {
    Write-Host "✗ pip is not installed!" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
Write-Host ""
Write-Host "Setting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path venv)) {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install Playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install Playwright browsers" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "✓ .env file created from .env.example" -ForegroundColor Green
        Write-Host "⚠ Please update .env file with your settings!" -ForegroundColor Yellow
    } else {
        @"
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
"@ | Out-File -FilePath .env -Encoding UTF8
        Write-Host "✓ .env file created" -ForegroundColor Green
        Write-Host "⚠ Please update DATABASE_URL in .env file!" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Make sure PostgreSQL is running" -ForegroundColor White
Write-Host "2. Update .env file with your PostgreSQL connection string" -ForegroundColor White
Write-Host "3. Activate virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "4. Run: python src/main.py" -ForegroundColor White

