# 🛡️ FinOps Project — AI-Assisted AWS Cost Optimization & FinOps Platform

A free, open-source FinOps tool that analyzes AWS billing data to detect cost anomalies, forecast future spend, and generate actionable cost-saving recommendations — built entirely with free/open-source tools. The platform combines cost analytics, machine learning, observability, and DevOps automation into a single dashboard.

## 📈 Project Highlights

- Automated the full build-to-deploy cycle using GitHub Actions CI/CD
- Containerized the complete application stack with Docker Compose
- Implemented infrastructure observability using Prometheus and Grafana
- Built AI-assisted cloud cost analysis and 30-day spend forecasting
- Deployed in a production-style environment on AWS EC2 behind Nginx

## 🏗 Architecture

<details> <summary>View text-based architecture (fallback)</summary>
Internet → AWS EC2 → Nginx → Docker → SentinelCost App
                                          │
                        ┌─────────────────┼─────────────────┐
                        ▼                 ▼                 ▼
                  Prometheus         Grafana        Node Exporter / cAdvisor

## 🔁 Workflow
AWS Cost Data
     ↓
AI Analysis
     ↓
Forecasting
     ↓
Anomaly Detection
     ↓
Recommendations
     ↓
Grafana
     ↓
User


## Features
- 📊 **Cost visualization** — daily spend broken down by AWS service (EC2, S3, RDS, Lambda, CloudFront)
- 🚨 **Anomaly detection** — statistical (z-score) detection of unusual cost spikes
- 🔮 **30-day forecasting** — machine learning (scikit-learn) prediction of future spend, factoring in trend and weekly seasonality
- 💡 **Automated recommendations** — rule-based cost-saving suggestions (Reserved Instances, idle resource checks, retry-loop detection)

## Tech Stack
Application: Python · Streamlit · Pandas · Scikit-Learn · Plotly · Groq AI

Infrastructure: AWS EC2 · Docker · Docker Compose · Nginx

Monitoring & Observability: Prometheus · Grafana · Node Exporter · cAdvisor

DevOps / CI-CD: GitHub Actions

100% free and open-source — no paid AI APIs, no paid infrastructure required.

## 📂 Project Structure
Finops-project/
├── app.py                  # Streamlit dashboard (main entry point)
├── pages/                  # Multi-page Streamlit views
├── auth/                   # Authentication logic
├── monitoring/             # Prometheus/Grafana configs
├── assets/                 # Images, static assets
├── docs/                   # Architecture diagram, demo GIF
├── screenshots/            # README screenshots
├── utils/                  # Forecasting, anomaly detection, recommendations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


## How to run locally

```bash
git clone https://github.com/YOUR-USERNAME/ai-finops-aws-optimizer.git
cd ai-finops-aws-optimizer
pip install -r requirements.txt
python generate_data.py     # creates sample billing data
streamlit run app.py        # launches the dashboard
```

[ Then open the link shown in your terminal  ]

## ⚙️ Installation
### Prerequisites
Python 3.10+
Docker
Docker Compose
Git
AWS Account (optional — for live billing data)

### Steps: 
bash
# 1. Clone the repository
git clone https://github.com/Aman-Ullah-Ansary/finOps-project.git
cd finOps-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Generate sample billing data
python generate_data.py

# 4. Run the application
streamlit run app.py

[ The app will be available at http://localhost:**** ]

## 🐳 Docker Deployment

Option 1 — Docker Compose (recommended)

bash
docker compose up -d

Option 2 — Manual Docker build/run

bash
docker build -t sentinelcost .
docker run -p 8501:8501 sentinelcost
## 🔄 CI/CD Pipeline
Developer → GitHub → GitHub Actions → EC2 → Docker → Nginx → Live Application

On every push to main, GitHub Actions automatically:

Runs tests & linting
Builds the Docker image
Deploys to the AWS EC2 instance
Restarts the container behind Nginx with zero manual intervention
## 📊 Monitoring

The platform ships with a full observability stack, visualized through dedicated Grafana dashboards:

Infrastructure Dashboard — host-level CPU, memory, disk (via Node Exporter)
Docker Dashboard — per-container resource usage (via cAdvisor)
Cost Dashboard — cloud spend trends and forecasts
Application Metrics Dashboard — request latency, anomalies detected, forecast accuracy

## 🤖 AI Features
Cost Forecasting — regression-based model projects spend 30 days ahead, accounting for trend and weekly seasonality
Anomaly Detection — z-score-based statistical detection of unusual cost spikes per service
AI Recommendations — Groq-powered LLM engine analyzes usage patterns and proposes concrete optimization actions (Reserved Instances, idle resource cleanup, retry-loop fixes)

## 🗺️ Roadmap
 - Live AWS Cost Explorer API integration (real billing data)
 - Terraform-based infrastructure provisioning
 - Kubernetes deployment manifests
 - Multi-cloud support (Azure, GCP)
 - Slack & Email alerting for anomalies
 - Conversational AI ChatOps interface




## Using real AWS data instead of synthetic data
This project ships with synthetic sample data so it works instantly with zero
AWS cost. To use real billing data instead, pull it via `boto3` using the
AWS Cost Explorer API (`get_cost_and_usage`), and format it into the same
`date, service, cost` CSV structure used here.

## 🚀 Live Demo

[ Deployment available upon request. 
Production deployment is hosted on AWS EC2.
To minimize cloud infrastructure costs, the public instance is not kept online continuously.]
