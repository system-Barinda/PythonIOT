"""
Parse interests
Find where interests are displayed
Extract text content reliably
"""

class InterestParser:
    """Parses interests from profile pages"""
    
    def __init__(self, page):
        self.page = page
    
    async def parse_interests(self) -> list:
        """
        Extract interests list
        Returns list of interests
        """
        interests = []
        
        try:
            # Find interest containers
            interest_selectors = [
                '.interests',
                '.tags',
                '[data-testid="interests"]',
                '.interest-tag'
            ]
            
            for selector in interest_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    text = await element.text_content()
                    if text:
                        # Split by common separators
                        items = text.replace(',', '|').split('|')
                        for item in items:
                            item = item.strip()
                            if item and item not in interests:
                                interests.append(item)
            
            # Also try finding individual interest elements
            individual_selectors = [
                '.interest',
                '.tag',
                '[data-interest]'
            ]
            
            for selector in individual_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    text = await element.text_content()
                    if text:
                        text = text.strip()
                        if text and text not in interests:
                            interests.append(text)
            
            return interests
            
        except Exception as e:
            print(f"❌ Error parsing interests: {e}")
            return []

