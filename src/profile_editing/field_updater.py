"""
Update specific fields
Add handlers for each field type (bio, age, location, interests, etc.)
Use multiple selector strategies for reliability
"""

class FieldUpdater:
    """Handles updating individual profile fields"""
    
    def __init__(self, page):
        self.page = page
    
    async def update_field(self, field_name: str, field_value) -> bool:
        """
        Update a specific field
        Routes to field-specific handlers
        """
        field_handlers = {
            'bio': self._update_bio,
            'age': self._update_age,
            'location': self._update_location,
            'interests': self._update_interests,
            'photos': self._update_photos,
            'name': self._update_name,
            'gender': self._update_gender
        }
        
        handler = field_handlers.get(field_name)
        if handler:
            return await handler(field_value)
        else:
            print(f"⚠️  No handler for field: {field_name}")
            return False
    
    async def _update_bio(self, bio: str) -> bool:
        """Update bio field"""
        try:
            bio_selectors = [
                'textarea[name="bio"]',
                'textarea[name="about"]',
                '#bio',
                '[data-testid="bio"]'
            ]
            
            for selector in bio_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.fill(selector, bio)
                    return True
            
            return False
        except Exception as e:
            print(f"❌ Error updating bio: {e}")
            return False
    
    async def _update_age(self, age: int) -> bool:
        """Update age field"""
        try:
            age_selectors = [
                'input[name="age"]',
                'input[type="number"]',
                '#age',
                '[data-testid="age"]'
            ]
            
            for selector in age_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.fill(selector, str(age))
                    return True
            
            return False
        except Exception as e:
            print(f"❌ Error updating age: {e}")
            return False
    
    async def _update_location(self, location: dict) -> bool:
        """Update location fields"""
        try:
            # Update city
            if location.get('city'):
                city_selectors = ['input[name="city"]', '#city']
                for selector in city_selectors:
                    if await self.page.locator(selector).count() > 0:
                        await self.page.fill(selector, location['city'])
                        break
            
            # Update state
            if location.get('state'):
                state_selectors = ['input[name="state"]', 'select[name="state"]', '#state']
                for selector in state_selectors:
                    if await self.page.locator(selector).count() > 0:
                        await self.page.fill(selector, location['state'])
                        break
            
            return True
        except Exception as e:
            print(f"❌ Error updating location: {e}")
            return False
    
    async def _update_interests(self, interests: list) -> bool:
        """Update interests"""
        try:
            # TODO: Implement interest selection
            # This will depend on how OkCupid displays interests
            pass
        except Exception as e:
            print(f"❌ Error updating interests: {e}")
            return False
    
    async def _update_photos(self, photos: list) -> bool:
        """Update photos"""
        try:
            # TODO: Implement photo upload
            pass
        except Exception as e:
            print(f"❌ Error updating photos: {e}")
            return False
    
    async def _update_name(self, name: str) -> bool:
        """Update name field"""
        try:
            name_selectors = ['input[name="name"]', '#name']
            for selector in name_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.fill(selector, name)
                    return True
            return False
        except Exception as e:
            print(f"❌ Error updating name: {e}")
            return False
    
    async def _update_gender(self, gender: str) -> bool:
        """Update gender field"""
        try:
            gender_selectors = [
                f'input[value="{gender}"]',
                'select[name="gender"]',
                '#gender'
            ]
            for selector in gender_selectors:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    return True
            return False
        except Exception as e:
            print(f"❌ Error updating gender: {e}")
            return False

