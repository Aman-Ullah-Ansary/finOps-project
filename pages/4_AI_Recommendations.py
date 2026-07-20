import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Recommendations",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Cost Optimization Recommendations")

st.caption("Smart recommendations to reduce AWS spending")

# ------------------------
# Load Data
# ------------------------

df = pd.read_csv("data/aws_costs.csv")

service_cost = (
    df.groupby("service")["cost"]
    .sum()
    .sort_values(ascending=False)
)

total = service_cost.sum()

st.metric(
    "Estimated Monthly Spend",
    f"${total:.2f}"
)

st.divider()

# ------------------------
# Recommendation Engine
# ------------------------

recommendations = []

for service, cost in service_cost.items():

    if service == "EC2":
        recommendations.append({
            "Priority":"🔴 High",
            "Service":"EC2",
            "Savings":cost*0.30,
            "Recommendation":"Rightsize or stop idle EC2 instances."
        })

    elif service == "S3":
        recommendations.append({
            "Priority":"🟠 Medium",
            "Service":"S3",
            "Savings":cost*0.20,
            "Recommendation":"Move infrequently accessed objects to Glacier."
        })

    elif service == "RDS":
        recommendations.append({
            "Priority":"🔴 High",
            "Service":"RDS",
            "Savings":cost*0.25,
            "Recommendation":"Use Reserved Instances for production databases."
        })

    elif service == "Lambda":
        recommendations.append({
            "Priority":"🟢 Low",
            "Service":"Lambda",
            "Savings":cost*0.15,
            "Recommendation":"Optimize function execution duration."
        })

    elif service == "CloudFront":
        recommendations.append({
            "Priority":"🟡 Medium",
            "Service":"CloudFront",
            "Savings":cost*0.10,
            "Recommendation":"Improve cache hit ratio."
        })

recommend_df = pd.DataFrame(recommendations)

st.subheader("Recommendations")

st.dataframe(
    recommend_df,
    use_container_width=True
)

st.divider()

total_savings = recommend_df["Savings"].sum()

st.success(
f"""
## 💰 Estimated Savings

You could save approximately

# ${total_savings:.2f}

per month by implementing the recommendations above.
"""
)

st.subheader("Executive Summary")

st.info(
"""
Top priorities:

• Rightsize EC2 instances

• Optimize RDS pricing

• Move cold S3 data to Glacier

• Improve CloudFront caching

• Optimize Lambda execution time
"""
)