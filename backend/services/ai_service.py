import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """AI service for content generation using Gemini/OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GEMINI_API_KEY')
        self.model = 'gpt-3.5-turbo'  # or gemini-pro
    
    def generate_project_ideas(self, interests, skills, count=5):
        """Generate personalized project ideas"""
        
        # Mock AI-generated project ideas
        # In production, this would call OpenAI/Gemini API
        
        project_templates = [
            {
                'title': 'Music Recommendation System',
                'description': 'Build a personalized music recommender using collaborative filtering',
                'difficulty': 'Intermediate',
                'skills_needed': ['Python', 'Machine Learning', 'Pandas'],
                'estimated_time': '3-4 weeks',
                'why_recommended': 'Matches your interest in music and data analysis'
            },
            {
                'title': 'E-commerce Platform',
                'description': 'Create a full-stack online shopping platform with payment integration',
                'difficulty': 'Advanced',
                'skills_needed': ['React', 'Node.js', 'MongoDB', 'REST API'],
                'estimated_time': '6-8 weeks',
                'why_recommended': 'Great for showcasing full-stack development skills'
            },
            {
                'title': 'Personal Finance Tracker',
                'description': 'Build a web app to track expenses and visualize spending patterns',
                'difficulty': 'Beginner',
                'skills_needed': ['JavaScript', 'HTML', 'CSS', 'Chart.js'],
                'estimated_time': '2-3 weeks',
                'why_recommended': 'Practical project that demonstrates frontend skills'
            },
            {
                'title': 'Real-time Chat Application',
                'description': 'Develop a real-time messaging app with WebSocket support',
                'difficulty': 'Intermediate',
                'skills_needed': ['React', 'Node.js', 'Socket.io', 'MongoDB'],
                'estimated_time': '4-5 weeks',
                'why_recommended': 'Showcases real-time communication implementation'
            },
            {
                'title': 'AI Image Caption Generator',
                'description': 'Create an app that generates captions for uploaded images using ML',
                'difficulty': 'Advanced',
                'skills_needed': ['Python', 'TensorFlow', 'Flask', 'React'],
                'estimated_time': '5-7 weeks',
                'why_recommended': 'Demonstrates AI/ML capabilities and deployment skills'
            }
        ]
        
        return project_templates[:count]
    
    def generate_implementation_guide(self, project_title, skills):
        """Generate detailed implementation guide"""
        
        guide = {
            'project_title': project_title,
            'overview': f'Comprehensive guide to build {project_title}',
            'steps': [
                {
                    'step': 1,
                    'title': 'Setup and Planning',
                    'description': 'Set up development environment and plan architecture',
                    'tasks': [
                        'Initialize Git repository',
                        'Set up project structure',
                        'Install dependencies',
                        'Create database schema'
                    ]
                },
                {
                    'step': 2,
                    'title': 'Backend Development',
                    'description': 'Build API endpoints and business logic',
                    'tasks': [
                        'Create REST API routes',
                        'Implement authentication',
                        'Set up database connections',
                        'Write unit tests'
                    ]
                },
                {
                    'step': 3,
                    'title': 'Frontend Development',
                    'description': 'Build user interface and integrate with backend',
                    'tasks': [
                        'Design UI components',
                        'Implement routing',
                        'Connect to API',
                        'Add error handling'
                    ]
                },
                {
                    'step': 4,
                    'title': 'Testing and Deployment',
                    'description': 'Test thoroughly and deploy to production',
                    'tasks': [
                        'Write integration tests',
                        'Fix bugs and optimize',
                        'Set up CI/CD pipeline',
                        'Deploy to cloud platform'
                    ]
                }
            ],
            'resources': [
                'Official documentation',
                'YouTube tutorials',
                'Stack Overflow community',
                'GitHub example projects'
            ]
        }
        
        return guide
    
    def generate_roadmap_tips(self, job_title, missing_skills):
        """Generate AI-powered learning tips"""
        
        tips = [
            f'Focus on mastering {missing_skills[0]} first as it\'s fundamental for {job_title}',
            'Build projects while learning to reinforce concepts',
            'Join online communities and participate in discussions',
            'Contribute to open-source projects to gain real-world experience',
            'Create a learning schedule and stick to it consistently'
        ]
        
        return tips
    
    def generate_shadowing_intro(self, job_role):
        """Generate introduction message for job shadowing"""
        
        intros = {
            'Data Scientist': 'Welcome to your virtual Data Scientist experience! I\'m Alex, a Senior Data Scientist at TechCorp. Today, you\'ll shadow me as I work on analyzing customer churn patterns. What would you like to know about a typical day in this role?',
            'Software Engineer': 'Hi! I\'m Jordan, a Software Engineer working on our mobile app. Today we\'re debugging a performance issue and planning a new feature. Ready to see what software engineering is really like?',
            'Product Manager': 'Hello! I\'m Sam, a Product Manager here. Today involves stakeholder meetings, reviewing user feedback, and prioritizing our product roadmap. What aspects of product management interest you most?'
        }
        
        return intros.get(job_role, f'Welcome to your virtual {job_role} experience! Let me show you what a day in this role looks like.')
    
    def generate_shadowing_response(self, job_role, user_message, conversation_history):
        """Generate contextual response for job shadowing chat"""
        
        # Mock AI response - in production, use GPT/Gemini with conversation context
        responses = [
            f'Great question! As a {job_role}, I typically start my day by checking emails and planning priorities...',
            'That\'s a common challenge in this role. Here\'s how I usually approach it...',
            'Let me walk you through a real scenario I dealt with last week...',
            'The skills you need most are definitely technical expertise, but communication is equally important...'
        ]
        
        return responses[len(conversation_history) % len(responses)]
    
    def generate_job_scenarios(self, job_role):
        """Generate realistic job scenarios"""
        
        scenarios = [
            {
                'scenario_id': 1,
                'title': 'Morning Standup',
                'description': 'Participate in daily team standup meeting',
                'type': 'Meeting',
                'duration': '15 minutes'
            },
            {
                'scenario_id': 2,
                'title': 'Code Review',
                'description': 'Review a colleague\'s pull request and provide feedback',
                'type': 'Technical',
                'duration': '30 minutes'
            },
            {
                'scenario_id': 3,
                'title': 'Problem Solving',
                'description': 'Debug a production issue reported by users',
                'type': 'Technical',
                'duration': '1-2 hours'
            },
            {
                'scenario_id': 4,
                'title': 'Client Meeting',
                'description': 'Present project progress to stakeholders',
                'type': 'Meeting',
                'duration': '45 minutes'
            }
        ]
        
        return scenarios
