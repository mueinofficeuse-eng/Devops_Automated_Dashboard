import requests
import os
from app.models import db, JenkinsStats
from app.app import app

JENKINS_URL = os.getenv('JENKINS_URL', 'http://localhost:8080')
JENKINS_USER = os.getenv('JENKINS_USER', 'admin')
JENKINS_TOKEN = os.getenv('JENKINS_TOKEN')

def fetch_jenkins_stats():
    # Jenkins API for jobs
    url = f"{JENKINS_URL}/api/json?tree=jobs[name,color,lastBuild[number,duration,timestamp]]"
    auth = (JENKINS_USER, JENKINS_TOKEN) if JENKINS_TOKEN else None
    
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            jobs = response.json().get('jobs', [])
            
            with app.app_context():
                for job in jobs:
                    name = job['name']
                    color = job['color']
                    # color: 'blue' (success), 'red' (failure), 'aborted', etc.
                    status = "SUCCESS" if color == "blue" else "FAILURE" if color == "red" else "RUNNING" if "anime" in color else "UNKNOWN"
                    
                    last_build = job.get('lastBuild')
                    build_num = last_build['number'] if last_build else 0
                    duration = last_build['duration'] / 1000.0 if last_build else 0 # ms to s
                    
                    stat = JenkinsStats.query.filter_by(job_name=name).first()
                    if not stat:
                        stat = JenkinsStats(job_name=name)
                        db.session.add(stat)
                    
                    stat.status = status
                    stat.last_build_number = build_num
                    stat.duration = duration
                
                db.session.commit()
            print("Updated Jenkins stats")
    except Exception as e:
        print(f"Error fetching Jenkins stats: {e}")

if __name__ == "__main__":
    fetch_jenkins_stats()
