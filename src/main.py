"""
Main orchestration file for OkCupid Automation
Coordinates all modules and manages browser instances
"""

import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from core.database import Database
from src.core.websocket_server import ConsumingAppsWebSocketServer, ProfileDataWebSocketServer, StateTransferWebSocketServer
from src.profile_creation.profile_creator import ProfileCreator
from src.profile_editing.profile_editor import ProfileEditor
from src.swiping.swipe_manager import SwipeManager
from src.prospect_info.prospect_scraper import ProspectScraper
from src.messaging.message_monitor import MessageMonitor

load_dotenv()

class OkCupidAutomation:
    def __init__(self):
        self.nst_browser_url = os.getenv('NST_BROWSER_URL', 'ws://localhost:3000')
        self.dev_mode = os.getenv('DEV_MODE', 'false').lower() == 'true'
        self.database = Database()
        self.playwright = None
        self.browser = None
        
        # WebSocket servers
        self.profile_data_ws = ProfileDataWebSocketServer(
            os.getenv('PROFILE_DATA_WS_URL', 'ws://localhost:8001')
        )
        self.consuming_apps_ws = ConsumingAppsWebSocketServer(
            os.getenv('CONSUMING_APPS_WS_URL', 'ws://localhost:8002')
        )
        self.state_transfer_ws = StateTransferWebSocketServer(
            os.getenv('STATE_TRANSFER_WS_URL', 'ws://localhost:8003')
        )
    
    async def initialize(self):
        """Initialize browser and database connections"""
        print("🚀 Initializing OkCupid Automation...")
        
        # Connect to database
        await self.database.connect()
        print("✅ Database connected")
        
        # Start WebSocket servers
        await asyncio.gather(
            self.profile_data_ws.start(),
            self.consuming_apps_ws.start(),
            self.state_transfer_ws.start()
        )
        print("✅ WebSocket servers started")
        
        # Initialize Playwright
        self.playwright = await async_playwright().start()
        
        # Connect to NST Browser or create local browser
        if self.nst_browser_url:
            try:
                self.browser = await self.playwright.chromium.connect_over_cdp(self.nst_browser_url)
                print(f"✅ Connected to NST Browser at {self.nst_browser_url}")
            except Exception as e:
                print(f"⚠️  Could not connect to NST Browser: {e}")
                print("🔄 Falling back to local browser...")
                self.browser = await self.playwright.chromium.launch(
                    headless=not self.dev_mode
                )
        else:
            self.browser = await self.playwright.chromium.launch(
                headless=not self.dev_mode
            )
            print("✅ Local browser launched")
    
    async def create_profile(self, profile_data):
        """Create a new profile using Developer 1's module"""
        context = await self.browser.new_context()
        page = await context.new_page()
        
        creator = ProfileCreator(page, profile_data, self.database)
        success = await creator.create_profile()
        
        await context.close()
        return success
    
    async def update_profile(self, profile_id, updated_data):
        """Update profile using Developer 2's module"""
        context = await self.browser.new_context()
        page = await context.new_page()
        
        editor = ProfileEditor(page, updated_data, self.database)
        success = await editor.update_profile()
        
        await context.close()
        return success
    
    async def start_swiping(self, profile_id, preferences):
        """Start swiping using Developer 3's module"""
        context = await self.browser.new_context()
        page = await context.new_page()
        
        swipe_manager = SwipeManager(page, preferences, self.database)
        await swipe_manager.start_swiping(profile_id)
        
        # Keep context open for continuous swiping
        return context
    
    async def scrape_prospect(self, profile_id):
        """Scrape prospect info using Developer 4's module"""
        context = await self.browser.new_context()
        page = await context.new_page()
        
        scraper = ProspectScraper(page)
        prospect_data = await scraper.scrape_profile(profile_id)
        
        await context.close()
        return prospect_data
    
    async def monitor_messages(self, profile_id):
        """Monitor messages using Developer 5's module"""
        context = await self.browser.new_context()
        page = await context.new_page()
        
        monitor = MessageMonitor(
            page, 
            profile_id, 
            self.consuming_apps_ws
        )
        await monitor.start_monitoring()
        
        # Keep context open for continuous monitoring
        return context
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        await self.database.disconnect()
        print("✅ Cleanup complete")

async def main():
    """Main entry point"""
    automation = OkCupidAutomation()
    
    try:
        await automation.initialize()
        
        # Example usage - you would call these based on your workflow
        # profile_data = {...}
        # await automation.create_profile(profile_data)
        
        # Keep running
        print("✅ Automation system ready")
        await asyncio.Event().wait()  # Keep running indefinitely
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        await automation.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

