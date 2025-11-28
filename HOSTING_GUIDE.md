# 🌐 Hosting Guide - OkCupid Automation

Your application can be hosted on various platforms. Here are the best options:

## ✅ Current Status

Your application runs **WebSocket servers** on:
- **Port 8001** - Profile Data WebSocket
- **Port 8002** - Consuming Apps WebSocket  
- **Port 8003** - State Transfer WebSocket

## 🚀 Hosting Options

### Option 1: Local Machine (Current Setup) ✅

**Best for:** Development and testing

**How to run:**
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run the application
python src/main.py
```

**Access:**
- WebSocket: `ws://localhost:8001`, `ws://localhost:8002`, `ws://localhost:8003`
- Only accessible from your local machine

---

### Option 2: VPS (Virtual Private Server) 🌟 **Recommended**

**Best for:** Production deployment

**Popular Providers:**
- **DigitalOcean** - $6/month (1GB RAM)
- **Linode** - $5/month
- **Vultr** - $6/month
- **AWS EC2** - Pay as you go
- **Google Cloud Compute** - Pay as you go

**Setup Steps:**

1. **Get a VPS** (Ubuntu 20.04+ recommended)

2. **SSH into your server:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install dependencies:**
   ```bash
   apt update
   apt install python3 python3-pip python3-venv postgresql git
   ```

4. **Clone and setup:**
   ```bash
   git clone your-repo-url
   cd flerencer
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install chromium
   ```

5. **Configure .env:**
   ```env
   NST_BROWSER_URL=ws://localhost:3000
   PROFILE_DATA_WS_URL=ws://0.0.0.0:8001
   CONSUMING_APPS_WS_URL=ws://0.0.0.0:8002
   STATE_TRANSFER_WS_URL=ws://0.0.0.0:8003
   DATABASE_URL=postgresql://user:pass@localhost:5432/okcupid
   DEV_MODE=false
   ```

6. **Run with systemd (keeps it running):**
   Create `/etc/systemd/system/okcupid-automation.service`:
   ```ini
   [Unit]
   Description=OkCupid Automation Service
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/flerencer
   Environment="PATH=/path/to/flerencer/venv/bin"
   ExecStart=/path/to/flerencer/venv/bin/python src/main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start service:**
   ```bash
   sudo systemctl enable okcupid-automation
   sudo systemctl start okcupid-automation
   ```

8. **Open firewall ports:**
   ```bash
   sudo ufw allow 8001/tcp
   sudo ufw allow 8002/tcp
   sudo ufw allow 8003/tcp
   ```

**Access:**
- WebSocket: `ws://your-server-ip:8001`, etc.

---

### Option 3: Docker Deployment 🐳

**Best for:** Containerized deployment

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application
COPY . .

# Expose ports
EXPOSE 8001 8002 8003

# Run application
CMD ["python", "src/main.py"]
```

**Build and run:**
```bash
docker build -t okcupid-automation .
docker run -d -p 8001:8001 -p 8002:8002 -p 8003:8003 \
  --env-file .env \
  --name okcupid-automation \
  okcupid-automation
```

---

### Option 4: Kubernetes (Already Configured!) ☸️

**Best for:** Scalable production

You already have Kubernetes configs in `k8s/` folder!

**Deploy:**
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Check status:**
```bash
kubectl get pods
kubectl get services
```

---

### Option 5: Cloud Platforms

#### AWS (Elastic Beanstalk / ECS)
- Deploy as container or directly
- Auto-scaling available
- Load balancer for WebSocket

#### Google Cloud (Cloud Run / GKE)
- Serverless option with Cloud Run
- Or use GKE for Kubernetes

#### Azure (Container Instances / AKS)
- Similar to AWS/GCP options

---

## 🔒 Security Considerations

### 1. Use Reverse Proxy (Nginx)

**Install Nginx:**
```bash
sudo apt install nginx
```

**Configure `/etc/nginx/sites-available/okcupid`:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /ws1/ {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /ws2/ {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /ws3/ {
        proxy_pass http://localhost:8003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**Enable SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. Firewall Configuration

Only open necessary ports:
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 📊 Monitoring & Maintenance

### Check if Running

```bash
# Check process
ps aux | grep python

# Check ports
netstat -tulpn | grep 8001

# Check logs
journalctl -u okcupid-automation -f
```

### Auto-restart on Failure

Systemd service (already configured above) will auto-restart.

---

## 🧪 Test Your Deployment

### Test WebSocket Connection

**Using Python:**
```python
import asyncio
import websockets

async def test():
    uri = "ws://your-server:8001"
    async with websockets.connect(uri) as websocket:
        print("✅ Connected!")
        await websocket.send('{"test": "message"}')
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(test())
```

**Using Browser Console:**
```javascript
const ws = new WebSocket('ws://your-server:8001');
ws.onopen = () => console.log('✅ Connected!');
ws.onmessage = (event) => console.log('Message:', event.data);
```

---

## 💰 Cost Comparison

| Option | Monthly Cost | Difficulty | Best For |
|--------|-------------|------------|----------|
| Local Machine | Free | Easy | Development |
| VPS (Basic) | $5-10 | Medium | Small Production |
| VPS (Scaled) | $20-50 | Medium | Medium Production |
| Kubernetes | $50+ | Hard | Large Scale |
| Cloud (AWS/GCP) | Variable | Medium | Enterprise |

---

## ✅ Quick Start - VPS Deployment

1. Get a VPS (DigitalOcean recommended)
2. Follow "Option 2: VPS" steps above
3. Configure domain name (optional)
4. Set up SSL certificate
5. Monitor with systemd logs

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8001

# Kill process
sudo kill -9 <PID>
```

### Can't Connect from Outside
- Check firewall: `sudo ufw status`
- Check if binding to 0.0.0.0 (not localhost)
- Verify security groups (cloud platforms)

### Application Crashes
- Check logs: `journalctl -u okcupid-automation`
- Verify database connection
- Check memory usage: `free -h`

---

**Your application is ready to host! Choose the option that fits your needs.** 🚀

