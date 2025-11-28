# ⚡ Quick Start - Run Project Now!

## Fastest Way to Get Started

### Option 1: Automated Setup (Recommended)

Just run this command in PowerShell:

```powershell
.\setup\windows.ps1
```

This will set up everything automatically!

### Option 2: Manual Setup

If the script doesn't work, follow these steps:

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Install Playwright browser
playwright install chromium

# 5. Create .env file (copy from below)
```

## Create .env File

Create a file named `.env` in the project root with this content:

```env
# NST Browser (optional)
NST_BROWSER_URL=ws://localhost:3000

# WebSocket Endpoints
PROFILE_DATA_WS_URL=ws://localhost:8001
CONSUMING_APPS_WS_URL=ws://localhost:8002
STATE_TRANSFER_WS_URL=ws://localhost:8003

# Database (UPDATE with your PostgreSQL credentials!)
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/okcupid

# Development Mode (set to true to see browser)
DEV_MODE=true
```

## Run the Project

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Test with demo
python quick_demo/hello_world_demo.py

# Run main application
python src/main.py
```

## That's It! 🎉

For detailed instructions, see `LOCAL_SETUP_GUIDE.md`

