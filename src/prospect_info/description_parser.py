"""
Parse descriptions
Find where descriptions are displayed
Extract text content reliably
"""

class DescriptionParser:
    """Parses descriptions/bios from profile pages"""
    
    def __init__(self, page):
        self.page = page
    
    async def parse_description(self) -> str:
        """
        Extract bio/description
        Returns description text
        """
        try:
            # Find description containers
            description_selectors = [
                '.profile-bio',
                '.about-me',
                '.description',
                '[data-testid="bio"]',
                '.profile-description'
            ]
            
            for selector in description_selectors:
                if await self.page.locator(selector).count() > 0:
                    text = await self.page.locator(selector).first.text_content()
                    if text:
                        return text.strip()
            
            # Fallback: try to find any large text block
            text_selectors = ['p', '.text-content']
            for selector in text_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    text = await element.text_content()
                    if text and len(text) > 50:  # Likely a description
                        return text.strip()
            
            return ""
            
        except Exception as e:
            print(f"❌ Error parsing description: {e}")
            return ""

