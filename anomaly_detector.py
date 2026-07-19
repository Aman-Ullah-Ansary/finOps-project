"""
anomaly_detector.py
--------------------
Finds "unusual" cost days for each AWS service — days where the cost
was way higher than that service's normal recent pattern.

HOW IT WORKS (in plain English):
For each service, we look at a rolling 14-day window of past costs.
We calculate the average and how "spread out" (standard deviation) those
costs normally are. Then for each day, we ask:
    "How many standard deviations away from normal is today's cost?"
That number is called a Z-SCORE.

If a day's Z-score is above a threshold (default: 2.5), we flag it as
an anomaly — meaning "this is unusually expensive, go check what happened."

This is a real, industry-standard statistical technique — no paid AI API needed.
"""

import pandas as pd


def detect_anomalies(df: pd.DataFrame, window: int = 14, z_threshold: float = 2.5) -> pd.DataFrame:
    """
    df must have columns: date, service, cost
    Returns the same dataframe with two new columns: zscore, is_anomaly
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["service", "date"])

    results = []
    for service, group in df.groupby("service"):
        group = group.sort_values("date").reset_index(drop=True)

        rolling_mean = group["cost"].rolling(window=window, min_periods=5).mean()
        rolling_std = group["cost"].rolling(window=window, min_periods=5).std()

        # Avoid divide-by-zero for very stable services
        rolling_std = rolling_std.replace(0, 0.01).fillna(0.01)

        zscore = (group["cost"] - rolling_mean) / rolling_std
        group["zscore"] = zscore.round(2)
        group["is_anomaly"] = group["zscore"] > z_threshold

        results.append(group)

    return pd.concat(results).sort_values(["date", "service"]).reset_index(drop=True)


if __name__ == "__main__":
    # Quick standalone test: run this file directly to see anomalies printed
    df = pd.read_csv("data/aws_costs.csv")
    result = detect_anomalies(df)
    anomalies = result[result["is_anomaly"]]
    print(f"Found {len(anomalies)} anomalies out of {len(result)} total records:\n")
    print(anomalies[["date", "service", "cost", "zscore"]].to_string(index=False))
