"""
Navigate to/from settings
Find the correct selectors for navigating to settings
Ensure you can reliably return to dashboard after editing
"""

class SettingsNavigator:
    """Handles navigation to and from settings page"""
    
    def __init__(self, page):
        self.page = page
    
    async def navigate_to_settings(self) -> bool:
        """
        Navigate to settings page
        TODO: Update selectors to match OkCupid's actual structure
        """
        try:
            # Try multiple selector strategies for reliability
            settings_selectors = [
                'a[href*="settings"]',
                'a[href*="edit"]',
                'button:has-text("Settings")',
                'button:has-text("Edit Profile")',
                '.settings-link',
                '[data-testid="settings"]'
            ]
            
            for selector in settings_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    await self.page.wait_for_load_state('networkidle')
                    return True
            
            # If direct link not found, try navigating via menu
            menu_selectors = [
                '.menu-button',
                '.profile-menu',
                '[data-testid="menu"]'
            ]
            
            for selector in menu_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    await self.page.wait_for_timeout(500)
                    
                    # Click settings in menu
                    settings_in_menu = 'a:has-text("Settings"), a:has-text("Edit")'
                    if await self.page.locator(settings_in_menu).count() > 0:
                        await self.page.click(settings_in_menu)
                        await self.page.wait_for_load_state('networkidle')
                        return True
            
            print("❌ Could not find settings page")
            return False
            
        except Exception as e:
            print(f"❌ Error navigating to settings: {e}")
            return False
    
    async def return_to_dashboard(self) -> bool:
        """
        Return to dashboard after editing
        TODO: Update selectors to match OkCupid's actual structure
        """
        try:
            # Try multiple selector strategies
            dashboard_selectors = [
                'a[href*="home"]',
                'a[href*="dashboard"]',
                'button:has-text("Home")',
                'button:has-text("Dashboard")',
                '.home-link',
                '.logo',
                '[data-testid="home"]'
            ]
            
            for selector in dashboard_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    await self.page.wait_for_load_state('networkidle')
                    return True
            
            # Fallback: navigate to home URL
            await self.page.goto('https://www.okcupid.com/home')
            await self.page.wait_for_load_state('networkidle')
            return True
            
        except Exception as e:
            print(f"❌ Error returning to dashboard: {e}")
            return False

