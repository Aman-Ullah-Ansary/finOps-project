import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.title("☁️ AI Cloud FinOps")

st.sidebar.markdown("---")

st.sidebar.info(
    """
**Platform Version:** 1.0

**Environment:** Development

**Data Source:** Sample AWS Billing Data
"""
)

# ------------------------------
# Load Data
# ------------------------------
df = load_data()

# ------------------------------
# Sidebar Filters
# ------------------------------
selected_services = st.sidebar.multiselect(
    "Select AWS Services",
    options=df["service"].unique(),
    default=df["service"].unique()
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["date"].max()
)

# ------------------------------
# Apply Filters
# ------------------------------
df = df[
    (df["service"].isin(selected_services))
    & (df["date"] >= pd.to_datetime(start_date))
    & (df["date"] <= pd.to_datetime(end_date))
]

# ------------------------------
# Dashboard Title
# ------------------------------
st.title("☁️ AI Cloud FinOps Platform")
st.caption("AI-Powered Cloud Cost Optimization Dashboard")

# ------------------------------
# Handle Empty Data
# ------------------------------
if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ------------------------------
# KPI Calculations
# ------------------------------
total_cost = df["cost"].sum()
avg_cost = df["cost"].mean()
max_cost = df["cost"].max()
service_count = df["service"].nunique()

highest_service = (
    df.groupby("service")["cost"]
    .sum()
    .idxmax()
)

# ------------------------------
# KPI Cards
# ------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Total Cost", f"${total_cost:,.2f}")
c2.metric("📈 Average Cost", f"${avg_cost:,.2f}")
c3.metric("🔥 Highest Cost", f"${max_cost:,.2f}")
c4.metric("☁️ AWS Services", service_count)
c5.metric("🏆 Top Service", highest_service)

st.divider()

# ------------------------------
# Daily Cost Trend
# ------------------------------
st.subheader("📈 Daily AWS Cost Trend")

daily_cost = (
    df.groupby("date")["cost"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily_cost,
    x="date",
    y="cost",
    markers=True,
    title="Daily AWS Cost"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Cost by Service
# ------------------------------
st.subheader("🥧 Cost by AWS Service")

service_cost = (
    df.groupby("service")["cost"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    service_cost,
    names="service",
    values="cost",
    hole=0.45
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Service Cost Comparison
# ------------------------------
st.subheader("📊 Service Cost Comparison")

fig3 = px.bar(
    service_cost,
    x="service",
    y="cost",
    color="service",
    text_auto=".2s",
    title="AWS Service Cost Comparison"
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------------
# Top Expensive Services
# ------------------------------
st.subheader("💸 Top AWS Services by Cost")

top_services = (
    df.groupby("service")["cost"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(top_services, use_container_width=True)

# ------------------------------
# Executive Summary
# ------------------------------
st.subheader("📄 Executive Summary")

st.success(
    f"""
✅ **Total AWS Spend:** ${total_cost:,.2f}

✅ **Average Daily Spend:** ${avg_cost:,.2f}

✅ **AWS Services Analysed:** {service_count}

✅ **Highest Cost Service:** {highest_service}

✅ **Dashboard Status:** Healthy
"""
)

# ------------------------------
# Billing Data
# ------------------------------
st.subheader("📋 Billing Data")

st.dataframe(df, use_container_width=True)