# 🚀 How to Run the Project

## ✅ Setup Complete!

Your project is ready to run. Here's what's been set up:

- ✅ Virtual environment created
- ✅ All main dependencies installed
- ✅ Playwright Chromium browser installed
- ⚠️ asyncpg skipped (optional - requires C++ Build Tools)

## Quick Start

### 1. Activate Virtual Environment

Open PowerShell in the project directory and run:

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your prompt.

### 2. Create .env File

Create a file named `.env` in the project root with this content:

```env
# NST Browser (optional - leave as is)
NST_BROWSER_URL=ws://localhost:3000

# WebSocket Endpoints (leave as default)
PROFILE_DATA_WS_URL=ws://localhost:8001
CONSUMING_APPS_WS_URL=ws://localhost:8002
STATE_TRANSFER_WS_URL=ws://localhost:8003

# Database (UPDATE THIS with your PostgreSQL credentials!)
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/okcupid

# Development Mode (set to true to see browser)
DEV_MODE=true
```

**Important:** Replace `postgres:yourpassword` with your actual PostgreSQL username and password.

### 3. Test the Setup

Run the demo to test browser automation:

```powershell
python quick_demo/hello_world_demo.py
```

This will:
- Open a browser (you'll see it if `DEV_MODE=true`)
- Navigate to Google
- Type "Hello world"
- Close after a few seconds

### 4. Run the Main Application

```powershell
python src/main.py
```

This will:
- Connect to database (if configured)
- Start WebSocket servers on ports 8001, 8002, 8003
- Initialize browser automation
- Keep running until you press Ctrl+C

## Troubleshooting

### Database Connection Issues

If you don't have PostgreSQL set up yet:

1. **Install PostgreSQL**: Download from https://www.postgresql.org/download/windows/
2. **Create database**: 
   ```sql
   CREATE DATABASE okcupid;
   ```
3. **Update .env**: Set correct username/password in `DATABASE_URL`

### Port Already in Use

If you see "port already in use" errors:
- Change ports in `.env` file
- Or stop other applications using ports 8001-8003

### Can't See Browser

Set `DEV_MODE=true` in `.env` to see the browser window.

## Next Steps

1. ✅ Project is ready to run
2. 📝 Read `LOCAL_SETUP_GUIDE.md` for detailed instructions
3. 🔧 Start customizing the automation code
4. 🚀 Begin development!

---

**You're all set! Happy coding! 🎉**

