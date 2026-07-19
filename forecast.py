"""
forecast.py
------------
Predicts AWS costs for the next 30 days, per service.

HOW IT WORKS (in plain English):
We teach a simple machine learning model (Linear Regression) two things
about the historical cost data:
  1. The overall TREND — is spend generally going up or down over time?
  2. The WEEKLY PATTERN — are certain days of the week more expensive?

The model then uses those two learned patterns to predict future costs.

We use scikit-learn here (not Prophet) because it installs instantly with
no extra system dependencies — perfect for a free, beginner-friendly setup.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_costs(df: pd.DataFrame, days_ahead: int = 30) -> pd.DataFrame:
    """
    df must have columns: date, service, cost
    Returns a dataframe with forecasted costs per service for the next `days_ahead` days.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    all_forecasts = []

    for service, group in df.groupby("service"):
        group = group.sort_values("date").reset_index(drop=True)

        # Feature 1: day index (captures the trend, e.g. day 0, 1, 2, 3...)
        group["day_index"] = np.arange(len(group))
        # Feature 2: day of week, one-hot encoded (captures weekly seasonality)
        group["day_of_week"] = group["date"].dt.dayofweek
        dow_dummies = pd.get_dummies(group["day_of_week"], prefix="dow")

        X = pd.concat([group[["day_index"]], dow_dummies], axis=1)
        y = group["cost"]

        model = LinearRegression()
        model.fit(X, y)

        # Build future dates to predict
        last_day_index = group["day_index"].max()
        last_date = group["date"].max()
        future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days_ahead + 1)]

        future_df = pd.DataFrame({
            "date": future_dates,
            "day_index": range(last_day_index + 1, last_day_index + 1 + days_ahead),
        })
        future_df["day_of_week"] = future_df["date"].dt.dayofweek
        future_dummies = pd.get_dummies(future_df["day_of_week"], prefix="dow")

        # Make sure future data has the same columns as training data (fill missing days with 0)
        future_dummies = future_dummies.reindex(columns=dow_dummies.columns, fill_value=0)
        X_future = pd.concat([future_df[["day_index"]], future_dummies], axis=1)

        predictions = model.predict(X_future)
        predictions = np.maximum(predictions, 0)  # cost can't be negative

        future_df["service"] = service
        future_df["predicted_cost"] = predictions.round(2)
        all_forecasts.append(future_df[["date", "service", "predicted_cost"]])

    return pd.concat(all_forecasts).sort_values(["date", "service"]).reset_index(drop=True)


if __name__ == "__main__":
    df = pd.read_csv("data/aws_costs.csv")
    forecast = forecast_costs(df, days_ahead=30)

    total_by_service = forecast.groupby("service")["predicted_cost"].sum().round(2)
    print("Predicted total cost for the NEXT 30 DAYS, per service:\n")
    print(total_by_service.to_string())
    print(f"\nGrand total predicted spend (next 30 days): ${total_by_service.sum():.2f}")
