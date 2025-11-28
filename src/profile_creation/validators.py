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
            # Check current URL for dashboard/home signs
            current_url = self.page.url
            if 'okcupid.com' in current_url and ('home' in current_url or 'dashboard' in current_url):
                return True
            
            # Check for page text indicators
            completion_indicators = [
                'profile complete',
                'welcome',
                'get started',
                'dashboard'
            ]
            
            page_text = await self.page.text_content('body')
            if page_text:
                page_text = page_text.lower()
                for indicator in completion_indicators:
                    if indicator in page_text:
                        return True
            
            # Check for navigation UI elements
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
