import requests
import os
from app.models import db, GitHubStats
from app.app import app

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER', 'octocat')
REPO_NAME = os.getenv('REPO_NAME', 'hello-world')

def fetch_github_stats():
    # Fetch Commits
    commits_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    
    response = requests.get(commits_url, headers=headers)
    commits_count = len(response.json()) if response.status_code == 200 else 0
    
    # Fetch PRs
    prs_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    response = requests.get(prs_url, headers=headers)
    open_prs = len(response.json()) if response.status_code == 200 else 0
    
    with app.app_context():
        stat = GitHubStats.query.filter_by(repo_name=REPO_NAME).first()
        if not stat:
            stat = GitHubStats(repo_name=REPO_NAME)
            db.session.add(stat)
        
        stat.commits_count = commits_count
        stat.open_prs = open_prs
        db.session.commit()
    
    print(f"Updated GitHub stats for {REPO_NAME}")

if __name__ == "__main__":
    fetch_github_stats()
