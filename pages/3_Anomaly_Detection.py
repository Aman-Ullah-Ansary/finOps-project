import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

# ------------------------------
# Title
# ------------------------------
st.title("🚨 Cost Anomaly Detection")
st.caption("Detect unusual AWS spending automatically")

# ------------------------------
# Load Data
# ------------------------------
df = load_data()

# ------------------------------
# Prepare Daily Cost Data
# ------------------------------
daily = (
    df.groupby("date")["cost"]
    .sum()
    .reset_index()
)

# ------------------------------
# Calculate Z-Score
# ------------------------------
mean = daily["cost"].mean()
std = daily["cost"].std()

if std == 0:
    daily["z_score"] = 0
else:
    daily["z_score"] = (daily["cost"] - mean) / std

daily["Anomaly"] = daily["z_score"].abs() > 2

# ------------------------------
# KPI Cards
# ------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Cost",
    f"${mean:.2f}"
)

col2.metric(
    "Highest Cost",
    f"${daily['cost'].max():.2f}"
)

col3.metric(
    "Anomalies Found",
    int(daily["Anomaly"].sum())
)

st.divider()

# ------------------------------
# Scatter Chart
# ------------------------------
st.subheader("📈 Cost Anomaly Visualization")

fig = px.scatter(
    daily,
    x="date",
    y="cost",
    color="Anomaly",
    size=daily["z_score"].abs() + 1,
    hover_data=["z_score"],
    title="Detected AWS Cost Anomalies"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Line Chart
# ------------------------------
st.subheader("📊 Daily Cost Trend")

fig2 = px.line(
    daily,
    x="date",
    y="cost",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Anomaly Table
# ------------------------------
st.subheader("📋 Detected Anomalies")

anomalies = daily[daily["Anomaly"]]

if anomalies.empty:
    st.success("✅ No anomalies detected.")
else:
    st.dataframe(
        anomalies,
        use_container_width=True
    )

# ------------------------------
# AI Analysis
# ------------------------------
st.subheader("🤖 AI Analysis")

if anomalies.empty:
    st.success(
        """
No abnormal AWS spending detected.

Infrastructure appears healthy.

No immediate action is required.
"""
    )
else:
    st.warning(
        f"""
Detected **{len(anomalies)} unusual spending events**.

Recommended actions:

• Review EC2 utilization

• Check RDS usage

• Investigate Lambda invocations

• Review CloudFront traffic

• Verify unexpected deployments
"""
    )