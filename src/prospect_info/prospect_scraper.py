"""
Developer 4: Prospect Info
Main ProspectScraper class
"""

from .image_extractor import ImageExtractor
from .interest_parser import InterestParser
from .description_parser import DescriptionParser

class ProspectScraper:
    """
    Main class for scraping prospect information
    Initialized with:
    - page: Playwright page instance
    """
    
    def __init__(self, page):
        self.page = page
        self.image_extractor = ImageExtractor(page)
        self.interest_parser = InterestParser(page)
        self.description_parser = DescriptionParser(page)
    
    async def scrape_profile(self, profile_id: str) -> dict:
        """
        Scrape profile information
        Returns: {images: [], interests: [], description: "", basic_info: {}}
        """
        try:
            # Navigate to profile
            profile_url = f'https://www.okcupid.com/profile/{profile_id}'
            await self.page.goto(profile_url)
            await self.page.wait_for_load_state('networkidle')
            
            # Extract all data
            images = await self.image_extractor.extract_images()
            interests = await self.interest_parser.parse_interests()
            description = await self.description_parser.parse_description()
            basic_info = await self._extract_basic_info()
            
            return {
                'images': images,
                'interests': interests,
                'description': description,
                'basic_info': basic_info
            }
            
        except Exception as e:
            print(f"❌ Error scraping profile: {e}")
            return {}
    
    async def _extract_basic_info(self) -> dict:
        """Extract age, location, etc."""
        basic_info = {}
        
        try:
            # Extract age
            age_selectors = ['.profile-age', '[data-testid="age"]']
            for selector in age_selectors:
                if await self.page.locator(selector).count() > 0:
                    age_text = await self.page.locator(selector).first.text_content()
                    import re
                    age_match = re.search(r'\d+', age_text)
                    if age_match:
                        basic_info['age'] = int(age_match.group())
                    break
            
            # Extract location
            location_selectors = ['.profile-location', '[data-testid="location"]']
            for selector in location_selectors:
                if await self.page.locator(selector).count() > 0:
                    basic_info['location'] = await self.page.locator(selector).first.text_content()
                    break
            
            # Extract name
            name_selectors = ['.profile-name', 'h1', '[data-testid="name"]']
            for selector in name_selectors:
                if await self.page.locator(selector).count() > 0:
                    basic_info['name'] = await self.page.locator(selector).first.text_content()
                    break
            
        except Exception as e:
            print(f"⚠️  Error extracting basic info: {e}")
        
        return basic_info

