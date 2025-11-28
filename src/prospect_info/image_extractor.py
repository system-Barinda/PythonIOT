"""
Extract profile images
Find all image selectors on profile pages
Extract both src attributes and CSS background images
Return list of image URLs
"""

class ImageExtractor:
    """Extracts images from profile pages"""
    
    def __init__(self, page):
        self.page = page
    
    async def extract_images(self) -> list:
        """
        Get all image URLs from profile
        Returns list of image URLs
        """
        images = []
        
        try:
            # Find all img elements
            img_selectors = [
                'img.profile-photo',
                'img[src*="profile"]',
                '.profile-image img',
                '[data-testid="profile-image"]'
            ]
            
            for selector in img_selectors:
                img_elements = await self.page.locator(selector).all()
                for img in img_elements:
                    src = await img.get_attribute('src')
                    if src and src not in images:
                        images.append(src)
            
            # Find images in CSS background
            bg_selectors = [
                '.profile-photo',
                '.photo-container',
                '[style*="background-image"]'
            ]
            
            for selector in bg_selectors:
                elements = await self.page.locator(selector).all()
                for element in elements:
                    style = await element.get_attribute('style')
                    if style and 'background-image' in style:
                        import re
                        url_match = re.search(r'url\(["\']?([^"\']+)["\']?\)', style)
                        if url_match:
                            url = url_match.group(1)
                            if url not in images:
                                images.append(url)
            
            return images
            
        except Exception as e:
            print(f"❌ Error extracting images: {e}")
            return []

