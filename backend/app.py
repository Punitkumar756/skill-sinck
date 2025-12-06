from flask import Flask, jsonify
from flask_cors import CORS
from routes.profile_routes import profile_bp
from routes.quiz_routes import quiz_bp
from routes.job_routes import job_bp
from routes.roadmap_routes import roadmap_bp
from routes.portfolio_routes import portfolio_bp
from routes.shadowing_routes import shadowing_bp
from routes.admin_routes import admin_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register Blueprints
app.register_blueprint(profile_bp, url_prefix='/api/profile')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
app.register_blueprint(job_bp, url_prefix='/api/jobs')
app.register_blueprint(roadmap_bp, url_prefix='/api/roadmap')
app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
app.register_blueprint(shadowing_bp, url_prefix='/api/shadowing')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/')
def home():
    return jsonify({
        'message': 'SkillSync AI - Career GPS API',
        'version': '1.0.0',
        'status': 'active'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
