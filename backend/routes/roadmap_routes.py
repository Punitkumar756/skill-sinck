from flask import Blueprint, request, jsonify
from services.roadmap_service import RoadmapService

roadmap_bp = Blueprint('roadmap', __name__)
roadmap_service = RoadmapService()

@roadmap_bp.route('/generate/<user_id>', methods=['POST'])
def generate_roadmap(user_id):
    """Generate personalized learning roadmap"""
    try:
        data = request.json
        target_job_id = data.get('target_job_id')
        
        if not target_job_id:
            return jsonify({'error': 'Target job ID required'}), 400
        
        roadmap = roadmap_service.generate_roadmap(user_id, target_job_id)
        
        return jsonify({
            'message': 'Roadmap generated successfully',
            'roadmap': roadmap
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@roadmap_bp.route('/<user_id>', methods=['GET'])
def get_roadmap(user_id):
    """Get user's learning roadmap"""
    try:
        roadmap = roadmap_service.get_user_roadmap(user_id)
        
        if not roadmap:
            return jsonify({'error': 'No roadmap found'}), 404
        
        return jsonify(roadmap), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@roadmap_bp.route('/progress/<user_id>', methods=['PUT'])
def update_progress(user_id):
    """Update learning progress"""
    try:
        data = request.json
        skill_id = data.get('skill_id')
        status = data.get('status')  # 'completed', 'in-progress', 'not-started'
        
        roadmap = roadmap_service.update_progress(user_id, skill_id, status)
        
        return jsonify({
            'message': 'Progress updated successfully',
            'roadmap': roadmap
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
