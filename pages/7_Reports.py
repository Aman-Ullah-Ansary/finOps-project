import streamlit as st
import pandas as pd
from io import BytesIO
from utils.data_loader import load_data

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Reports")
st.caption("Generate and download AWS FinOps reports.")

# ----------------------------
# Load Data
# ----------------------------
df = load_data()

# ----------------------------
# Calculate Metrics
# ----------------------------
total_spend = df["cost"].sum()

average_daily = (
    df.groupby("date")["cost"]
    .sum()
    .mean()
)

service_cost = (
    df.groupby("service")["cost"]
    .sum()
)

highest_service = service_cost.idxmax()
highest_cost = service_cost.max()

lowest_service = service_cost.idxmin()
lowest_cost = service_cost.min()

# ----------------------------
# KPI Cards
# ----------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💰 Total AWS Spend",
        f"${total_spend:.2f}"
    )

with col2:
    st.metric(
        "📅 Average Daily Spend",
        f"${average_daily:.2f}"
    )

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "📈 Highest Cost Service",
        highest_service,
        f"${highest_cost:.2f}"
    )

with col4:
    st.metric(
        "📉 Lowest Cost Service",
        lowest_service,
        f"${lowest_cost:.2f}"
    )

# ----------------------------
# Executive Summary
# ----------------------------
st.divider()

st.subheader("📋 Executive Summary")

with st.container(border=True):

    st.markdown(f"""
### AWS Cost Overview

- **Total Cloud Spend:** **${total_spend:.2f}**
- **Average Daily Spend:** **${average_daily:.2f}**
- **Highest Cost Service:** **{highest_service} (${highest_cost:.2f})**
- **Lowest Cost Service:** **{lowest_service} (${lowest_cost:.2f})**

### Overall Cost Status

🟡 **Moderate Spending**

### Optimization Recommendations

- ✅ Review spending on **{highest_service}** to identify optimization opportunities.
- ✅ Purchase Reserved Instances or Savings Plans for long-running workloads.
- ✅ Remove idle EC2, EBS, and Load Balancer resources.
- ✅ Enable S3 Lifecycle Policies for infrequently accessed data.
- ✅ Configure AWS Budgets and Cost Anomaly Detection.
""")

# ----------------------------
# AWS Cost Data
# ----------------------------
st.divider()

st.subheader("📊 AWS Cost Dataset")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ----------------------------
# Download Report
# ----------------------------
st.divider()

st.subheader("📥 Download Reports")

csv = df.to_csv(index=False).encode("utf-8")

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="AWS Cost Report"
    )

col1, col2 = st.columns(2)

with col1:

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="aws_finops_report.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:

    st.download_button(
        label="📊 Download Excel",
        data=excel_buffer.getvalue(),
        file_name="aws_finops_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ----------------------------
# Footer
# ----------------------------
st.divider()

st.caption(
    "AI-Powered Cloud Cost Optimization & FinOps Platform for AWS | Reports Module"
)