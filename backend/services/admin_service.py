from services.profile_service import ProfileService
from services.quiz_service import QuizService
from collections import Counter

class AdminService:
    """Admin dashboard analytics service"""
    
    def __init__(self):
        self.profile_service = ProfileService()
        self.quiz_service = QuizService()
    
    def get_university_analytics(self, university_id):
        """Get comprehensive analytics for university"""
        
        # Mock data - in production, filter by university_id from database
        analytics = {
            'university_id': university_id,
            'total_students': 1250,
            'active_users': 890,
            'completed_profiles': 750,
            'completed_quizzes': 680,
            'avg_match_percentage': 72.5,
            'top_career_interests': [
                {'career': 'Software Engineer', 'count': 285},
                {'career': 'Data Scientist', 'count': 198},
                {'career': 'Product Manager', 'count': 156},
                {'career': 'UX Designer', 'count': 142},
                {'career': 'DevOps Engineer', 'count': 121}
            ],
            'engagement_metrics': {
                'daily_active_users': 234,
                'weekly_active_users': 567,
                'monthly_active_users': 890
            }
        }
        
        return analytics
    
    def get_student_interests(self, university_id):
        """Get aggregated student interests data"""
        
        # Mock aggregated interests
        interests = [
            {'interest': 'Machine Learning', 'count': 340, 'percentage': 27.2},
            {'interest': 'Web Development', 'count': 425, 'percentage': 34.0},
            {'interest': 'Data Analysis', 'count': 298, 'percentage': 23.8},
            {'interest': 'Cloud Computing', 'count': 267, 'percentage': 21.4},
            {'interest': 'Mobile Development', 'count': 223, 'percentage': 17.8},
            {'interest': 'Cybersecurity', 'count': 189, 'percentage': 15.1},
            {'interest': 'UI/UX Design', 'count': 245, 'percentage': 19.6}
        ]
        
        return interests
    
    def get_skill_gap_analysis(self, university_id):
        """Get common skill gaps across students"""
        
        # Mock skill gap analysis
        skill_gaps = [
            {
                'skill': 'Cloud Platforms (AWS/Azure)',
                'gap_percentage': 68.5,
                'students_lacking': 856,
                'priority': 'High',
                'recommendation': 'Add cloud computing module to curriculum'
            },
            {
                'skill': 'System Design',
                'gap_percentage': 72.3,
                'students_lacking': 904,
                'priority': 'High',
                'recommendation': 'Introduce system design workshops'
            },
            {
                'skill': 'Docker/Kubernetes',
                'gap_percentage': 81.2,
                'students_lacking': 1015,
                'priority': 'High',
                'recommendation': 'Create DevOps specialization track'
            },
            {
                'skill': 'Advanced SQL',
                'gap_percentage': 45.6,
                'students_lacking': 570,
                'priority': 'Medium',
                'recommendation': 'Enhance database courses'
            },
            {
                'skill': 'API Development',
                'gap_percentage': 52.1,
                'students_lacking': 651,
                'priority': 'Medium',
                'recommendation': 'Add REST API development projects'
            }
        ]
        
        return skill_gaps
    
    def get_career_trends(self, university_id):
        """Get trending career paths among students"""
        
        trends = [
            {
                'career': 'Machine Learning Engineer',
                'trend': 'Rising',
                'growth': '+42%',
                'current_interest': 198,
                'previous_period': 139
            },
            {
                'career': 'Cloud Architect',
                'trend': 'Rising',
                'growth': '+38%',
                'current_interest': 156,
                'previous_period': 113
            },
            {
                'career': 'Full Stack Developer',
                'trend': 'Stable',
                'growth': '+5%',
                'current_interest': 285,
                'previous_period': 271
            },
            {
                'career': 'Data Analyst',
                'trend': 'Rising',
                'growth': '+28%',
                'current_interest': 223,
                'previous_period': 174
            },
            {
                'career': 'DevOps Engineer',
                'trend': 'Rising',
                'growth': '+51%',
                'current_interest': 181,
                'previous_period': 120
            }
        ]
        
        return trends
    
    def generate_report(self, university_id, report_type='comprehensive'):
        """Generate analytics report for export"""
        
        report = {
            'university_id': university_id,
            'report_type': report_type,
            'generated_at': '2025-12-06T10:30:00Z',
            'analytics': self.get_university_analytics(university_id),
            'student_interests': self.get_student_interests(university_id),
            'skill_gaps': self.get_skill_gap_analysis(university_id),
            'career_trends': self.get_career_trends(university_id),
            'recommendations': [
                'Introduce cloud computing certification programs',
                'Partner with industry for real-world project exposure',
                'Organize ML/AI bootcamps and workshops',
                'Update curriculum to include DevOps practices',
                'Create mentorship programs with industry professionals'
            ]
        }
        
        return report
