# 📖 What This Project Does

## 🎯 Main Purpose

This is an **OkCupid Browser Automation System** that automates various tasks on the OkCupid dating platform using Python and Playwright. It's designed to handle multiple profiles simultaneously and automate repetitive dating app tasks.

---

## 🤖 What It Automates

### 1. **Profile Creation** 🤖
- Automatically creates new OkCupid profiles
- Fills out signup forms (email, password, name, age, gender)
- Handles profile setup steps (photos, bio, interests)
- Detects and handles obstacles like CAPTCHA or verification
- Saves profile data to database

### 2. **Profile Editing** ✏️
- Updates existing profile information
- Changes bio, age, location, interests
- Updates photos
- Navigates to settings and back automatically

### 3. **Automated Swiping** 💕
- Automatically swipes through profiles (Like/Pass)
- Uses preference matching to decide who to swipe on
- Tracks daily swipe limits
- Handles match notifications

### 4. **Prospect Information Scraping** 📊
- Extracts data from profiles you're viewing
- Gets images, interests, descriptions
- Collects age, location, and other basic info
- Stores data for analysis

### 5. **Message Monitoring & Automation** 💬
- Monitors for new messages in real-time
- Detects new messages using DOM changes or pixel detection
- Scrapes message content
- Can send automated responses quickly

---

## 🏗️ How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│         OkCupid Automation              │
│                                         │
│  ┌──────────────┐                       │
│  │   Browser    │  (Playwright)         │
│  │  Automation  │                       │
│  └──────────────┘                       │
│         │                               │
│         ▼                               │
│  ┌──────────────┐                       │
│  │   Database   │  (PostgreSQL)        │
│  │   Storage    │                       │
│  └──────────────┘                       │
│         │                               │
│         ▼                               │
│  ┌──────────────┐                       │
│  │  WebSocket   │  (3 servers)          │
│  │   Servers    │                       │
│  └──────────────┘                       │
└─────────────────────────────────────────┘
```

### Key Components

1. **Browser Automation (Playwright)**
   - Controls a real browser (Chromium)
   - Can run headless (invisible) or visible
   - Handles multiple browser tabs (one per profile)

2. **Database (PostgreSQL)**
   - Stores profile information
   - Tracks matches and messages
   - Keeps swipe history

3. **WebSocket Servers**
   - **Port 8001**: Sends profile data to external apps
   - **Port 8002**: Receives messages for consuming applications
   - **Port 8003**: Handles state transfer (for obstacle resolution)

4. **Multi-Profile Support**
   - Each profile gets its own browser tab
   - Can manage multiple OkCupid accounts simultaneously
   - Independent automation for each profile

---

## 🔄 Workflow Example

### Typical Use Case:

1. **Setup Phase:**
   ```
   - Start application
   - Connect to database
   - Launch browser
   - Start WebSocket servers
   ```

2. **Profile Creation:**
   ```
   - Navigate to OkCupid signup
   - Fill form with profile data
   - Handle CAPTCHA (if needed)
   - Complete profile setup
   - Save to database
   ```

3. **Swiping:**
   ```
   - Navigate to discovery page
   - Get current profile shown
   - Check preferences (age, distance, interests)
   - Decide: Swipe Yes or No
   - Track daily limits
   - Continue until limit reached
   ```

4. **Message Monitoring:**
   ```
   - Monitor message page continuously
   - Detect new messages (DOM or pixel changes)
   - Extract message content
   - Send to WebSocket for processing
   - Optionally send automated response
   ```

---

## 🎨 Developer Organization

The project is split into **5 developer sections** to minimize conflicts:

- **Developer 1**: Profile Creation
- **Developer 2**: Profile Editing  
- **Developer 3**: Swiping
- **Developer 4**: Prospect Info Scraping
- **Developer 5**: Messaging

Each developer works independently in their own folder.

---

## 💡 Real-World Use Cases

### Use Case 1: Dating Research
- Automate profile creation for research
- Collect data on user preferences
- Analyze matching patterns

### Use Case 2: Profile Management
- Manage multiple dating profiles
- Update profiles automatically
- Keep profiles active

### Use Case 3: Automated Matching
- Automate swiping based on preferences
- Save time on repetitive actions
- Focus on meaningful matches

### Use Case 4: Message Automation
- Monitor messages 24/7
- Get instant notifications
- Quick response system

---

## 🔧 Technical Details

### Technologies Used:
- **Python 3.8+** - Main programming language
- **Playwright** - Browser automation
- **PostgreSQL** - Database storage
- **WebSockets** - Real-time communication
- **SQLAlchemy** - Database ORM
- **NST Browser** (optional) - Remote browser control

### Deployment Options:
- **Local Machine** - For development/testing
- **VPS** - For production hosting
- **Docker** - Containerized deployment
- **Kubernetes** - Scalable cloud deployment

---

## ⚠️ Important Notes

### What This Project Is:
✅ A browser automation tool  
✅ A multi-profile management system  
✅ A data collection and analysis tool  
✅ A WebSocket-based API server  

### What This Project Is NOT:
❌ A web application with a user interface  
❌ A mobile app  
❌ A traditional REST API  
❌ A replacement for manual OkCupid usage  

---

## 🚀 Getting Started

1. **Run the application:**
   ```powershell
   python src/main.py
   ```

2. **Use the automation:**
   - Connect via WebSocket clients
   - Send commands to create profiles
   - Monitor messages
   - Scrape data

3. **Access data:**
   - Query PostgreSQL database
   - Connect to WebSocket servers
   - Use the API endpoints

---

## 📊 Summary

**In simple terms:** This project automates OkCupid dating app tasks like creating profiles, swiping, monitoring messages, and collecting data. It's designed for managing multiple profiles simultaneously and can be deployed on servers to run 24/7.

**Think of it as:** A robot assistant that handles repetitive OkCupid tasks so you don't have to do them manually.

---

**Ready to use?** Check `RUN_PROJECT.md` to get started!

