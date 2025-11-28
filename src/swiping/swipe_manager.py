"""
Developer 3: Swiping
Main SwipeManager class
"""

from .swipe_actions import SwipeActions
from .preference_matcher import PreferenceMatcher
from .daily_limit_tracker import DailyLimitTracker

class SwipeManager:
    """
    Main class for managing swiping
    Initialized with:
    - page: Playwright page instance
    - preferences: User preferences dictionary
    - database: Database instance
    """
    
    def __init__(self, page, preferences: dict, database):
        self.page = page
        self.preferences = preferences
        self.database = database
        self.swipe_actions = SwipeActions(page)
        self.preference_matcher = PreferenceMatcher(preferences)
        self.limit_tracker = DailyLimitTracker(database)
    
    async def start_swiping(self, profile_id: str):
        """
        Start swiping on profiles
        Runs continuously until daily limit is reached
        """
        try:
            # Navigate to discovery/swipe page
            await self.page.goto('https://www.okcupid.com/discover')
            await self.page.wait_for_load_state('networkidle')
            
            while True:
                # Check daily limit
                remaining = await self.limit_tracker.get_remaining_swipes(profile_id)
                if remaining <= 0:
                    print("⚠️  Daily swipe limit reached")
                    break
                
                # Get current profile info
                profile_info = await self.swipe_actions.get_current_profile_info()
                if not profile_info:
                    print("⚠️  No more profiles to swipe")
                    break
                
                # Decide whether to swipe yes or no
                should_swipe_yes = await self.preference_matcher.should_swipe_yes(profile_info)
                
                if should_swipe_yes:
                    success = await self.swipe_actions.swipe_yes()
                    if success:
                        await self.limit_tracker.record_swipe(profile_id, 'yes')
                        print("✅ Swiped YES")
                else:
                    success = await self.swipe_actions.swipe_no()
                    if success:
                        await self.limit_tracker.record_swipe(profile_id, 'no')
                        print("❌ Swiped NO")
                
                # Wait for next profile to load
                await self.page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"❌ Error during swiping: {e}")

