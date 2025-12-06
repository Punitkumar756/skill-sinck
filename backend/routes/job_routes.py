from flask import Blueprint, request, jsonify
from services.job_matching_service import JobMatchingService

job_bp = Blueprint('jobs', __name__)
job_service = JobMatchingService()

@job_bp.route('/search', methods=['GET'])
def search_jobs():
    """Search for available jobs"""
    try:
        query = request.args.get('query', '')
        location = request.args.get('location', '')
        
        jobs = job_service.search_jobs(query, location)
        
        return jsonify({
            'jobs': jobs,
            'count': len(jobs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/match/<user_id>', methods=['GET'])
def get_matches(user_id):
    """Get job matches for a user"""
    try:
        matches = job_service.get_job_matches(user_id)
        
        return jsonify({
            'matches': matches,
            'count': len(matches)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/match/<user_id>/<job_id>', methods=['GET'])
def calculate_match(user_id, job_id):
    """Calculate match percentage for specific job"""
    try:
        match_data = job_service.calculate_job_match(user_id, job_id)
        
        return jsonify(match_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_bp.route('/<job_id>', methods=['GET'])
def get_job_details(job_id):
    """Get detailed job information"""
    try:
        job = job_service.get_job_by_id(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
