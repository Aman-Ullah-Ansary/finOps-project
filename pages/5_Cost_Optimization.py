import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Cost Optimization",
    page_icon="💰",
    layout="wide"
)

# ------------------------------
# Title
# ------------------------------
st.title("💰 Cost Optimization Center")
st.caption("Estimate potential AWS cost savings through optimization")

# ------------------------------
# Load Data
# ------------------------------
df = load_data()

# ------------------------------
# Calculate Service Cost
# ------------------------------
service_cost = (
    df.groupby("service")["cost"]
    .sum()
    .reset_index()
)

# ------------------------------
# Optimization Rules
# ------------------------------
optimization_rules = {
    "EC2": 0.30,
    "RDS": 0.25,
    "S3": 0.20,
    "Lambda": 0.15,
    "CloudFront": 0.10
}

service_cost["Savings %"] = service_cost["service"].map(
    optimization_rules
).fillna(0.05)

service_cost["Potential Savings"] = (
    service_cost["cost"] *
    service_cost["Savings %"]
)

service_cost["Optimized Cost"] = (
    service_cost["cost"] -
    service_cost["Potential Savings"]
)

# ------------------------------
# KPI Cards
# ------------------------------
total_cost = service_cost["cost"].sum()
total_savings = service_cost["Potential Savings"].sum()
optimized_cost = service_cost["Optimized Cost"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Current Cost",
    f"${total_cost:,.2f}"
)

col2.metric(
    "💸 Potential Savings",
    f"${total_savings:,.2f}"
)

col3.metric(
    "✅ Optimized Cost",
    f"${optimized_cost:,.2f}"
)

st.divider()

# ------------------------------
# Cost Optimization Table
# ------------------------------
st.subheader("📋 Cost Optimization Report")

display_df = service_cost.copy()

display_df["Savings %"] = (
    display_df["Savings %"] * 100
).round(0).astype(int).astype(str) + "%"

display_df = display_df.rename(columns={
    "service": "AWS Service",
    "cost": "Current Cost"
})

st.dataframe(
    display_df,
    use_container_width=True
)

# ------------------------------
# Savings Chart
# ------------------------------
st.subheader("📊 Potential Savings by Service")

fig = px.bar(
    service_cost,
    x="service",
    y="Potential Savings",
    color="service",
    text_auto=".2f",
    title="Estimated Monthly Savings"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------------
# Cost Comparison Chart
# ------------------------------
st.subheader("📈 Current vs Optimized Cost")

comparison = service_cost.melt(
    id_vars="service",
    value_vars=["cost", "Optimized Cost"],
    var_name="Category",
    value_name="Amount"
)

fig2 = px.bar(
    comparison,
    x="service",
    y="Amount",
    color="Category",
    barmode="group",
    title="Current Cost vs Optimized Cost"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------------
# Executive Summary
# ------------------------------
highest_service = (
    service_cost.sort_values(
        "Potential Savings",
        ascending=False
    )
    .iloc[0]["service"]
)

st.subheader("📄 Executive Summary")

st.success(
f"""
### Optimization Summary

💰 Current AWS Spend: **${total_cost:,.2f}**

💸 Estimated Monthly Savings: **${total_savings:,.2f}**

✅ Optimized Monthly Spend: **${optimized_cost:,.2f}**

🏆 Highest Saving Opportunity: **{highest_service}**

### Recommended Actions

• Rightsize EC2 instances

• Purchase Reserved Instances for RDS

• Move unused S3 data to Glacier

• Optimize Lambda memory allocation

• Improve CloudFront cache efficiency
"""
)