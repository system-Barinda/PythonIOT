"""
Scrape message content
Extract message text, timestamps, direction (sent/received)
Handle multiple messages in a conversation
"""

class MessageScraper:
    """Scrapes message content from pages"""
    
    def __init__(self, page):
        self.page = page
    
    async def scrape_messages(self) -> list:
        """
        Extract message content
        Returns list of message dictionaries
        """
        messages = []
        
        try:
            # Find message elements
            message_selectors = [
                '.message',
                '.message-item',
                '[data-testid="message"]'
            ]
            
            for selector in message_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    message_data = await self._extract_message_data(element)
                    if message_data:
                        messages.append(message_data)
            
            return messages
            
        except Exception as e:
            print(f"❌ Error scraping messages: {e}")
            return []
    
    async def _extract_message_data(self, element) -> dict:
        """Extract data from a single message element"""
        try:
            # Extract text
            text = await element.text_content()
            
            # Determine direction (sent/received)
            direction = 'received'  # Default
            sent_indicators = ['.sent', '.outgoing', '[data-direction="sent"]']
            for indicator in sent_indicators:
                if await element.locator(indicator).count() > 0:
                    direction = 'sent'
                    break
            
            # Extract timestamp
            timestamp = None
            time_selectors = ['.timestamp', '.time', '[data-time]']
            for selector in time_selectors:
                time_elem = element.locator(selector).first
                if await time_elem.count() > 0:
                    timestamp = await time_elem.text_content()
                    break
            
            return {
                'content': text.strip() if text else '',
                'direction': direction,
                'timestamp': timestamp
            }
            
        except Exception as e:
            print(f"⚠️  Error extracting message data: {e}")
            return None

