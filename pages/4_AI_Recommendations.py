import streamlit as st
import pandas as pd
from utils.data_loader import load_data

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="AI Recommendations",
    page_icon="🤖",
    layout="wide"
)

# ------------------------------
# Title
# ------------------------------
st.title("🤖 AI Cost Optimization Recommendations")
st.caption("AI-generated suggestions to reduce AWS cloud costs")

# ------------------------------
# Load Data
# ------------------------------
df = load_data()

# ------------------------------
# Service Cost Summary
# ------------------------------
service_cost = (
    df.groupby("service")["cost"]
    .sum()
    .sort_values(ascending=False)
)

total_cost = service_cost.sum()

st.metric(
    "💰 Estimated Monthly Spend",
    f"${total_cost:,.2f}"
)

st.divider()

# ------------------------------
# AI Recommendation Engine
# ------------------------------
recommendations = []

for service, cost in service_cost.items():

    if service == "EC2":
        recommendations.append({
            "Priority": "🔴 High",
            "Service": "EC2",
            "Current Cost": round(cost, 2),
            "Potential Savings": round(cost * 0.30, 2),
            "Recommendation": "Rightsize or terminate idle EC2 instances."
        })

    elif service == "RDS":
        recommendations.append({
            "Priority": "🔴 High",
            "Service": "RDS",
            "Current Cost": round(cost, 2),
            "Potential Savings": round(cost * 0.25, 2),
            "Recommendation": "Purchase Reserved Instances for long-running databases."
        })

    elif service == "S3":
        recommendations.append({
            "Priority": "🟠 Medium",
            "Service": "S3",
            "Current Cost": round(cost, 2),
            "Potential Savings": round(cost * 0.20, 2),
            "Recommendation": "Move cold data to Glacier or Intelligent-Tiering."
        })

    elif service == "Lambda":
        recommendations.append({
            "Priority": "🟢 Low",
            "Service": "Lambda",
            "Current Cost": round(cost, 2),
            "Potential Savings": round(cost * 0.15, 2),
            "Recommendation": "Reduce execution time and memory allocation."
        })

    elif service == "CloudFront":
        recommendations.append({
            "Priority": "🟡 Medium",
            "Service": "CloudFront",
            "Current Cost": round(cost, 2),
            "Potential Savings": round(cost * 0.10, 2),
            "Recommendation": "Increase cache hit ratio and optimize CDN behavior."
        })

    else:
        recommendations.append({
            "Priority": "🟢 Low",
            "Service": service,
            "Current Cost": round(cost, 2),
            "Potential Savings": round(cost * 0.05, 2),
            "Recommendation": "Review usage and eliminate unnecessary resources."
        })

recommend_df = pd.DataFrame(recommendations)

# ------------------------------
# Recommendations Table
# ------------------------------
st.subheader("📋 AI Recommendations")

st.dataframe(
    recommend_df,
    use_container_width=True
)

# ------------------------------
# Savings Summary
# ------------------------------
total_savings = recommend_df["Potential Savings"].sum()

st.divider()

st.success(
f"""
## 💰 Estimated Monthly Savings

### Potential Savings

**${total_savings:,.2f}**

By applying these recommendations, your estimated monthly AWS bill can be significantly reduced.
"""
)

# ------------------------------
# Executive Summary
# ------------------------------
st.subheader("📄 Executive Summary")

highest_service = service_cost.idxmax()

st.info(
f"""
### AI Analysis

• Highest spending service: **{highest_service}**

• Estimated monthly spend: **${total_cost:,.2f}**

• Estimated monthly savings: **${total_savings:,.2f}**

### Recommended Priorities

✅ Rightsize EC2 instances

✅ Optimize RDS pricing

✅ Archive unused S3 objects

✅ Improve CloudFront caching

✅ Optimize Lambda execution
"""
)