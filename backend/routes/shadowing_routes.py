from flask import Blueprint, request, jsonify
from services.virtual_shadowing_service import VirtualShadowingService

shadowing_bp = Blueprint('shadowing', __name__)
shadowing_service = VirtualShadowingService()

@shadowing_bp.route('/start-session', methods=['POST'])
def start_session():
    """Start a virtual shadowing session for a specific job role"""
    try:
        data = request.json
        user_id = data.get('user_id')
        job_role = data.get('job_role')
        
        if not user_id or not job_role:
            return jsonify({'error': 'User ID and job role required'}), 400
        
        session = shadowing_service.start_shadowing_session(user_id, job_role)
        
        return jsonify({
            'message': 'Shadowing session started',
            'session': session
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shadowing_bp.route('/chat', methods=['POST'])
def chat():
    """Chat with AI about the job role"""
    try:
        data = request.json
        session_id = data.get('session_id')
        message = data.get('message')
        
        if not session_id or not message:
            return jsonify({'error': 'Session ID and message required'}), 400
        
        response = shadowing_service.chat(session_id, message)
        
        return jsonify({
            'response': response
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shadowing_bp.route('/scenarios/<job_role>', methods=['GET'])
def get_scenarios(job_role):
    """Get realistic scenarios for a job role"""
    try:
        scenarios = shadowing_service.get_job_scenarios(job_role)
        
        return jsonify({
            'scenarios': scenarios
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shadowing_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get shadowing session details"""
    try:
        session = shadowing_service.get_session(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify(session), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
