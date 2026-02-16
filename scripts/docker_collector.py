import docker
from app.models import db, DockerStats
from app.app import app

def fetch_docker_stats():
    client = docker.from_env()
    containers = client.containers.list(all=True)
    
    with app.app_context():
        for container in containers:
            name = container.name
            status = container.status
            
            # Simple resource usage (stats() is blocking, usually we want a snapshot)
            try:
                # This fetches a single stat update
                stats = container.stats(stream=False)
                cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
                system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                cpu_usage = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0.0
                
                mem_usage = stats['memory_stats']['usage'] / (1024 * 1024) # MB
            except:
                cpu_usage = 0.0
                mem_usage = 0.0
            
            stat = DockerStats.query.filter_by(container_name=name).first()
            if not stat:
                stat = DockerStats(container_name=name)
                db.session.add(stat)
            
            stat.status = status
            stat.cpu_usage = cpu_usage
            stat.memory_usage = mem_usage
        
        db.session.commit()
    print("Updated Docker stats")

if __name__ == "__main__":
    fetch_docker_stats()
