from datetime import datetime

class Job:
    def __init__(self, job_id, title, company, description, required_skills, location='Remote'):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.description = description
        self.required_skills = required_skills  # List of skills
        self.location = location
        self.salary_range = None
        self.experience_level = 'Entry Level'
        self.posted_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            'job_id': self.job_id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'required_skills': self.required_skills,
            'location': self.location,
            'salary_range': self.salary_range,
            'experience_level': self.experience_level,
            'posted_at': self.posted_at.isoformat()
        }

class JobMatch:
    def __init__(self, job_id, user_id, match_percentage, matching_skills, missing_skills):
        self.job_id = job_id
        self.user_id = user_id
        self.match_percentage = match_percentage
        self.matching_skills = matching_skills
        self.missing_skills = missing_skills
        self.calculated_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            'job_id': self.job_id,
            'user_id': self.user_id,
            'match_percentage': self.match_percentage,
            'matching_skills': self.matching_skills,
            'missing_skills': self.missing_skills,
            'calculated_at': self.calculated_at.isoformat()
        }
