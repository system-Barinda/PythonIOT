"""
Yes/no swipe logic
Find selectors for Like/Pass buttons
Implement reliable swipe detection
Handle match modals
"""

class SwipeActions:
    """Handles actual swipe actions"""
    
    def __init__(self, page):
        self.page = page
    
    async def swipe_yes(self) -> bool:
        """
        Perform a "yes" swipe (like)
        Returns True if successful
        """
        try:
            # Try multiple selector strategies
            like_selectors = [
                'button:has-text("Like")',
                'button:has-text("Yes")',
                '.like-button',
                '[data-testid="like"]',
                'button[aria-label*="like"]',
                '.swipe-yes'
            ]
            
            for selector in like_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    await self.page.wait_for_timeout(500)
                    
                    # Check for match modal
                    await self._handle_match_modal()
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error swiping yes: {e}")
            return False
    
    async def swipe_no(self) -> bool:
        """
        Perform a "no" swipe (pass)
        Returns True if successful
        """
        try:
            # Try multiple selector strategies
            pass_selectors = [
                'button:has-text("Pass")',
                'button:has-text("No")',
                '.pass-button',
                '[data-testid="pass"]',
                'button[aria-label*="pass"]',
                '.swipe-no'
            ]
            
            for selector in pass_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    await self.page.wait_for_timeout(500)
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error swiping no: {e}")
            return False
    
    async def get_current_profile_info(self) -> dict:
        """
        Extract profile data from current profile card
        Returns dictionary with profile information
        """
        try:
            profile_info = {}
            
            # Extract name
            name_selectors = ['.profile-name', 'h1', 'h2', '[data-testid="name"]']
            for selector in name_selectors:
                if await self.page.locator(selector).count() > 0:
                    profile_info['name'] = await self.page.locator(selector).first.text_content()
                    break
            
            # Extract age
            age_selectors = ['.profile-age', '[data-testid="age"]']
            for selector in age_selectors:
                if await self.page.locator(selector).count() > 0:
                    age_text = await self.page.locator(selector).first.text_content()
                    # Extract number from text
                    import re
                    age_match = re.search(r'\d+', age_text)
                    if age_match:
                        profile_info['age'] = int(age_match.group())
                    break
            
            # Extract bio/description
            bio_selectors = ['.profile-bio', '.description', '[data-testid="bio"]']
            for selector in bio_selectors:
                if await self.page.locator(selector).count() > 0:
                    profile_info['bio'] = await self.page.locator(selector).first.text_content()
                    break
            
            return profile_info if profile_info else None
            
        except Exception as e:
            print(f"❌ Error extracting profile info: {e}")
            return None
    
    async def _handle_match_modal(self):
        """Handle match modal if it appears"""
        try:
            match_modal_selectors = [
                '.match-modal',
                '.its-a-match',
                '[data-testid="match-modal"]'
            ]
            
            for selector in match_modal_selectors:
                if await self.page.locator(selector).count() > 0:
                    # Close modal
                    close_selectors = [
                        'button:has-text("Continue")',
                        'button:has-text("Close")',
                        '.close-button'
                    ]
                    for close_sel in close_selectors:
                        if await self.page.locator(close_sel).count() > 0:
                            await self.page.click(close_sel)
                            await self.page.wait_for_timeout(500)
                            break
                    break
        except Exception as e:
            print(f"⚠️  Error handling match modal: {e}")

