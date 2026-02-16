async function updateDashboard() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        // Update GitHub
        const githubContainer = document.getElementById('github-stats');
        if (data.github.length > 0) {
            githubContainer.innerHTML = data.github.map(repo => `
                <div class="stat-item">
                    <span class="stat-value">${repo.commits}</span>
                    <span class="stat-label">Commits</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">${repo.prs}</span>
                    <span class="stat-label">Pull Requests</span>
                </div>
            `).join('');
            initGitHubChart(data.github[0]);
        }

        // Update Jenkins
        const jenkinsContainer = document.getElementById('jenkins-list');
        jenkinsContainer.innerHTML = data.jenkins.map(job => `
            <div class="status-row">
                <div class="job-info">
                    <p style="font-weight: 600;">${job.job}</p>
                    <p style="font-size: 0.8rem; color: var(--text-muted);">Build #${job.build}</p>
                </div>
                <span class="badge ${job.status === 'SUCCESS' ? 'badge-success' : 'badge-danger'}">${job.status}</span>
            </div>
        `).join('') || '<p>No jobs found</p>';

        // Update Docker
        const dockerContainer = document.getElementById('docker-list');
        dockerContainer.innerHTML = data.docker.map(container => `
            <div class="status-row container-item">
                <div style="display: flex; justify-content: space-between; width: 100%;">
                    <span>${container.name}</span>
                    <span class="badge ${container.status === 'running' ? 'badge-success' : 'badge-danger'}">${container.status}</span>
                </div>
                <div style="width: 100%;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem;">
                        <span color: var(--text-muted)>CPU: ${container.cpu.toFixed(1)}%</span>
                        <span color: var(--text-muted)>RAM: ${container.mem.toFixed(1)}MB</span>
                    </div>
                    <div class="usage-bar">
                        <div class="usage-fill" style="width: ${container.cpu}%"></div>
                    </div>
                </div>
            </div>
        `).join('') || '<p>No containers found</p>';

    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

let githubChart;
function initGitHubChart(repo) {
    const ctx = document.getElementById('githubChart').getContext('2d');
    if (githubChart) githubChart.destroy();
    
    githubChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Commits', 'PRs'],
            datasets: [{
                data: [repo.commits, repo.prs],
                backgroundColor: ['#6366f1', '#a855f7'],
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94a3b8' } }
            },
            cutout: '70%'
        }
    });
}

document.getElementById('refresh-btn').addEventListener('click', updateDashboard);

// Initial load
updateDashboard();
// Auto update every 30 seconds
setInterval(updateDashboard, 30000);
