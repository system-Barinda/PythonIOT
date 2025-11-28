"""
Validate edits
Verify that profile edits were successful
"""

class EditValidators:
    """Validates that profile edits were successful"""
    
    def __init__(self, page):
        self.page = page
    
    async def validate_edits(self) -> bool:
        """
        Validate that edits were saved successfully
        Returns True if edits are valid, False otherwise
        """
        try:
            # Check for success message
            success_indicators = [
                'saved',
                'updated',
                'success',
                'changes saved'
            ]
            
            page_text = await self.page.text_content('body')
            if page_text:
                for indicator in success_indicators:
                    if indicator.lower() in page_text.lower():
                        return True
            
            # Check if we're still on settings page (might indicate error)
            current_url = self.page.url
            if 'settings' in current_url or 'edit' in current_url:
                # Check for error messages
                error_selectors = [
                    '.error',
                    '.alert-error',
                    '[role="alert"]'
                ]
                
                for selector in error_selectors:
                    if await self.page.locator(selector).count() > 0:
                        error_text = await self.page.locator(selector).text_content()
                        if error_text:
                            print(f"⚠️  Error detected: {error_text}")
                            return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error validating edits: {e}")
            return False

