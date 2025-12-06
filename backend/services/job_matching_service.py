from models.job import Job, JobMatch
from services.profile_service import ProfileService
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatchingService:
    """AI-powered job matching engine"""
    
    def __init__(self):
        self.profile_service = ProfileService()
        # Mock job database
        self.jobs = self._initialize_sample_jobs()
    
    def _initialize_sample_jobs(self):
        """Initialize sample jobs for demonstration"""
        jobs = [
            Job(
                job_id='job_001',
                title='Data Analyst',
                company='Tech Corp',
                description='Analyze data and create insights',
                required_skills=['Python', 'SQL', 'Pandas', 'Data Analysis', 'Excel'],
                location='Remote'
            ),
            Job(
                job_id='job_002',
                title='Frontend Developer',
                company='Web Solutions',
                description='Build responsive web applications',
                required_skills=['JavaScript', 'React', 'HTML', 'CSS', 'Git'],
                location='New York'
            ),
            Job(
                job_id='job_003',
                title='Machine Learning Engineer',
                company='AI Innovations',
                description='Develop ML models and deploy them',
                required_skills=['Python', 'Machine Learning', 'TensorFlow', 'Scikit-Learn', 'AWS'],
                location='San Francisco'
            ),
            Job(
                job_id='job_004',
                title='Full Stack Developer',
                company='StartupXYZ',
                description='Work on both frontend and backend',
                required_skills=['JavaScript', 'React', 'Node.js', 'MongoDB', 'REST API'],
                location='Remote'
            ),
            Job(
                job_id='job_005',
                title='DevOps Engineer',
                company='Cloud Systems',
                description='Manage cloud infrastructure and CI/CD',
                required_skills=['Docker', 'Kubernetes', 'AWS', 'Python', 'Git'],
                location='Austin'
            )
        ]
        
        return {job.job_id: job for job in jobs}
    
    def search_jobs(self, query='', location=''):
        """Search for jobs based on query and location"""
        results = []
        
        for job in self.jobs.values():
            # Simple search logic
            if query.lower() in job.title.lower() or query.lower() in job.description.lower():
                if not location or location.lower() in job.location.lower() or job.location == 'Remote':
                    results.append(job.to_dict())
            elif not query:  # If no query, return all matching location
                if not location or location.lower() in job.location.lower() or job.location == 'Remote':
                    results.append(job.to_dict())
        
        return results
    
    def get_job_matches(self, user_id):
        """Get all job matches for a user, sorted by match percentage"""
        matches = []
        
        for job_id in self.jobs.keys():
            match_data = self.calculate_job_match(user_id, job_id)
            matches.append(match_data)
        
        # Sort by match percentage
        matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return matches
    
    def calculate_job_match(self, user_id, job_id):
        """Calculate match percentage between user and job"""
        
        # Get user skills
        user_skills = self.profile_service.get_user_skills(user_id)
        
        # Get job requirements
        job = self.jobs.get(job_id)
        if not job:
            return {'error': 'Job not found'}
        
        required_skills = [skill.lower() for skill in job.required_skills]
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        # Calculate matching skills
        matching_skills = list(set(user_skills_lower) & set(required_skills))
        missing_skills = list(set(required_skills) - set(user_skills_lower))
        
        # Calculate match percentage
        if len(required_skills) > 0:
            match_percentage = round((len(matching_skills) / len(required_skills)) * 100, 1)
        else:
            match_percentage = 0
        
        # Create match object
        match = JobMatch(
            job_id=job_id,
            user_id=user_id,
            match_percentage=match_percentage,
            matching_skills=[s.title() for s in matching_skills],
            missing_skills=[s.title() for s in missing_skills]
        )
        
        result = match.to_dict()
        result['job'] = job.to_dict()
        
        return result
    
    def get_job_by_id(self, job_id):
        """Get job details by ID"""
        job = self.jobs.get(job_id)
        return job.to_dict() if job else None
    
    def add_job(self, job_data):
        """Add a new job (for admin use)"""
        job = Job(
            job_id=job_data['job_id'],
            title=job_data['title'],
            company=job_data['company'],
            description=job_data['description'],
            required_skills=job_data['required_skills'],
            location=job_data.get('location', 'Remote')
        )
        
        self.jobs[job.job_id] = job
        return job.to_dict()
