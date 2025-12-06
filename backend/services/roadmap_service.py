from services.job_matching_service import JobMatchingService
from services.ai_service import AIService
from datetime import datetime, timedelta

class RoadmapService:
    """Service to generate personalized learning roadmaps"""
    
    def __init__(self):
        self.job_service = JobMatchingService()
        self.ai_service = AIService()
        self.roadmaps = {}
    
    def generate_roadmap(self, user_id, target_job_id):
        """Generate a personalized learning roadmap"""
        
        # Calculate job match to identify skill gaps
        match_data = self.job_service.calculate_job_match(user_id, target_job_id)
        
        if 'error' in match_data:
            return match_data
        
        missing_skills = match_data['missing_skills']
        job_title = match_data['job']['title']
        
        # Generate learning path for each missing skill
        learning_path = []
        current_date = datetime.utcnow()
        
        for idx, skill in enumerate(missing_skills):
            courses = self._get_courses_for_skill(skill)
            
            # Calculate timeline (2-4 weeks per skill)
            weeks_needed = 3
            start_date = current_date + timedelta(weeks=idx * weeks_needed)
            end_date = start_date + timedelta(weeks=weeks_needed)
            
            learning_path.append({
                'skill': skill,
                'priority': 'High' if idx < 3 else 'Medium',
                'courses': courses,
                'estimated_duration': f'{weeks_needed} weeks',
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'status': 'not-started'
            })
        
        # Generate AI-powered recommendations
        additional_tips = self.ai_service.generate_roadmap_tips(job_title, missing_skills)
        
        roadmap = {
            'user_id': user_id,
            'target_job_id': target_job_id,
            'target_job_title': job_title,
            'current_match_percentage': match_data['match_percentage'],
            'learning_path': learning_path,
            'total_duration': f'{len(missing_skills) * 3} weeks',
            'additional_tips': additional_tips,
            'created_at': datetime.utcnow().isoformat(),
            'progress': 0
        }
        
        # Store roadmap
        self.roadmaps[user_id] = roadmap
        
        return roadmap
    
    def _get_courses_for_skill(self, skill):
        """Get recommended courses for a skill"""
        
        # Mock course database
        course_db = {
            'Python': [
                {'name': 'Python for Everybody', 'provider': 'Coursera', 'type': 'Free', 'url': 'https://coursera.org'},
                {'name': 'Complete Python Bootcamp', 'provider': 'Udemy', 'type': 'Paid', 'url': 'https://udemy.com'}
            ],
            'Machine Learning': [
                {'name': 'Machine Learning by Andrew Ng', 'provider': 'Coursera', 'type': 'Free', 'url': 'https://coursera.org'},
                {'name': 'Applied ML', 'provider': 'Fast.ai', 'type': 'Free', 'url': 'https://fast.ai'}
            ],
            'React': [
                {'name': 'React - The Complete Guide', 'provider': 'Udemy', 'type': 'Paid', 'url': 'https://udemy.com'},
                {'name': 'React Documentation', 'provider': 'Official', 'type': 'Free', 'url': 'https://react.dev'}
            ],
            'SQL': [
                {'name': 'SQL for Data Science', 'provider': 'Coursera', 'type': 'Free', 'url': 'https://coursera.org'},
                {'name': 'The Complete SQL Bootcamp', 'provider': 'Udemy', 'type': 'Paid', 'url': 'https://udemy.com'}
            ],
            'AWS': [
                {'name': 'AWS Cloud Practitioner', 'provider': 'AWS Training', 'type': 'Free', 'url': 'https://aws.training'},
                {'name': 'AWS Certified Solutions Architect', 'provider': 'A Cloud Guru', 'type': 'Paid', 'url': 'https://acloudguru.com'}
            ]
        }
        
        # Return courses for skill or generic courses
        return course_db.get(skill, [
            {'name': f'{skill} Fundamentals', 'provider': 'YouTube', 'type': 'Free', 'url': 'https://youtube.com'},
            {'name': f'Master {skill}', 'provider': 'Udemy', 'type': 'Paid', 'url': 'https://udemy.com'}
        ])
    
    def get_user_roadmap(self, user_id):
        """Get user's learning roadmap"""
        return self.roadmaps.get(user_id)
    
    def update_progress(self, user_id, skill_id, status):
        """Update learning progress for a skill"""
        roadmap = self.roadmaps.get(user_id)
        
        if not roadmap:
            return None
        
        # Update skill status
        for item in roadmap['learning_path']:
            if item['skill'] == skill_id:
                item['status'] = status
                break
        
        # Recalculate overall progress
        total_skills = len(roadmap['learning_path'])
        completed_skills = sum(1 for item in roadmap['learning_path'] if item['status'] == 'completed')
        roadmap['progress'] = round((completed_skills / total_skills) * 100, 1) if total_skills > 0 else 0
        
        return roadmap
