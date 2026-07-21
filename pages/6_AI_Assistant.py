import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
from utils.data_loader import load_data

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI FinOps Assistant",
    page_icon="💬",
    layout="wide"
)

st.title("💬 AI FinOps Assistant")
st.caption("Ask questions about your AWS cloud spending.")

# ----------------------------
# Load Data
# ----------------------------
df = load_data()

# ----------------------------
# User Input
# ----------------------------
question = st.text_input(
    "Ask a question",
    placeholder="Example: Which AWS service costs the most?"
)

if st.button("Analyze"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    q = question.lower()

    st.subheader("🤖 Answer")

    # ----------------------------
    # Highest Cost Service
    # ----------------------------
    if "highest" in q or "most" in q:

        service = (
            df.groupby("service")["cost"]
            .sum()
            .idxmax()
        )

        cost = (
            df.groupby("service")["cost"]
            .sum()
            .max()
        )

        st.success(
            f"The highest AWS spending is on **{service}** with a total cost of **${cost:.2f}**."
        )

    # ----------------------------
    # Lowest Cost Service
    # ----------------------------
    elif "lowest" in q or "least" in q:

        service = (
            df.groupby("service")["cost"]
            .sum()
            .idxmin()
        )

        cost = (
            df.groupby("service")["cost"]
            .sum()
            .min()
        )

        st.success(
            f"The lowest AWS spending is **{service}** with a total cost of **${cost:.2f}**."
        )

    # ----------------------------
    # Total Spend
    # ----------------------------
    elif "total" in q:

        total = df["cost"].sum()

        st.success(
            f"Total AWS spend is **${total:.2f}**."
        )

    # ----------------------------
    # Average Daily Spend
    # ----------------------------
    elif "average" in q:

        avg = (
            df.groupby("date")["cost"]
            .sum()
            .mean()
        )

        st.success(
            f"Average daily AWS spend is **${avg:.2f}**."
        )

    # ----------------------------
    # Optimization
    # ----------------------------
    elif "save" in q or "optimize" in q:

        st.info("""
### Recommended Optimizations

• Resize underutilized EC2 instances

• Delete unattached EBS volumes

• Enable S3 Lifecycle Policies

• Purchase Savings Plans

• Remove idle Load Balancers

Estimated Savings: **15–30%**
""")

    # ----------------------------
    # Groq AI
    # ----------------------------
    else:

        with st.spinner("🤖 AI is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an AI FinOps Assistant specializing in AWS, Kubernetes, Docker, Terraform, DevOps, Cloud Computing, and FinOps."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    temperature=0.7,
                    max_tokens=512
                )

                st.success(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Groq Error: {e}")