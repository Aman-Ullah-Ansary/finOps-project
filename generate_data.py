"""
generate_data.py
-----------------
This creates FAKE (but realistic) AWS billing data so you can build and test
your FinOps dashboard without spending any real money on AWS.

It simulates 120 days of daily costs across 5 common AWS services:
EC2, S3, RDS, Lambda, and CloudFront.

It also intentionally injects a few "cost spikes" (anomalies) so your
anomaly detector has something real to catch and show off.

HOW TO RUN:
    python generate_data.py

OUTPUT:
    data/aws_costs.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Make results repeatable every time you run this script
np.random.seed(42)

NUM_DAYS = 120
SERVICES = {
    "EC2": {"base_cost": 45, "noise": 5, "weekly_pattern": True},
    "S3": {"base_cost": 12, "noise": 2, "weekly_pattern": False},
    "RDS": {"base_cost": 30, "noise": 4, "weekly_pattern": True},
    "Lambda": {"base_cost": 6, "noise": 1.5, "weekly_pattern": False},
    "CloudFront": {"base_cost": 9, "noise": 2, "weekly_pattern": True},
}

start_date = datetime.today() - timedelta(days=NUM_DAYS)
dates = [start_date + timedelta(days=i) for i in range(NUM_DAYS)]

rows = []
for service, cfg in SERVICES.items():
    for i, date in enumerate(dates):
        # Slow upward growth trend over time (like a real growing company)
        trend = i * 0.05

        # Weekday costs run a bit higher than weekend for compute-heavy services
        weekday_factor = 1.0
        if cfg["weekly_pattern"] and date.weekday() < 5:  # Mon-Fri
            weekday_factor = 1.15

        cost = cfg["base_cost"] * weekday_factor + trend
        cost += np.random.normal(0, cfg["noise"])  # natural daily noise
        cost = max(cost, 0.5)  # cost can't be negative

        rows.append({"date": date.strftime("%Y-%m-%d"), "service": service, "cost": round(cost, 2)})

df = pd.DataFrame(rows)

# ---- Inject a few realistic anomalies (cost spikes) ----
# Example: someone left an oversized EC2 instance running over a weekend
anomaly_injections = [
    {"service": "EC2", "days_ago": 15, "multiplier": 3.2},
    {"service": "RDS", "days_ago": 40, "multiplier": 2.5},
    {"service": "Lambda", "days_ago": 8, "multiplier": 6.0},   # e.g. infinite retry loop bug
    {"service": "CloudFront", "days_ago": 55, "multiplier": 2.8},
]

for anomaly in anomaly_injections:
    target_date = (datetime.today() - timedelta(days=anomaly["days_ago"])).strftime("%Y-%m-%d")
    mask = (df["date"] == target_date) & (df["service"] == anomaly["service"])
    df.loc[mask, "cost"] = df.loc[mask, "cost"] * anomaly["multiplier"]
    df["cost"] = df["cost"].round(2)

df = df.sort_values(["date", "service"]).reset_index(drop=True)

df.to_csv("data/aws_costs.csv", index=False)
print(f"Done! Created data/aws_costs.csv with {len(df)} rows across {len(SERVICES)} services.")
print(f"Injected {len(anomaly_injections)} cost anomalies for your detector to find.")
