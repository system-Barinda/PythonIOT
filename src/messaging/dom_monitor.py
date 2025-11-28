"""
DOM element monitoring
Find selectors for unread message indicators
Detect new messages in the message list
Get conversation elements with new messages
"""

class DOMMonitor:
    """Monitors DOM for new messages"""
    
    def __init__(self, page):
        self.page = page
        self.last_message_count = 0
    
    async def check_for_new_messages(self) -> bool:
        """
        Detect new messages via DOM
        Returns True if new messages detected
        """
        try:
            # Find unread message indicators
            unread_selectors = [
                '.unread',
                '.message-unread',
                '[data-unread="true"]',
                '.notification-badge',
                '[data-testid="unread"]'
            ]
            
            unread_count = 0
            for selector in unread_selectors:
                count = await self.page.locator(selector).count()
                unread_count += count
            
            # Check message list count
            message_list_selectors = [
                '.message-item',
                '.conversation',
                '[data-testid="message"]'
            ]
            
            message_count = 0
            for selector in message_list_selectors:
                count = await self.page.locator(selector).count()
                message_count = max(message_count, count)
            
            # Compare with last count
            if message_count > self.last_message_count or unread_count > 0:
                self.last_message_count = message_count
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error checking DOM for messages: {e}")
            return False

