# OkCupid Automation - Python/Playwright Project

Browser automation tool for automating OkCupid interactions using Playwright and Python.

## Features

- 🤖 Automated profile creation
- ✏️ Automated profile editing
- 💕 Automated swiping with preference matching
- 📊 Prospect information scraping
- 💬 Message monitoring and automated responses

## Technology Stack

- **Language**: Python 3.8+
- **Browser Automation**: Playwright
- **Database**: PostgreSQL
- **Communication**: WebSockets
- **Browser**: NST Browser (or local Chromium)

## Project Structure

```
okcupid-web/
├── setup/                    # Setup scripts by OS
│   ├── windows.ps1           # Windows setup
│   ├── linux.sh              # Linux setup
│   └── macos.sh              # macOS setup
├── src/
│   ├── core/                 # Core infrastructure
│   │   ├── database.py       # PostgreSQL database
│   │   └── websocket_server.py # WebSocket servers
│   ├── profile_creation/     # Developer 1: Profile Creation
│   │   ├── profile_creator.py
│   │   ├── creation_steps.py
│   │   ├── obstacle_handler.py
│   │   └── validators.py
│   ├── profile_editing/      # Developer 2: Profile Editing
│   │   ├── profile_editor.py
│   │   ├── settings_navigator.py
│   │   ├── field_updater.py
│   │   └── edit_validators.py
│   ├── swiping/              # Developer 3: Swiping
│   │   ├── swipe_manager.py
│   │   ├── swipe_actions.py
│   │   ├── preference_matcher.py
│   │   └── daily_limit_tracker.py
│   ├── prospect_info/        # Developer 4: Prospect Info
│   │   ├── prospect_scraper.py
│   │   ├── image_extractor.py
│   │   ├── interest_parser.py
│   │   └── description_parser.py
│   ├── messaging/            # Developer 5: Messaging
│   │   ├── message_monitor.py
│   │   ├── pixel_detector.py
│   │   ├── dom_monitor.py
│   │   ├── message_scraper.py
│   │   └── message_sender.py
│   └── main.py              # Main orchestration
├── quick_demo/              # Quick demo scripts
├── k8s/                     # Kubernetes configurations
└── README.md
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Set Up Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- `NST_BROWSER_URL` - NST Browser WebSocket URL
- `DATABASE_URL` - PostgreSQL connection string
- `DEV_MODE` - Set to `true` to see browser (for debugging)

### 4. Set Up Database

Ensure PostgreSQL is running and create the database:

```sql
CREATE DATABASE okcupid;
```

## Running the Application

### Activate Virtual Environment

```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/macOS
source venv/bin/activate
```

### Run Main Application

```bash
python src/main.py
```

## Configuration

Copy `.env.example` to `.env` and configure:

```env
# NST Browser
NST_BROWSER_URL=ws://localhost:3000

# WebSocket Endpoints
PROFILE_DATA_WS_URL=ws://localhost:8001
CONSUMING_APPS_WS_URL=ws://localhost:8002
STATE_TRANSFER_WS_URL=ws://localhost:8003

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/okcupid

# Development
DEV_MODE=false  # Set to true to disable headless mode
```

## Developer Quick Start Guides

### Developer 1: Profile Creation

**Location**: `src/profile_creation/`

**Files**:
- `profile_creator.py` - Main ProfileCreator class
- `creation_steps.py` - Step-by-step creation logic
- `obstacle_handler.py` - Handles obstacles (CAPTCHA, verification, etc.)
- `validators.py` - Profile validation

**First Steps**:
1. Understand the flow:
```python
from src.profile_creation import ProfileCreator
from src.core.database import Database

