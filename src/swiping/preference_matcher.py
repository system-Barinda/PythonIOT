"""
Match preferences to profiles
Add your matching logic (age, distance, interests, etc.)
Return True for swipe yes, False for swipe no
"""

class PreferenceMatcher:
    """Matches user preferences to profiles"""
    
    def __init__(self, preferences: dict):
        self.preferences = preferences
    
    async def should_swipe_yes(self, profile_info: dict) -> bool:
        """
        Determine if we should swipe yes based on preferences
        Returns True for swipe yes, False for swipe no
        """
        if not profile_info:
            return False
        
        # Age matching
        if not self._check_age_match(profile_info):
            return False
        
        # Distance matching (if available)
        if 'distance' in profile_info and 'max_distance' in self.preferences:
            if profile_info['distance'] > self.preferences['max_distance']:
                return False
        
        # Interest matching (if available)
        if 'interests' in profile_info and 'required_interests' in self.preferences:
            if not self._check_interests_match(profile_info['interests']):
                return False
        
        # Bio matching (if we have keywords)
        if 'bio' in profile_info and 'bio_keywords' in self.preferences:
            if not self._check_bio_match(profile_info['bio']):
                return False
        
        # If all checks pass, swipe yes
        return True
    
    def _check_age_match(self, profile_info: dict) -> bool:
        """Check if age matches preferences"""
        if 'age' not in profile_info:
            return True  # If age not available, don't filter
        
        age = profile_info['age']
        min_age = self.preferences.get('min_age', 18)
        max_age = self.preferences.get('max_age', 100)
        
        return min_age <= age <= max_age
    
    def _check_interests_match(self, profile_interests: list) -> bool:
        """Check if interests match"""
        required = self.preferences.get('required_interests', [])
        if not required:
            return True
        
        # Check if at least one required interest is present
        profile_interest_set = set(interest.lower() for interest in profile_interests)
        required_set = set(interest.lower() for interest in required)
        
        return len(profile_interest_set.intersection(required_set)) > 0
    
    def _check_bio_match(self, bio: str) -> bool:
        """Check if bio contains keywords"""
        keywords = self.preferences.get('bio_keywords', [])
        if not keywords:
            return True
        
        bio_lower = bio.lower()
        return any(keyword.lower() in bio_lower for keyword in keywords)

