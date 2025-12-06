from flask import Blueprint, request, jsonify
from services.quiz_service import QuizService

quiz_bp = Blueprint('quiz', __name__)
quiz_service = QuizService()

@quiz_bp.route('/start', methods=['GET'])
def start_quiz():
    """Get psychometric quiz questions"""
    try:
        questions = quiz_service.get_quiz_questions()
        return jsonify({
            'questions': questions,
            'total': len(questions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and get career recommendations"""
    try:
        data = request.json
        user_id = data.get('user_id')
        answers = data.get('answers')
        
        if not user_id or not answers:
            return jsonify({'error': 'User ID and answers required'}), 400
        
        # Analyze answers and get career recommendations
        results = quiz_service.analyze_quiz(user_id, answers)
        
        return jsonify({
            'message': 'Quiz analyzed successfully',
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/results/<user_id>', methods=['GET'])
def get_results(user_id):
    """Get quiz results for a user"""
    try:
        results = quiz_service.get_user_results(user_id)
        
        if not results:
            return jsonify({'error': 'No quiz results found'}), 404
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
