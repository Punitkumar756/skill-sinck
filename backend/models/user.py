from datetime import datetime

class User:
    def __init__(self, user_id, email, name, role='student'):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role  # student, admin, university
        self.created_at = datetime.utcnow()
        self.profile = None
        self.quiz_results = None
        
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'profile': self.profile,
            'quiz_results': self.quiz_results
        }

class StudentProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.skills = []
        self.education = []
        self.experience = []
        self.certifications = []
        self.interests = []
        self.projects = []
        self.updated_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'skills': self.skills,
            'education': self.education,
            'experience': self.experience,
            'certifications': self.certifications,
            'interests': self.interests,
            'projects': self.projects,
            'updated_at': self.updated_at.isoformat()
        }
