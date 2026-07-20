import pandas as pd

def load_data():
    df = pd.read_csv("data/aws_costs.csv")
    return df