import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    """
    Load and prepare AWS cost data.
    """

    df = pd.read_csv("data/aws_costs.csv")

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Sort by date
    df = df.sort_values("date")

    # Reset index
    df = df.reset_index(drop=True)

    return df