import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cost Optimization",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Cost Optimization Center")

df = pd.read_csv("data/aws_costs.csv")

service_cost = (
    df.groupby("service")["cost"]
    .sum()
    .reset_index()
)

optimizations = {
    "EC2": 0.30,
    "RDS": 0.25,
    "S3": 0.20,
    "Lambda": 0.15,
    "CloudFront": 0.10
}

service_cost["Potential Savings"] = service_cost.apply(
    lambda row: row["cost"] * optimizations.get(row["service"], 0.05),
    axis=1
)

service_cost["Optimized Cost"] = (
    service_cost["cost"] - service_cost["Potential Savings"]
)

st.subheader("Estimated Monthly Savings")

st.dataframe(service_cost, use_container_width=True)

fig = px.bar(
    service_cost,
    x="service",
    y="Potential Savings",
    color="service",
    title="Potential Savings by Service",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

total = service_cost["Potential Savings"].sum()

st.success(
f"""
Estimated Savings

💰 ${total:.2f}

per month
"""
)