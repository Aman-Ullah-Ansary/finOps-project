import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Cost Forecasting")

st.caption("Predict future AWS cloud spending")

# -----------------------
# Load Data
# -----------------------

df = pd.read_csv("data/aws_costs.csv")

df["date"] = pd.to_datetime(df["date"])

daily = (
    df.groupby("date")["cost"]
    .sum()
    .reset_index()
)

daily["day"] = np.arange(len(daily))

# -----------------------
# Train Model
# -----------------------

X = daily[["day"]]
y = daily["cost"]

model = LinearRegression()
model.fit(X, y)

future_days = np.arange(len(daily)+30).reshape(-1,1)

prediction = model.predict(future_days)

forecast = pd.DataFrame({
    "Day":future_days.flatten(),
    "Forecast Cost":prediction
})

# -----------------------
# KPIs
# -----------------------

c1,c2,c3 = st.columns(3)

c1.metric(
    "Today's Cost",
    f"${daily['cost'].iloc[-1]:.2f}"
)

c2.metric(
    "30-Day Forecast",
    f"${prediction[-1]:.2f}"
)

growth=((prediction[-1]-daily["cost"].iloc[-1])/daily["cost"].iloc[-1])*100

c3.metric(
    "Growth",
    f"{growth:.2f}%"
)

st.divider()

# -----------------------
# Forecast Chart
# -----------------------

fig = px.line(
    forecast,
    x="Day",
    y="Forecast Cost",
    title="30-Day Cost Forecast"
)

st.plotly_chart(fig,use_container_width=True)

st.success(
f"""
Predicted AWS monthly spend after 30 days:

**${prediction[-1]:.2f}**

Growth:

**{growth:.2f}%**
"""
)