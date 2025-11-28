# message_monitor.py

"""
Developer 5: Messaging/Posting
Main MessageMonitor class
Runs continuously to monitor for new messages
"""

from .dom_monitor import DOMMonitor
from .pixel_detector import PixelDetector
from .message_scraper import MessageScraper
from .message_sender import MessageSender
from database import Database, Message # Import necessary database components
from sqlalchemy.future import select
from datetime import datetime

class MessageMonitor:
    """
    Main class for monitoring messages
    Initialized with:
    - page: Playwright page instance
    - profile_id: Profile ID
    - websocket_server: WebSocket server instance
    - database: Database instance (NEW REQUIRED ARGUMENT)
    """
    
    def __init__(self, page, profile_id: str, websocket_server, database: Database):
        self.page = page
        self.profile_id = profile_id
        self.websocket_server = websocket_server
        self.database = database # Store the database instance
        self.dom_monitor = DOMMonitor(page)
        self.pixel_detector = PixelDetector(page)
        self.message_scraper = MessageScraper(page)
        self.message_sender = MessageSender(page)
        self.running = False
    
    async def save_message_to_db(self, message_data: dict):
        """Saves a scraped message to the database."""
        # NOTE: You'll need to determine the match_id based on the current conversation
        # This logic is complex and dependent on how you navigate to a specific match's chat.
        # For simplicity, we assume a match_id and convert the scraped timestamp.
        
        # --- Simplified Logic: REQUIRES MATCH_ID from context ---
        # The scraping doesn't give match_id, so this must be passed/derived
        # In a real app, you would scrape the match_id from the URL/DOM before scraping messages.
        match_id = 1 # Placeholder for demonstration - MUST BE CORRECTED
        
        try:
            # Assuming the scraped timestamp is a string that needs parsing/conversion
            # You might need a more robust parser here depending on the timestamp format
            try:
                # Basic assumption: scraped timestamp is ISO format
                timestamp = datetime.fromisoformat(message_data.get('timestamp'))
            except (ValueError, TypeError):
                # Fallback to current time if parsing fails
                timestamp = datetime.utcnow()
                
            async with self.database.get_session() as session:
                new_message = Message(
                    profile_id=self.profile_id,
                    match_id=match_id, # Placeholder
                    content=message_data.get('content'),
                    direction=message_data.get('direction'),
                    timestamp=timestamp
                )
                session.add(new_message)
                await session.commit()
                print(f"✅ Message saved to DB for match {match_id}")
        except Exception as e:
            print(f"❌ Error saving message to DB: {e}")


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
                    
                    # Process and save new messages
                    for message in messages:
                        # 1. Save to database
                        await self.save_message_to_db(message)
                        
                        # 2. Send to WebSocket server
                        await self.websocket_server.send_message({
                            'profile_id': self.profile_id,
                            'message': message
                        })
                    
                    print(f"📨 Found and processed {len(messages)} messages")
                
                # Wait before next check
                await self.page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"❌ Error during monitoring: {e}")
                await self.page.wait_for_timeout(5000)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False