# profile_creator.py

"""
Developer 1: Profile Creation
Main ProfileCreator class that orchestrates profile creation
"""

# Corrected Import: Assuming database.py is accessible
from database import Profile
from .creation_steps import CreationSteps
from .obstacle_handler import ObstacleHandler
from .validators import ProfileValidator

class ProfileCreator:
    """
    Main class for creating OkCupid profiles
    Initialized with:
    - page: Playwright page instance
    - profile_data: Dictionary with profile information
    - database: Database instance
    """
    
    def __init__(self, page, profile_data: dict, database):
        self.page = page
        self.profile_data = profile_data
        self.database = database
        self.creation_steps = CreationSteps(page, profile_data)
        self.obstacle_handler = ObstacleHandler(page, database)
        self.validator = ProfileValidator(page)
    
    async def create_profile(self) -> bool:
        """
        Main method to create a profile
        Returns True if successful, False otherwise
        """
        try:
            # Navigate to OkCupid signup page
            await self.page.goto('https://www.okcupid.com/signup')
            await self.page.wait_for_load_state('networkidle')
            
            # Check for obstacles (CAPTCHA, verification, etc.)
            obstacle_detected = await self.obstacle_handler.check_for_obstacles()
            if obstacle_detected:
                # State will be transferred to headful browser automatically
                print("⚠️  Obstacle detected, transferring state...")
                return False
            
            # Fill basic info (signup form)
            success = await self.creation_steps.fill_basic_info()
            if not success:
                return False
            
            # Complete additional steps
            success = await self.creation_steps.complete_additional_steps()
            if not success:
                return False
            
            # Validate profile was created
            is_valid = await self.validator.validate_profile_created()
            if not is_valid:
                return False
            
            # Save profile to database
            await self._save_profile_to_database()
            
            print("✅ Profile created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating profile: {e}")
            return False
    
    async def _save_profile_to_database(self):
        """Save created profile to database"""
        async with self.database.get_session() as session:
            # Create profile record
            # Profile is already imported at the top of the file
            profile = Profile(
                profile_id=self.profile_data.get('email'),
                email=self.profile_data.get('email'),
                password=self.profile_data.get('password'), # FIXED: Added missing password field
                name=self.profile_data.get('name'),
                age=self.profile_data.get('age'),
                gender=self.profile_data.get('gender')
            )
            session.add(profile)
            await session.commit()