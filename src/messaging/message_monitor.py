"""
Developer 5: Messaging/Posting
Main MessageMonitor class
Runs continuously to monitor for new messages
"""

from .dom_monitor import DOMMonitor
from .pixel_detector import PixelDetector
from .message_scraper import MessageScraper
from .message_sender import MessageSender

class MessageMonitor:
    """
    Main class for monitoring messages
    Initialized with:
    - page: Playwright page instance
    - profile_id: Profile ID
    - websocket_server: WebSocket server instance
    """
    
    def __init__(self, page, profile_id: str, websocket_server):
        self.page = page
        self.profile_id = profile_id
        self.websocket_server = websocket_server
        self.dom_monitor = DOMMonitor(page)
        self.pixel_detector = PixelDetector(page)
        self.message_scraper = MessageScraper(page)
        self.message_sender = MessageSender(page)
        self.running = False
    
    async def start_monitoring(self):
        """
        Start monitoring for new messages
        Runs continuously
        """
        self.running = True
        
        # Navigate to messages page
        await self.page.goto('https://www.okcupid.com/messages')
        await self.page.wait_for_load_state('networkidle')
        
        print(f"✅ Message monitoring started for profile {self.profile_id}")
        
        while self.running:
            try:
                # Check for new messages via DOM
                new_messages = await self.dom_monitor.check_for_new_messages()
                
                # Also check via pixel detection
                pixel_changes = await self.pixel_detector.check_for_changes()
                
                if new_messages or pixel_changes:
                    # Scrape messages
                    messages = await self.message_scraper.scrape_messages()
                    
                    # Send to WebSocket server
                    for message in messages:
                        await self.websocket_server.send_message({
                            'profile_id': self.profile_id,
                            'message': message
                        })
                    
                    print(f"📨 Found {len(messages)} new messages")
                
                # Wait before next check
                await self.page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"❌ Error during monitoring: {e}")
                await self.page.wait_for_timeout(5000)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False

