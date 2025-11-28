# 🚀 Local Setup Guide - OkCupid Automation

Complete guide to run the project on your local Windows machine.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.8 or higher** - [Download here](https://www.python.org/downloads/)
2. **PostgreSQL** (optional for basic testing, required for full functionality)
3. **PowerShell** (comes with Windows)

## Step-by-Step Setup

### Step 1: Verify Python Installation

Open PowerShell and check your Python version:

```powershell
python --version
```

If Python is not installed or version is below 3.8, install/upgrade it first.

### Step 2: Run the Setup Script

Navigate to the project directory and run the Windows setup script:

```powershell
cd "C:\Users\TFB\OneDrive\Desktop\ALL NOTES\large network admnistrator\flerencer"
.\setup\windows.ps1
```

This script will:
- ✅ Check Python installation
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Install Playwright browsers
- ✅ Create `.env` file

### Step 3: Configure Environment Variables

After setup, edit the `.env` file in the project root:

```env
# NST Browser (optional - leave as is if not using NST Browser)
NST_BROWSER_URL=ws://localhost:3000

# WebSocket Endpoints (leave as default)
PROFILE_DATA_WS_URL=ws://localhost:8001
CONSUMING_APPS_WS_URL=ws://localhost:8002
STATE_TRANSFER_WS_URL=ws://localhost:8003

# Database (UPDATE THIS!)
DATABASE_URL=postgresql://username:password@localhost:5432/okcupid

# Development Mode (set to true to see browser)
DEV_MODE=true
```

**Important:** Update `DATABASE_URL` with your PostgreSQL credentials:
- `username`: Your PostgreSQL username
- `password`: Your PostgreSQL password
- `localhost:5432`: Default PostgreSQL location
- `okcupid`: Database name (create it first if it doesn't exist)

### Step 4: Set Up PostgreSQL (Optional for Testing)

If you don't have PostgreSQL:

1. **Download PostgreSQL**: [Download here](https://www.postgresql.org/download/windows/)
2. **Install PostgreSQL** with default settings
3. **Create the database**:
   ```sql
   CREATE DATABASE okcupid;
   ```

Or use **pgAdmin** (GUI tool that comes with PostgreSQL) to create the database.

**Note:** For basic testing without database, you can modify the code to skip database operations, but full functionality requires PostgreSQL.

### Step 5: Activate Virtual Environment

Every time you want to run the project, activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your prompt.

### Step 6: Test the Connection

Test the browser automation with the demo script:

```powershell
python quick_demo/hello_world_demo.py
```

This will:
- Try to connect to NST Browser (if running)
- Fall back to local browser if NST is not available
- Open Google and type "Hello world"
- If `DEV_MODE=true`, you'll see the browser window

### Step 7: Run the Main Application

```powershell
python src/main.py
```

This will:
- Connect to the database
- Start WebSocket servers
- Initialize the browser
- Keep running until you stop it (Ctrl+C)

## Troubleshooting

### Issue: "Python is not recognized"

**Solution:** 
- Make sure Python is added to PATH during installation
- Or use full path: `C:\Python3x\python.exe`

### Issue: "Execution Policy Error" in PowerShell

**Solution:** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Cannot connect to database"

**Solutions:**
- Make sure PostgreSQL is running
- Check your `.env` file has correct credentials
- Verify database `okcupid` exists
- Test connection: `psql -U username -d okcupid`

### Issue: "Playwright browsers not found"

**Solution:** 
```powershell
playwright install chromium
```

### Issue: "Port already in use" (WebSocket servers)

**Solution:** 
- Change ports in `.env` file
- Or stop other applications using ports 8001, 8002, 8003

### Issue: "NST Browser connection failed"

**Solution:** 
- This is normal if NST Browser is not running
- The app will automatically use local browser instead
- To use NST Browser, start it first (requires Docker)

## Quick Commands Reference

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run demo
python quick_demo/hello_world_demo.py

# Run main application
python src/main.py

# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Deactivate virtual environment
deactivate
```

## Development Mode

Set `DEV_MODE=true` in `.env` to:
- See the browser window (not headless)
- Debug automation issues
- Watch what's happening

## Next Steps

1. ✅ Setup complete - you can now run the project
2. 📝 Read `README.md` for developer guides
3. 🔧 Customize selectors in each developer section
4. 🚀 Start developing your automation features

## Need Help?

- Check `README.md` for detailed documentation
- Review `VERIFICATION_REPORT.md` for project status
- Check `ERRORS_FIXED.md` for recent fixes

---

**Happy Coding! 🎉**

