import random
from datetime import datetime

class QuizService:
    """Psychometric quiz service for career path discovery"""
    
    def __init__(self):
        self.quiz_results = {}
        self.career_mapping = {
            'analytical': ['Data Scientist', 'Data Analyst', 'Business Analyst', 'Research Scientist'],
            'creative': ['UX Designer', 'Product Designer', 'Content Creator', 'Marketing Specialist'],
            'technical': ['Software Engineer', 'DevOps Engineer', 'System Administrator', 'Cloud Architect'],
            'leadership': ['Product Manager', 'Project Manager', 'Team Lead', 'Scrum Master'],
            'problem_solving': ['Software Developer', 'Machine Learning Engineer', 'Solutions Architect'],
            'communication': ['Technical Writer', 'Developer Advocate', 'Sales Engineer', 'Customer Success Manager']
        }
    
    def get_quiz_questions(self):
        """Get psychometric quiz questions"""
        questions = [
            {
                'id': 1,
                'question': 'I enjoy analyzing data and finding patterns',
                'type': 'analytical',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 2,
                'question': 'I prefer creating visual designs and user experiences',
                'type': 'creative',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 3,
                'question': 'I like working with code and building technical solutions',
                'type': 'technical',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 4,
                'question': 'I enjoy leading teams and coordinating projects',
                'type': 'leadership',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 5,
                'question': 'I thrive on solving complex technical problems',
                'type': 'problem_solving',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 6,
                'question': 'I excel at explaining technical concepts to others',
                'type': 'communication',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 7,
                'question': 'I prefer working with numbers and statistics',
                'type': 'analytical',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 8,
                'question': 'I enjoy brainstorming innovative ideas',
                'type': 'creative',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 9,
                'question': 'I am comfortable with system architecture and infrastructure',
                'type': 'technical',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            },
            {
                'id': 10,
                'question': 'I like making strategic decisions and planning',
                'type': 'leadership',
                'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
            }
        ]
        
        return questions
    
    def analyze_quiz(self, user_id, answers):
        """Analyze quiz answers and recommend careers"""
        
        # Calculate scores for each trait
        trait_scores = {}
        
        for answer in answers:
            question_id = answer['question_id']
            response = answer['response']
            
            # Get question type
            questions = self.get_quiz_questions()
            question = next((q for q in questions if q['id'] == question_id), None)
            
            if question:
                trait = question['type']
                score = self._convert_response_to_score(response)
                
                if trait not in trait_scores:
                    trait_scores[trait] = []
                trait_scores[trait].append(score)
        
        # Average scores per trait
        avg_scores = {trait: sum(scores)/len(scores) for trait, scores in trait_scores.items()}
        
        # Get top 3 traits
        top_traits = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Recommend careers based on top traits
        recommended_careers = []
        for trait, score in top_traits:
            careers = self.career_mapping.get(trait, [])
            for career in careers:
                if career not in recommended_careers:
                    recommended_careers.append({
                        'title': career,
                        'match_score': round(score * 20, 1),  # Convert to percentage
                        'trait': trait
                    })
        
        results = {
            'user_id': user_id,
            'trait_scores': avg_scores,
            'top_traits': [trait for trait, _ in top_traits],
            'recommended_careers': recommended_careers[:10],
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        # Store results
        self.quiz_results[user_id] = results
        
        return results
    
    def _convert_response_to_score(self, response):
        """Convert text response to numerical score"""
        score_map = {
            'Strongly Disagree': 1,
            'Disagree': 2,
            'Neutral': 3,
            'Agree': 4,
            'Strongly Agree': 5
        }
        return score_map.get(response, 3)
    
    def get_user_results(self, user_id):
        """Get quiz results for a user"""
        return self.quiz_results.get(user_id)
