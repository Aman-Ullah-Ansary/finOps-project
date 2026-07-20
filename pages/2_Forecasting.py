import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.data_loader import load_data

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

# ------------------------------
# Title
# ------------------------------
st.title("📈 Cost Forecasting")
st.caption("Predict future AWS cloud spending")

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

daily["day"] = np.arange(len(daily))

# ------------------------------
# Train Linear Regression Model
# ------------------------------
X = daily[["day"]]
y = daily["cost"]

model = LinearRegression()
model.fit(X, y)

# ------------------------------
# Predict Next 30 Days
# ------------------------------
future_days = np.arange(len(daily) + 30).reshape(-1, 1)

prediction = model.predict(future_days)

forecast = pd.DataFrame({
    "Day": future_days.flatten(),
    "Forecast Cost": prediction
})

# ------------------------------
# KPI Cards
# ------------------------------
today_cost = daily["cost"].iloc[-1]
forecast_cost = prediction[-1]

growth = ((forecast_cost - today_cost) / today_cost) * 100

c1, c2, c3 = st.columns(3)

c1.metric(
    "Today's Cost",
    f"${today_cost:.2f}"
)

c2.metric(
    "30-Day Forecast",
    f"${forecast_cost:.2f}"
)

c3.metric(
    "Expected Growth",
    f"{growth:.2f}%"
)

st.divider()

# ------------------------------
# Forecast Chart
# ------------------------------
st.subheader("📊 Cost Forecast")

fig = px.line(
    forecast,
    x="Day",
    y="Forecast Cost",
    markers=True,
    title="Predicted AWS Cost (Next 30 Days)"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Forecast Summary
# ------------------------------
st.subheader("📄 Forecast Summary")

st.success(
    f"""
### AI Prediction

💰 **Current Daily Cost:** ${today_cost:.2f}

📈 **Predicted Cost After 30 Days:** ${forecast_cost:.2f}

📊 **Expected Growth:** {growth:.2f}%

🤖 Based on historical billing trends, AWS spending is projected to follow this trajectory over the next month.
"""
)

# ------------------------------
# Forecast Table
# ------------------------------
st.subheader("📋 Forecast Data")

st.dataframe(forecast, use_container_width=True)