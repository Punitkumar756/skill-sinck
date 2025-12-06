from services.profile_service import ProfileService
from services.ai_service import AIService

class PortfolioService:
    """Service to generate project ideas and manage portfolios"""
    
    def __init__(self):
        self.profile_service = ProfileService()
        self.ai_service = AIService()
        self.portfolios = {}
    
    def generate_project_ideas(self, user_id, count=5):
        """Generate personalized project ideas based on user interests"""
        
        # Get user profile
        profile = self.profile_service.get_profile(user_id)
        
        if not profile:
            return []
        
        interests = profile.get('interests', [])
        skills = profile.get('skills', [])
        
        # Use AI to generate project ideas
        project_ideas = self.ai_service.generate_project_ideas(interests, skills, count)
        
        return project_ideas
    
    def get_project_implementation_guide(self, project_title, user_id):
        """Get detailed implementation guide for a project"""
        
        profile = self.profile_service.get_profile(user_id)
        skills = profile.get('skills', []) if profile else []
        
        # Generate implementation guide using AI
        guide = self.ai_service.generate_implementation_guide(project_title, skills)
        
        return guide
    
    def add_project_to_portfolio(self, user_id, project_data):
        """Add a completed project to user's portfolio"""
        
        if user_id not in self.portfolios:
            self.portfolios[user_id] = {
                'user_id': user_id,
                'projects': []
            }
        
        project = {
            'title': project_data.get('title'),
            'description': project_data.get('description'),
            'technologies': project_data.get('technologies', []),
            'github_url': project_data.get('github_url'),
            'demo_url': project_data.get('demo_url'),
            'images': project_data.get('images', []),
            'completed_date': project_data.get('completed_date')
        }
        
        self.portfolios[user_id]['projects'].append(project)
        
        return self.portfolios[user_id]
    
    def get_user_portfolio(self, user_id):
        """Get user's project portfolio"""
        return self.portfolios.get(user_id, {'user_id': user_id, 'projects': []})
    
    def remove_project(self, user_id, project_title):
        """Remove a project from portfolio"""
        if user_id in self.portfolios:
            projects = self.portfolios[user_id]['projects']
            self.portfolios[user_id]['projects'] = [
                p for p in projects if p['title'] != project_title
            ]
            return True
        return False
