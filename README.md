# SentinelCost — AI-Powered AWS Cost Optimization & FinOps Dashboard

A free, open-source FinOps tool that analyzes AWS billing data to detect cost
anomalies, forecast future spend, and generate actionable cost-saving
recommendations — built entirely with free/open-source tools.

## Features
- 📊 **Cost visualization** — daily spend broken down by AWS service (EC2, S3, RDS, Lambda, CloudFront)
- 🚨 **Anomaly detection** — statistical (z-score) detection of unusual cost spikes
- 🔮 **30-day forecasting** — machine learning (scikit-learn) prediction of future spend, factoring in trend and weekly seasonality
- 💡 **Automated recommendations** — rule-based cost-saving suggestions (Reserved Instances, idle resource checks, retry-loop detection)

## Tech Stack
Python · pandas · scikit-learn · Streamlit · Plotly · boto3 (for real AWS integration)

100% free and open-source — no paid AI APIs, no paid infrastructure required.

## How to run locally

```bash
git clone https://github.com/YOUR-USERNAME/ai-finops-aws-optimizer.git
cd ai-finops-aws-optimizer
pip install -r requirements.txt
python generate_data.py     # creates sample billing data
streamlit run app.py        # launches the dashboard
```

Then open the link shown in your terminal (usually `http://localhost:8501`).

## Project structure
```
├── data/
│   └── aws_costs.csv        # sample billing data (generated)
├── generate_data.py          # creates realistic synthetic AWS cost data
├── anomaly_detector.py       # z-score based anomaly detection
├── forecast.py                # linear regression cost forecasting
├── recommendations.py         # rule-based cost-saving engine
├── app.py                     # Streamlit dashboard (main entry point)
└── requirements.txt
```

## Using real AWS data instead of synthetic data
This project ships with synthetic sample data so it works instantly with zero
AWS cost. To use real billing data instead, pull it via `boto3` using the
AWS Cost Explorer API (`get_cost_and_usage`), and format it into the same
`date, service, cost` CSV structure used here.

## Live demo
[Add your Streamlit Cloud link here after deploying]
