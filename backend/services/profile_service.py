from models.user import StudentProfile
from datetime import datetime

class ProfileService:
    """Service to manage user profiles"""
    
    def __init__(self):
        # In production, this would connect to a database
        self.profiles = {}
    
    def create_or_update_profile(self, user_id, profile_data):
        """Create or update a student profile"""
        
        if user_id not in self.profiles:
            profile = StudentProfile(user_id)
        else:
            profile = self.profiles[user_id]
        
        # Update profile fields
        if 'skills' in profile_data:
            profile.skills = profile_data['skills']
        
        if 'education' in profile_data:
            profile.education = profile_data['education']
        
        if 'experience' in profile_data:
            profile.experience = profile_data['experience']
        
        if 'certifications' in profile_data:
            profile.certifications = profile_data['certifications']
        
        if 'interests' in profile_data:
            profile.interests = profile_data['interests']
        
        if 'projects' in profile_data:
            profile.projects = profile_data['projects']
        
        profile.updated_at = datetime.utcnow()
        
        # Save profile
        self.profiles[user_id] = profile
        
        return profile.to_dict()
    
    def get_profile(self, user_id):
        """Get user profile"""
        if user_id in self.profiles:
            return self.profiles[user_id].to_dict()
        return None
    
    def delete_profile(self, user_id):
        """Delete user profile"""
        if user_id in self.profiles:
            del self.profiles[user_id]
            return True
        return False
    
    def get_user_skills(self, user_id):
        """Get user's skills list"""
        if user_id in self.profiles:
            return self.profiles[user_id].skills
        return []
