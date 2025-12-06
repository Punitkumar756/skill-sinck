from services.ai_service import AIService
import uuid
from datetime import datetime

class VirtualShadowingService:
    """Virtual job shadowing with AI chatbot"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.sessions = {}
    
    def start_shadowing_session(self, user_id, job_role):
        """Start a virtual shadowing session"""
        
        session_id = str(uuid.uuid4())
        
        # Get initial scenario from AI
        intro_message = self.ai_service.generate_shadowing_intro(job_role)
        
        session = {
            'session_id': session_id,
            'user_id': user_id,
            'job_role': job_role,
            'started_at': datetime.utcnow().isoformat(),
            'conversation_history': [
                {
                    'role': 'assistant',
                    'message': intro_message,
                    'timestamp': datetime.utcnow().isoformat()
                }
            ],
            'scenarios_completed': 0
        }
        
        self.sessions[session_id] = session
        
        return session
    
    def chat(self, session_id, message):
        """Chat with AI about the job role"""
        
        session = self.sessions.get(session_id)
        
        if not session:
            return {'error': 'Session not found'}
        
        # Add user message to history
        session['conversation_history'].append({
            'role': 'user',
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Get AI response
        job_role = session['job_role']
        conversation_history = session['conversation_history']
        
        ai_response = self.ai_service.generate_shadowing_response(
            job_role, 
            message, 
            conversation_history
        )
        
        # Add AI response to history
        session['conversation_history'].append({
            'role': 'assistant',
            'message': ai_response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return ai_response
    
    def get_job_scenarios(self, job_role):
        """Get realistic scenarios for a job role"""
        
        scenarios = self.ai_service.generate_job_scenarios(job_role)
        
        return scenarios
    
    def get_session(self, session_id):
        """Get session details"""
        return self.sessions.get(session_id)
    
    def end_session(self, session_id):
        """End a shadowing session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session['ended_at'] = datetime.utcnow().isoformat()
            return session
        return None
