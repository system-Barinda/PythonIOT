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

# ✅ FIXED IMPORT — correct location is src/core/database.py
from src.core.database import Database, Message


from sqlalchemy.future import select
from datetime import datetime


class MessageMonitor:
    """
    Main class for monitoring messages
    - page: Playwright page instance
    - profile_id: Profile ID
    - websocket_server: WebSocket server instance
    - database: Database instance
    """

    def __init__(self, page, profile_id: str, websocket_server, database: Database):
        self.page = page
        self.profile_id = profile_id
        self.websocket_server = websocket_server
        self.database = database
        self.dom_monitor = DOMMonitor(page)
        self.pixel_detector = PixelDetector(page)
        self.message_scraper = MessageScraper(page)
        self.message_sender = MessageSender(page)
        self.running = False

    async def save_message_to_db(self, message_data: dict):
        """Saves a scraped message to the database."""
        match_id = 1  # TODO: Replace with real match ID logic

        try:
            try:
                timestamp = datetime.fromisoformat(message_data.get('timestamp'))
            except Exception:
                timestamp = datetime.utcnow()

            async with self.database.get_session() as session:
                new_msg = Message(
                    profile_id=self.profile_id,
                    match_id=match_id,
                    content=message_data.get('content'),
                    direction=message_data.get('direction'),
                    timestamp=timestamp
                )

                session.add(new_msg)
                await session.commit()

                print(f"✅ Message saved for match {match_id}")

        except Exception as e:
            print(f"❌ Error saving message to DB: {e}")

    async def start_monitoring(self):
        """Continuously monitor the messages page."""

        self.running = True

        await self.page.goto("https://www.okcupid.com/messages")
        await self.page.wait_for_load_state("networkidle")

        print(f"✅ Message monitoring started for profile {self.profile_id}")

        while self.running:
            try:
                new_messages = await self.dom_monitor.check_for_new_messages()
                pixel_changes = await self.pixel_detector.check_for_changes()

                if new_messages or pixel_changes:
                    messages = await self.message_scraper.scrape_messages()

                    for msg in messages:
                        await self.save_message_to_db(msg)
                        await self.websocket_server.send_message({
                            "profile_id": self.profile_id,
                            "message": msg
                        })

                    print(f"📨 Processed {len(messages)} messages")

                await self.page.wait_for_timeout(2000)

            except Exception as e:
                print(f"❌ Error during monitoring: {e}")
                await self.page.wait_for_timeout(5000)

    def stop_monitoring(self):
        self.running = False
