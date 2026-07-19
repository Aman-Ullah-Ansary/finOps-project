"""
app.py
-------
This is your dashboard. It brings together everything from the other
files (data, anomaly detection, forecasting, recommendations) into one
visual web page.

HOW TO RUN THIS (do this in your terminal):
    streamlit run app.py

It will open automatically in your web browser at http://localhost:8501
"""

import pandas as pd
import streamlit as st
import plotly.express as px

from anomaly_detector import detect_anomalies
from forecast import forecast_costs
from recommendations import generate_recommendations

st.set_page_config(page_title="SentinelCost — AI FinOps Dashboard", layout="wide")

st.title("☁️ SentinelCost — AI-Powered AWS Cost Optimization Dashboard")
st.caption("Anomaly detection, 30-day forecasting, and cost-saving recommendations — built on real FinOps techniques.")

# ---------- Load data ----------
@st.cache_data
def load_data():
    return pd.read_csv("data/aws_costs.csv")

df = load_data()
df["date"] = pd.to_datetime(df["date"])

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
services = sorted(df["service"].unique())
selected_services = st.sidebar.multiselect("AWS Services", services, default=services)
filtered_df = df[df["service"].isin(selected_services)]

# ---------- Top KPIs ----------
total_spend = filtered_df["cost"].sum()
avg_daily_spend = filtered_df.groupby("date")["cost"].sum().mean()
num_days = filtered_df["date"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Spend (period shown)", f"${total_spend:,.2f}")
col2.metric("Avg Daily Spend", f"${avg_daily_spend:,.2f}")
col3.metric("Days of Data", f"{num_days}")

st.divider()

# ---------- Cost over time chart ----------
st.subheader("📈 Daily Cost by Service")
daily_by_service = filtered_df.groupby(["date", "service"], as_index=False)["cost"].sum()
fig = px.line(daily_by_service, x="date", y="cost", color="service", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------- Anomaly detection ----------
st.subheader("🚨 Detected Cost Anomalies")
anomaly_df = detect_anomalies(filtered_df)
anomalies_only = anomaly_df[anomaly_df["is_anomaly"]].sort_values("date", ascending=False)

if len(anomalies_only) == 0:
    st.success("No anomalies detected in the selected data. Spend looks normal.")
else:
    st.warning(f"Found {len(anomalies_only)} unusual cost spike(s). Review these:")
    st.dataframe(
        anomalies_only[["date", "service", "cost", "zscore"]].rename(
            columns={"zscore": "severity_score (higher = more unusual)"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    fig2 = px.scatter(
        anomaly_df, x="date", y="cost", color="service",
        symbol="is_anomaly", size=anomaly_df["is_anomaly"].map({True: 14, False: 6}),
        title="Cost timeline with anomalies highlighted (larger dot = anomaly)"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------- Forecast ----------
st.subheader("🔮 30-Day Cost Forecast")
forecast_df = forecast_costs(filtered_df, days_ahead=30)

fig3 = px.line(forecast_df, x="date", y="predicted_cost", color="service", markers=False,
               title="Predicted spend for the next 30 days")
st.plotly_chart(fig3, use_container_width=True)

forecast_total = forecast_df.groupby("service")["predicted_cost"].sum().round(2).sort_values(ascending=False)
st.write("**Predicted total spend, next 30 days, by service:**")
st.dataframe(forecast_total.reset_index().rename(columns={"predicted_cost": "predicted_total_cost"}),
             use_container_width=True, hide_index=True)
st.info(f"**Grand total predicted spend (next 30 days): ${forecast_total.sum():,.2f}**")

st.divider()

# ---------- Recommendations ----------
st.subheader("💡 Cost-Saving Recommendations")
recs = generate_recommendations(filtered_df)

if len(recs) == 0:
    st.success("No specific recommendations right now — costs look well-optimized.")
else:
    severity_color = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
    for r in recs:
        with st.expander(f"{severity_color.get(r['severity'], '⚪')} [{r['severity']}] {r['service']} — {r['title']}"):
            st.write(r["detail"])

st.divider()
st.caption("Built with Python, scikit-learn, and Streamlit — 100% free, open-source stack. No paid AI APIs used.")
