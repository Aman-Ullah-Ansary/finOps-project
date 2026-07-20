import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Cost Anomaly Detection")

st.caption("Detect unusual AWS spending automatically")

# ------------------------
# Load Data
# ------------------------

df = pd.read_csv("data/aws_costs.csv")

df["date"] = pd.to_datetime(df["date"])

daily = (
    df.groupby("date")["cost"]
    .sum()
    .reset_index()
)

# ------------------------
# Z-Score
# ------------------------

mean = daily["cost"].mean()
std = daily["cost"].std()

daily["z_score"] = (daily["cost"] - mean) / std

daily["Anomaly"] = abs(daily["z_score"]) > 2

# ------------------------
# KPI Cards
# ------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average Cost",
    f"${mean:.2f}"
)

c2.metric(
    "Highest Cost",
    f"${daily['cost'].max():.2f}"
)

c3.metric(
    "Anomalies",
    int(daily["Anomaly"].sum())
)

st.divider()

# ------------------------
# Chart
# ------------------------

fig = px.scatter(
    daily,
    x="date",
    y="cost",
    color="Anomaly",
    size=abs(daily["z_score"]),
    title="Detected AWS Cost Anomalies"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Table
# ------------------------

st.subheader("Detected Anomalies")

anomalies = daily[daily["Anomaly"]]

if anomalies.empty:
    st.success("✅ No anomalies detected.")
else:
    st.dataframe(anomalies, use_container_width=True)

# ------------------------
# AI Summary
# ------------------------

if anomalies.empty:
    st.success(
        """
AI Analysis

No abnormal AWS spending detected.

Infrastructure appears healthy.
"""
    )
else:
    st.warning(
        f"""
AI Analysis

Detected **{len(anomalies)} unusual cost spikes**.

Recommendation:

• Check EC2 usage

• Review RDS activity

• Verify Lambda executions

• Inspect CloudFront traffic
"""
    )