"""
Pixel diff detection
Set up monitoring regions (message list area)
Compare screenshots to detect changes
Optionally check specific pixel coordinates
"""

from PIL import Image
import io
import hashlib

class PixelDetector:
    """Detects changes via pixel comparison"""
    
    def __init__(self, page):
        self.page = page
        self.last_screenshot_hash = None
        self.monitoring_region = None  # (x, y, width, height)
    
    async def check_for_changes(self) -> bool:
        """
        Detect changes via pixel diff
        Returns True if changes detected
        """
        try:
            # Take screenshot of message list area
            screenshot = await self._take_screenshot()
            
            if screenshot:
                # Calculate hash
                current_hash = hashlib.md5(screenshot).hexdigest()
                
                # Compare with last hash
                if self.last_screenshot_hash and current_hash != self.last_screenshot_hash:
                    self.last_screenshot_hash = current_hash
                    return True
                
                # Update hash
                if not self.last_screenshot_hash:
                    self.last_screenshot_hash = current_hash
            
            return False
            
        except Exception as e:
            print(f"❌ Error checking pixel changes: {e}")
            return False
    
    async def _take_screenshot(self) -> bytes:
        """Take screenshot of message list area"""
        try:
            # Find message list container
            message_list_selectors = [
                '.message-list',
                '.conversations',
                '[data-testid="message-list"]'
            ]
            
            for selector in message_list_selectors:
                if await self.page.locator(selector).count() > 0:
                    element = self.page.locator(selector).first
                    screenshot = await element.screenshot()
                    return screenshot
            
            # Fallback: screenshot entire page
            screenshot = await self.page.screenshot()
            return screenshot
            
        except Exception as e:
            print(f"⚠️  Error taking screenshot: {e}")
            return None
    
    def set_monitoring_region(self, x: int, y: int, width: int, height: int):
        """Set specific region to monitor"""
        self.monitoring_region = (x, y, width, height)

