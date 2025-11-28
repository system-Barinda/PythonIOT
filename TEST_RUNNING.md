# ✅ Test if Your Application is Running

## Quick Test

### Step 1: Start the Application

Open PowerShell in the project directory:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the application
python src/main.py
```

You should see:
```
🚀 Initializing OkCupid Automation...
✅ Database connected
✅ ProfileDataWebSocketServer started on ws://localhost:8001
✅ ConsumingAppsWebSocketServer started on ws://localhost:8002
✅ StateTransferWebSocketServer started on ws://localhost:8003
✅ Automation system ready
```

### Step 2: Test WebSocket Servers

Open a **new** PowerShell window and run:

```powershell
.\venv\Scripts\Activate.ps1
python test_websocket.py
```

This will test all three WebSocket servers.

### Step 3: Check Ports

In another terminal, check if ports are listening:

```powershell
netstat -an | findstr "8001 8002 8003"
```

You should see:
```
TCP    0.0.0.0:8001    0.0.0.0:0    LISTENING
TCP    0.0.0.0:8002    0.0.0.0:0    LISTENING
TCP    0.0.0.0:8003    0.0.0.0:0    LISTENING
```

## ✅ If Everything Works

Your application is **running well** and ready to host!

## 🚀 Next Steps for Hosting

1. **For Local Testing:** Keep running `python src/main.py`
2. **For Production:** See `HOSTING_GUIDE.md` for deployment options
3. **For VPS:** Follow the VPS deployment guide
4. **For Cloud:** Use Kubernetes configs in `k8s/` folder

## 📝 Notes

- The application runs **WebSocket servers**, not a traditional HTTP web server
- Clients connect via WebSocket protocol (ws://)
- For external access, you'll need to:
  - Open firewall ports (8001, 8002, 8003)
  - Use reverse proxy (Nginx) for SSL/HTTPS
  - Configure domain name (optional)

See `HOSTING_GUIDE.md` for complete hosting instructions!

