# 🚀 DIY DevOps Dashboard 

A professional-grade DevOps Dashboard from scratch. 

---

## ☁️ AWS Setup (Amazon Linux 2023)

If you are using this on an **AWS EC2 (Amazon Linux 2023)** instance, follow these steps:

### 1. Security Group Configuration
Ensure your EC2 Security Group has the following ports open (Inbound rules):
- `5001`: Dashboard Web UI
- `8080`: Jenkins Web UI
- `5432`: PostgreSQL (Only if you need external access)

### 2. Automated Setup
I've included a script to handle all installations (`dnf`, `docker`, `python3`):
```bash
chmod +x setup_aws.sh
./setup_aws.sh
```
*Note: You may need to logout and log back in for Docker permissions to take effect.*

---

## 📁 Project Structure 

- `app/`: The "Brain" - where the Flask web server and Database models live.
- `scripts/`: The "Hands" - Python scripts that reach out to GitHub, Jenkins, and Docker to grab data.
- `static/ & templates/`: The "Face" - The HTML and CSS that make the dashboard look beautiful.
- `docker-compose.yml`: The "Foundation" - A single file that sets up your Database (PostgreSQL) and Jenkins automatically.

---

## 🛠️ Phase 1: Prepare Your Environment

Before we start, make sure you have **Python 3** and **Docker Desktop** installed on your Machine.

### 1. Create a Virtual Environment
This keeps your project's libraries separate from your computer's system libraries.
```bash
cd devops_dashboard
python3 -m venv venv
source venv/bin/activate
```
*You should now see `(venv)` at the start of your terminal line.*

### 2. Install the Libraries
```bash
pip install -r requirements.txt
```

---

## 🐳 Phase 2: Launch the Infrastructure

We need a database to store our data and Jenkins to monitor builds. Docker makes this easy.

1.  **Open Docker Desktop** and make sure it's running.
2.  **Start the services**:
    ```bash
    docker-compose up -d
    ```
    - `db`: A PostgreSQL database will start on port 5432.
    - `jenkins`: Jenkins will start on port 8080.

---

## 🔑 Phase 3: Get Your API Keys (Crucial Step)

The dashboard needs permission to talk to external tools.

### 1. GitHub Token
- Go to [GitHub Settings > Developer Settings > Personal Access Tokens > Tokens (classic)](https://github.com/settings/tokens).
- Generate a new token with `repo` permissions.
- **Copy it immediately!**

### 2. Jenkins Token
- Open `http://localhost:8080` in your browser.
- Follow the instructions to unlock Jenkins (the password is found in the Docker logs: `docker logs devops_jenkins`).
- Go to `User (top right) > Configure > API Token > Add New Token`.

### 3. Set Up Your `.env` File
Create a new file named `.env` in the `devops_dashboard` folder (or edit the example):
```env
GITHUB_TOKEN=your_token_here
REPO_OWNER=your_github_username
REPO_NAME=name_of_any_public_repo
JENKINS_TOKEN=your_jenkins_token
```

---

## 📊 Phase 4: Collect Data & Run

Now we tell our "Hands" (scripts) to go get the data and put it in the "Foundation" (database).

### 1. Initialize the Database
Run the app once just to create the tables:
```bash
python3 -m app.app
```
*(Stop it with `Ctrl+C` once it says it's running).*

### 2. Run the Collectors
Run these commands to pull live data:
```bash
python3 -m scripts.github_collector
python3 -m scripts.jenkins_collector
python3 -m scripts.docker_collector
```

---

## 🌐 Phase 5: View Your Dashboard

Now, start the web server for real:
```bash
python3 -m app.app
```
Open your browser to: **[http://localhost:5001](http://localhost:5001)**

---

## 💡 Troubleshooting for Beginners

- **"Docker not found"**: Make sure Docker Desktop is open.
- **"ModuleNotFoundError"**: Ensure you ran `source venv/bin/activate` before installing requirements.
- **"Port already in use"**: If 5001 is busy, change `port=5001` in `app/app.py` to `port=5002`.
- **Empty Dashboard?**: Make sure you ran the `scripts/` commands in Phase 4. They are the ones that actually "fill" the dashboard with data!
