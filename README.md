# 🛡️ FinOps Project — AI-Assisted AWS Cost Optimization & FinOps Platform

A free, open-source FinOps tool that analyzes AWS billing data to detect cost anomalies, forecast future spend, and generate actionable cost-saving recommendations — built entirely with free/open-source tools. The platform combines cost analytics, machine learning, observability, and DevOps automation into a single dashboard.

## 📈 Project Highlights

- Automated the full build-to-deploy cycle using GitHub Actions CI/CD
- Containerized the complete application stack with Docker Compose
- Implemented infrastructure observability using Prometheus and Grafana
- Built AI-assisted cloud cost analysis and 30-day spend forecasting
- Deployed in a production-style environment on AWS EC2 behind Nginx

## Architecture

<details>
<summary>View Architecture</summary>

```text
                 Internet
                     │
                     ▼
                AWS EC2 Instance
                     │
                     ▼
                  Nginx
                     │
                     ▼
            Docker Compose Stack
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 SentinelCost   Prometheus      Grafana
      │                              ▲
      │                              │
      └──────────────┐        ┌──────┘
                     ▼        ▼
          Node Exporter   cAdvisor
```

</details>


## 🔁 Workflow
```text

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
```

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

```text
finOps-project/
├── app.py                  # Streamlit dashboard (main entry point)
├── pages/                  # Multi-page Streamlit views
├── auth/                   # Authentication logic
├── monitoring/             # Prometheus & Grafana configuration
├── assets/                 # Images and static assets
├── docs/                   # Architecture diagrams and demo GIF
├── screenshots/            # README screenshots
├── utils/                  # Forecasting, anomaly detection, recommendations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```


## How to run locally

```bash
git clone https://github.com/Aman-Ullah-Ansary/finOps-project.git
cd finOps-project
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


## 📸 Screenshots

<details>
<summary><b>📷 Click to view all screenshots (19)</b></summary>

<br>

<img width="1917" height="827" alt="Screenshot 2026-07-21 122931" src="https://github.com/user-attachments/assets/f3be14f0-3c86-464d-9ab4-0fea3b621572" />

<img width="1908" height="748" alt="Screenshot 2026-07-21 144441" src="https://github.com/user-attachments/assets/16aa8d0d-8a8c-41bd-bbb8-2ce3e07ecf35" />

<img width="1910" height="911" alt="Screenshot 2026-07-21 160455" src="https://github.com/user-attachments/assets/7dbcd918-8c7b-412f-a424-87eb04222e90" />

<img width="1917" height="961" alt="Screenshot 2026-07-21 161213" src="https://github.com/user-attachments/assets/f91ff89d-dfcf-41aa-ba93-9c87b2c20520" />

<img width="1602" height="857" alt="Screenshot 2026-07-21 205918" src="https://github.com/user-attachments/assets/529eb8d2-fd27-4fe7-9e2a-397ac94b3103" />

<img width="1878" height="916" alt="Screenshot 2026-07-21 210153" src="https://github.com/user-attachments/assets/bcbbd783-5d8a-4f15-a087-fc12c2896dfc" />

<img width="1482" height="757" alt="Screenshot 2026-07-21 210339" src="https://github.com/user-attachments/assets/565c76d3-3375-4e53-a2c0-b57697a23941" />

<img width="1917" height="1021" alt="Screenshot 2026-07-21 210521" src="https://github.com/user-attachments/assets/5e328b6e-02c7-4264-8c5c-0669a7e03131" />

<img width="1572" height="802" alt="Screenshot 2026-07-21 210557" src="https://github.com/user-attachments/assets/18f65bbe-30d3-47f0-8f00-c016d19e9baa" />

<img width="1910" height="793" alt="Screenshot 2026-07-21 210641" src="https://github.com/user-attachments/assets/5d2da984-953e-43a8-b490-3982fa5635d2" />

<img width="1917" height="863" alt="Screenshot 2026-07-21 210656" src="https://github.com/user-attachments/assets/416dd8bd-a54d-4310-aa4c-78e37476f211" />

<img width="1917" height="863" alt="Screenshot 2026-07-21 210709" src="https://github.com/user-attachments/assets/c8a63719-6341-4663-8d4a-2844096e1874" />

<img width="1915" height="837" alt="Screenshot 2026-07-21 210726" src="https://github.com/user-attachments/assets/a19883eb-1a52-404b-9745-e4f196b7dbd2" />

<img width="1915" height="848" alt="Screenshot 2026-07-21 210746" src="https://github.com/user-attachments/assets/999824aa-7287-4a33-99c2-e6e76a10e3e3" />

<img width="1917" height="863" alt="Screenshot 2026-07-21 210813" src="https://github.com/user-attachments/assets/9990d777-82bb-4195-9751-039a682b8959" />

<img width="1917" height="637" alt="Screenshot 2026-07-21 210849" src="https://github.com/user-attachments/assets/56a34019-e302-4c0a-9bd5-16df64f81b9b" />

<img width="1917" height="583" alt="Screenshot 2026-07-21 210934" src="https://github.com/user-attachments/assets/82b8d30d-970b-4e3f-9090-ff7585a32525" />

<img width="1916" height="856" alt="Screenshot 2026-07-21 211024" src="https://github.com/user-attachments/assets/b530fcbd-e92a-424b-b1db-4c50672213cd" />

<img width="1917" height="802" alt="Screenshot 2026-07-21 211037" src="https://github.com/user-attachments/assets/370d07c1-0b7c-43ab-8509-2c3bff7406f5" />

</details>


## Using real AWS data instead of synthetic data
This project ships with synthetic sample data so it works instantly with zero
AWS cost. To use real billing data instead, pull it via `boto3` using the
AWS Cost Explorer API (`get_cost_and_usage`), and format it into the same
`date, service, cost` CSV structure used here.

## 🚀 Live Demo

[ Deployment available upon request. 
Production deployment is hosted on AWS EC2.
To minimize cloud infrastructure costs, the public instance is not kept online continuously.]
