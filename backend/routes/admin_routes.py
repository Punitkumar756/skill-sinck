from flask import Blueprint, request, jsonify
from services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)
admin_service = AdminService()

@admin_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get university analytics dashboard data"""
    try:
        university_id = request.args.get('university_id')
        
        if not university_id:
            return jsonify({'error': 'University ID required'}), 400
        
        analytics = admin_service.get_university_analytics(university_id)
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/student-interests', methods=['GET'])
def get_student_interests():
    """Get aggregated student interests data"""
    try:
        university_id = request.args.get('university_id')
        
        if not university_id:
            return jsonify({'error': 'University ID required'}), 400
        
        interests = admin_service.get_student_interests(university_id)
        
        return jsonify({
            'interests': interests
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/skill-gaps', methods=['GET'])
def get_skill_gaps():
    """Get common skill gaps across students"""
    try:
        university_id = request.args.get('university_id')
        
        if not university_id:
            return jsonify({'error': 'University ID required'}), 400
        
        skill_gaps = admin_service.get_skill_gap_analysis(university_id)
        
        return jsonify({
            'skill_gaps': skill_gaps
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/career-trends', methods=['GET'])
def get_career_trends():
    """Get trending career paths among students"""
    try:
        university_id = request.args.get('university_id')
        
        if not university_id:
            return jsonify({'error': 'University ID required'}), 400
        
        trends = admin_service.get_career_trends(university_id)
        
        return jsonify({
            'trends': trends
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/export-report', methods=['GET'])
def export_report():
    """Export analytics report"""
    try:
        university_id = request.args.get('university_id')
        report_type = request.args.get('type', 'comprehensive')
        
        if not university_id:
            return jsonify({'error': 'University ID required'}), 400
        
        report = admin_service.generate_report(university_id, report_type)
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
