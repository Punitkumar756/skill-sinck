from flask import Blueprint, request, jsonify
from services.portfolio_service import PortfolioService

portfolio_bp = Blueprint('portfolio', __name__)
portfolio_service = PortfolioService()

@portfolio_bp.route('/generate-ideas/<user_id>', methods=['GET'])
def generate_project_ideas(user_id):
    """Generate personalized project ideas based on interests"""
    try:
        count = request.args.get('count', 5, type=int)
        
        project_ideas = portfolio_service.generate_project_ideas(user_id, count)
        
        return jsonify({
            'project_ideas': project_ideas,
            'count': len(project_ideas)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/project-details', methods=['POST'])
def get_project_details():
    """Get detailed implementation guide for a project idea"""
    try:
        data = request.json
        project_title = data.get('project_title')
        user_id = data.get('user_id')
        
        if not project_title or not user_id:
            return jsonify({'error': 'Project title and user ID required'}), 400
        
        details = portfolio_service.get_project_implementation_guide(project_title, user_id)
        
        return jsonify(details), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/save-project', methods=['POST'])
def save_project():
    """Save a completed project to portfolio"""
    try:
        data = request.json
        user_id = data.get('user_id')
        project_data = data.get('project_data')
        
        if not user_id or not project_data:
            return jsonify({'error': 'User ID and project data required'}), 400
        
        portfolio = portfolio_service.add_project_to_portfolio(user_id, project_data)
        
        return jsonify({
            'message': 'Project saved successfully',
            'portfolio': portfolio
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/<user_id>', methods=['GET'])
def get_portfolio(user_id):
    """Get user's project portfolio"""
    try:
        portfolio = portfolio_service.get_user_portfolio(user_id)
        
        return jsonify(portfolio), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
