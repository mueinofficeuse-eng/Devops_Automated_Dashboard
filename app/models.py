from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class GitHubStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(100), nullable=False)
    commits_count = db.Column(db.Integer, default=0)
    open_prs = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class JenkinsStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20)) # SUCCESS, FAILURE, ABORTED
    last_build_number = db.Column(db.Integer)
    duration = db.Column(db.Float) # in seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class DockerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20)) # running, exited
    cpu_usage = db.Column(db.Float)
    memory_usage = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
