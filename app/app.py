import os
from flask import Flask, render_template, jsonify
from app.models import db, GitHubStats, JenkinsStats, DockerStats
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# 1. Database Configuration
# We tell Flask where our PostgreSQL database is located.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://devops_user:devops_password@localhost:5432/devops_dashboard')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Connect the Database to our App
db.init_app(app)

# 3. Create Tables automatically if they don't exist
with app.app_context():
    db.create_all()

# 4. Route: The main page
@app.route('/')
def index():
    return render_template('index.html')

# 5. Route: The "API" that sends data to our Dashboard
@app.route('/api/stats')
def get_stats():
    github = GitHubStats.query.all()
    jenkins = JenkinsStats.query.all()
    docker = DockerStats.query.all()
    
    return jsonify({
        'github': [{'repo': g.repo_name, 'commits': g.commits_count, 'prs': g.open_prs} for g in github],
        'jenkins': [{'job': j.job_name, 'status': j.status, 'build': j.last_build_number} for j in jenkins],
        'docker': [{'name': d.container_name, 'status': d.status, 'cpu': d.cpu_usage, 'mem': d.memory_usage} for d in docker]
    })

if __name__ == '__main__':
    # host='0.0.0.0' allows external access on AWS
    app.run(host='0.0.0.0', debug=True, port=5001)
