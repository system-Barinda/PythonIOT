"""
Handles obstacles (CAPTCHA, verification, etc.)
The state transfer will automatically handle sending to headful browser
"""

import os
from src.core.websocket_server import StateTransferWebSocketServer

class ObstacleHandler:
    """Detects and handles obstacles during profile creation"""
    
    def __init__(self, page, database):
        self.page = page
        self.database = database
        self.state_transfer_ws = StateTransferWebSocketServer(
            os.getenv('STATE_TRANSFER_WS_URL', 'ws://localhost:8003')
        )
    
    async def check_for_obstacles(self) -> bool:
        """
        Detect obstacles on the page
        Returns True if obstacle detected, False otherwise
        """
        # Check for CAPTCHA
        if await self._check_captcha():
            await self._handle_obstacle('captcha')
            return True
        
        # Check for email verification
        if await self._check_email_verification():
            await self._handle_obstacle('email_verification')
            return True
        
        # Check for phone verification
        if await self._check_phone_verification():
            await self._handle_obstacle('phone_verification')
            return True
        
        # Check for other obstacles
        if await self._check_other_obstacles():
            await self._handle_obstacle('other')
            return True
        
        return False
    
    async def _check_captcha(self) -> bool:
        """Check if CAPTCHA is present"""
        captcha_selectors = [
            '.g-recaptcha',
            '#captcha',
            'iframe[src*="recaptcha"]',
            '[data-sitekey]'
        ]
        
        for selector in captcha_selectors:
            if await self.page.locator(selector).count() > 0:
                return True
        return False
    
    async def _check_email_verification(self) -> bool:
        """Check if email verification is required"""
        verification_text = [
            'verify your email',
            'check your email',
            'email verification',
            'confirm your email'
        ]
        
        page_text = await self.page.text_content('body')
        if page_text:
            for text in verification_text:
                if text.lower() in page_text.lower():
                    return True
        return False
    
    async def _check_phone_verification(self) -> bool:
        """Check if phone verification is required"""
        phone_selectors = [
            'input[name="phone"]',
            'input[type="tel"]',
            '#phone'
        ]
        
        for selector in phone_selectors:
            if await self.page.locator(selector).count() > 0:
                # Check if it's required
                is_required = await self.page.locator(selector).get_attribute('required')
                if is_required:
                    return True
        return False
    
    async def _check_other_obstacles(self) -> bool:
        """Check for other types of obstacles"""
        # Add detection for new obstacle types
        # TODO: Implement additional obstacle detection
        return False
    
    async def _handle_obstacle(self, obstacle_type: str):
        """
        Handle obstacle by transferring state to headful browser
        """
        print(f"⚠️  Handling obstacle: {obstacle_type}")
        
        # Get current page state
        state_data = {
            'type': obstacle_type,
            'url': self.page.url,
            'html': await self.page.content(),
            'cookies': await self.page.context.cookies()
        }
        
        # Transfer state to headful browser
        await self.state_transfer_ws.transfer_state(state_data)
        print("✅ State transferred to headful browser for resolution")