creator = ProfileCreator(page, profile_data, database)
success = await creator.create_profile()
```

2. Start with `creation_steps.py`:
   - Modify `fill_basic_info()` to handle your specific form fields
   - Update selectors to match OkCupid's actual HTML structure
   - Test each step individually

3. Handle obstacles in `obstacle_handler.py`:
   - Add detection for new obstacle types
   - The state transfer will automatically handle sending to headful browser

4. Test your changes:
   - Set `DEV_MODE=true` in `.env` to see the browser
   - Run the main application and watch profile creation

### Developer 2: Profile Editing

**Location**: `src/profile_editing/`

**Files**:
- `profile_editor.py` - Main ProfileEditor class
- `settings_navigator.py` - Navigate to/from settings
- `field_updater.py` - Update specific fields
- `edit_validators.py` - Validate edits

**First Steps**:
1. Start with `settings_navigator.py`:
   - Find the correct selectors for navigating to settings
   - Ensure you can reliably return to dashboard after editing

2. Implement field updates in `field_updater.py`:
   - Add handlers for each field type (bio, age, location, interests, etc.)
   - Use multiple selector strategies for reliability

### Developer 3: Swiping

**Location**: `src/swiping/`

**Files**:
- `swipe_manager.py` - Main SwipeManager class
- `preference_matcher.py` - Match preferences to profiles
- `swipe_actions.py` - Yes/no swipe logic
- `daily_limit_tracker.py` - Track daily swipe limits

**First Steps**:
1. Start with `swipe_actions.py`:
   - Find selectors for Like/Pass buttons
   - Implement reliable swipe detection
   - Handle match modals

2. Implement preference matching in `preference_matcher.py`:
   - Add your matching logic (age, distance, interests, etc.)
   - Return True for swipe yes, False for swipe no

### Developer 4: Prospect Info

**Location**: `src/prospect_info/`

**Files**:
- `prospect_scraper.py` - Main ProspectScraper class
- `image_extractor.py` - Extract profile images
- `interest_parser.py` - Parse interests
- `description_parser.py` - Parse descriptions

**First Steps**:
1. Start with `image_extractor.py`:
   - Find all image selectors on profile pages
   - Extract both src attributes and CSS background images
   - Return list of image URLs

2. Implement parsing in `interest_parser.py` and `description_parser.py`:
   - Find where interests and descriptions are displayed
   - Extract text content reliably

### Developer 5: Messaging/Posting

**Location**: `src/messaging/`

**Files**:
- `message_monitor.py` - Main MessageMonitor class
- `pixel_detector.py` - Pixel diff detection
- `dom_monitor.py` - DOM element monitoring
- `message_scraper.py` - Scrape message content
- `message_sender.py` - Send messages quickly

**First Steps**:
1. Start with `dom_monitor.py`:
   - Find selectors for unread message indicators
   - Detect new messages in the message list

2. Implement pixel detection in `pixel_detector.py`:
   - Set up monitoring regions (message list area)
   - Compare screenshots to detect changes

3. Implement message scraping in `message_scraper.py`:
   - Extract message text, timestamps, direction (sent/received)

4. Implement fast sending in `message_sender.py`:
   - Find message input field
   - Type message quickly (delay=0)
   - Send immediately

## Kubernetes Deployment

Deploy to Kubernetes using the configs in `k8s/`:

```bash
# Apply configurations
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml  # Create from secret.yaml.example first
kubectl apply -f k8s/nstbrowser-deployment.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Architecture Notes

- **Single NST Browser per node**: Each Kubernetes node runs one NST Browser instance
- **Multiple tabs per browser**: Each profile gets its own tab in the browser
- **State transfer**: When obstacles are encountered, state is transferred to a headful browser instance for resolution
- **WebSocket communication**: All profile data and messages flow through WebSockets
- **Database storage**: Profile data is stored in external database

## Troubleshooting

### NST Browser not connecting
- Ensure Docker is running: `docker ps`
- Check NST Browser logs: `docker-compose logs nst-browser`
- Verify port 3000 is accessible

### Browser automation not working
- Set `DEV_MODE=true` to see what's happening
- Check Playwright selectors match actual page structure
- Verify NST Browser is accessible at configured URL

### WebSocket connection issues
- Verify WebSocket endpoints are correct in `.env`
- Check firewall/network settings
- Ensure services are running and accessible

## Contributing

Each developer works in their own section to minimize merge conflicts:

- Developer 1: `src/profile_creation/`
- Developer 2: `src/profile_editing/`
- Developer 3: `src/swiping/`
- Developer 4: `src/prospect_info/`
- Developer 5: `src/messaging/`

Avoid modifying other developers' sections unless coordinating changes.

## License

MIT
