"""
Developer 2: Profile Editing
Main ProfileEditor class
"""

from .settings_navigator import SettingsNavigator
from .field_updater import FieldUpdater
from .edit_validators import EditValidators
from src.core.database import Profile


class ProfileEditor:
    """
    Main class for editing OkCupid profiles
    Initialized with:
    - page: Playwright page instance
    - profile_data: Updated profile data dictionary
    - database: Database instance
    """
    
    def __init__(self, page, profile_data: dict, database):
        self.page = page
        self.profile_data = profile_data
        self.database = database
        self.settings_navigator = SettingsNavigator(page)
        self.field_updater = FieldUpdater(page)
        self.validator = EditValidators(page)
    
    async def update_profile(self) -> bool:
        """
        Main method to update profile
        Returns True if successful, False otherwise
        """
        try:
            # Navigate to settings
            await self.settings_navigator.navigate_to_settings()
            
            # Update each field
            for field_name, field_value in self.profile_data.items():
                if field_value is not None:
                    success = await self.field_updater.update_field(field_name, field_value)
                    if not success:
                        print(f"⚠️  Failed to update field: {field_name}")
            
            # Validate edits
            is_valid = await self.validator.validate_edits()
            if not is_valid:
                return False
            
            # Return to dashboard
            await self.settings_navigator.return_to_dashboard()
            
            print("✅ Profile updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating profile: {e}")
            return False

