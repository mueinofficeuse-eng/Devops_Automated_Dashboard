#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting DevOps Dashboard Setup for Amazon Linux 2023..."

# 1. Update system
sudo dnf update -y

# 2. Install Python and Git
sudo dnf install -y python3-pip git

# 3. Install Docker
sudo dnf install -y docker
sudo systemctl start docker
sudo systemctl enable docker
# Allow current user to run docker without sudo (requires logout/login)
sudo usermod -aG docker $USER

# 4. Install Docker Compose (v2)
sudo dnf install -y docker-compose-plugin

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "⚠️ IMPORTANT: Please log out and log back in to use Docker without sudo."
echo "💡 To run the dashboard, execute: source venv/bin/activate && python3 -m app.app"
