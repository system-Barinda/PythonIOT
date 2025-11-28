"""
Send messages quickly
Find message input field
Type message quickly (delay=0)
Send immediately
"""

class MessageSender:
    """Sends messages quickly"""
    
    def __init__(self, page):
        self.page = page
    
    async def send_message(self, message_text: str) -> bool:
        """
        Send message quickly
        Returns True if successful
        """
        try:
            # Find message input field
            input_selectors = [
                'textarea[name="message"]',
                'input[name="message"]',
                '.message-input',
                '[data-testid="message-input"]',
                'textarea[placeholder*="message"]'
            ]
            
            for selector in input_selectors:
                if await self.page.locator(selector).count() > 0:
                    input_field = self.page.locator(selector).first
                    
                    # Type message quickly (delay=0)
                    await input_field.fill(message_text)
                    
                    # Send message
                    send_selectors = [
                        'button[type="submit"]',
                        'button:has-text("Send")',
                        '.send-button',
                        '[data-testid="send"]'
                    ]
                    
                    for send_sel in send_selectors:
                        if await self.page.locator(send_sel).count() > 0:
                            await self.page.locator(send_sel).first.click()
                            await self.page.wait_for_timeout(500)
                            return True
                    
                    # Fallback: press Enter
                    await input_field.press('Enter')
                    await self.page.wait_for_timeout(500)
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

