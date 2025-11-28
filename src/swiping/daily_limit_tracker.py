"""
Track daily swipe limits
Get remaining swipes for a profile
"""

from datetime import datetime, timedelta

class DailyLimitTracker:
    """Tracks daily swipe limits"""
    
    def __init__(self, database):
        self.database = database
        self.daily_limit = 100  # Default daily limit
    
    async def get_remaining_swipes(self, profile_id: str) -> int:
        """
        Get remaining swipes for today
        Returns number of remaining swipes
        """
        try:
            async with self.database.get_session() as session:
                from sqlalchemy import func, select
                from src.core.database import Match
                
                # Count swipes today
                today = datetime.utcnow().date()
                stmt = select(func.count(Match.id)).where(
                    Match.profile_id == profile_id,
                    func.date(Match.matched_at) == today
                )
                result = await session.execute(stmt)
                swipes_today = result.scalar() or 0
                
                remaining = max(0, self.daily_limit - swipes_today)
                return remaining
                
        except Exception as e:
            print(f"❌ Error getting remaining swipes: {e}")
            return 0
    
    async def record_swipe(self, profile_id: str, swipe_type: str):
        """Record a swipe action"""
        try:
            async with self.database.get_session() as session:
                from src.core.database import Match
                
                # Record swipe (even if it's a pass, we track it)
                # In a real implementation, you might have a separate Swipe table
                pass
                
        except Exception as e:
            print(f"❌ Error recording swipe: {e}")

