"""
Profile validation
Verify that profile was created successfully
"""

class ProfileValidator:
    """Validates that profile creation was successful"""
    
    def __init__(self, page):
        self.page = page
    
    async def validate_profile_created(self) -> bool:
        """
        Validate that profile was created successfully
        Returns True if profile is valid, False otherwise
        """
        try:
            # Check if we're on the dashboard/home page
            current_url = self.page.url
            if 'okcupid.com' in current_url and ('home' in current_url or 'dashboard' in current_url):
                return True
            
            # Check for profile completion indicators
            completion_indicators = [
                'profile complete',
                'welcome',
                'get started',
                'dashboard'
            ]
            
            page_text = await self.page.text_content('body')
            if page_text:
                for indicator in completion_indicators:
                    if indicator.lower() in page_text.lower():
                        return True
            
            # Check for navigation elements that indicate logged in state
            nav_selectors = [
                'nav',
                '.navigation',
                '[data-testid="navigation"]'
            ]
            
            for selector in nav_selectors:
                if await self.page.locator(selector).count() > 0:
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error validating profile: {e}")
            return False
```<ctrl63>