from flask import Blueprint, request, jsonify
from services.resume_parser import ResumeParser
from services.profile_service import ProfileService
import os

profile_bp = Blueprint('profile', __name__)
resume_parser = ResumeParser()
profile_service = ProfileService()

@profile_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume to extract skills and experience"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        user_id = request.form.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Parse resume
        profile_data = resume_parser.parse(file)
        
        # Save profile
        profile = profile_service.create_or_update_profile(user_id, profile_data)
        
        return jsonify({
            'message': 'Resume parsed successfully',
            'profile': profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/manual-entry', methods=['POST'])
def manual_entry():
    """Manual profile creation"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        profile = profile_service.create_or_update_profile(user_id, data)
        
        return jsonify({
            'message': 'Profile created successfully',
            'profile': profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    try:
        profile = profile_service.get_profile(user_id)
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify(profile), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<user_id>', methods=['PUT'])
def update_profile(user_id):
    """Update user profile"""
    try:
        data = request.json
        profile = profile_service.create_or_update_profile(user_id, data)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
