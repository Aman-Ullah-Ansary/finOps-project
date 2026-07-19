"""
recommendations.py
--------------------
Generates plain-English, actionable cost-saving recommendations based on
patterns in the billing data. This is "rule-based AI" — a set of if/then
rules written by a human expert (you!) rather than a black-box model.
Real FinOps tools (AWS Trusted Advisor, CloudHealth, etc.) work this way
for a huge part of their recommendations, so this is genuinely realistic.

HOW IT WORKS:
Each function below checks the cost data for one specific wasteful pattern
and returns a recommendation if it finds one.
"""

import pandas as pd


def _pct_change_last_n_days(group: pd.DataFrame, n: int = 14) -> float:
    group = group.sort_values("date")
    if len(group) < n * 2:
        return 0.0
    recent = group["cost"].tail(n).mean()
    previous = group["cost"].tail(n * 2).head(n).mean()
    if previous == 0:
        return 0.0
    return ((recent - previous) / previous) * 100


def generate_recommendations(df: pd.DataFrame) -> list[dict]:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    recommendations = []

    for service, group in df.groupby("service"):
        group = group.sort_values("date")
        avg_cost = group["cost"].mean()
        trend_pct = _pct_change_last_n_days(group)

        # Rule 1: Steadily rising cost trend -> flag for review
        if trend_pct > 20:
            recommendations.append({
                "service": service,
                "severity": "High",
                "title": f"{service} spend rising fast",
                "detail": (
                    f"{service} costs are up {trend_pct:.0f}% over the last 2 weeks "
                    f"compared to the 2 weeks before that. Review recent usage — "
                    f"this could be a new workload, an unintended scale-up, or leftover test resources."
                ),
            })

        # Rule 2: High-cost compute services -> suggest Reserved Instances / Savings Plans
        if service in ("EC2", "RDS") and avg_cost > 25:
            recommendations.append({
                "service": service,
                "severity": "Medium",
                "title": f"Consider Reserved Instances / Savings Plan for {service}",
                "detail": (
                    f"{service} has averaged ${avg_cost:.2f}/day. If this workload runs "
                    f"steadily (not just spiky/temporary), switching to a 1-year Reserved "
                    f"Instance or Savings Plan typically cuts this cost by 30-60%."
                ),
            })

        # Rule 3: Very spiky/inconsistent Lambda cost -> possible retry loop or bad trigger config
        if service == "Lambda" and group["cost"].std() > group["cost"].mean() * 0.5:
            recommendations.append({
                "service": service,
                "severity": "Medium",
                "title": "Lambda costs are unusually inconsistent",
                "detail": (
                    "Lambda spend swings a lot day to day. This is often caused by a retry "
                    "loop, an oversized memory allocation, or an event source misconfiguration. "
                    "Check CloudWatch logs for repeated invocations or errors."
                ),
            })

        # Rule 4: Low, flat cost -> could be an idle/forgotten resource worth checking
        if avg_cost < 15 and trend_pct == 0 and service in ("EC2", "RDS"):
            recommendations.append({
                "service": service,
                "severity": "Low",
                "title": f"Verify {service} resources are still needed",
                "detail": (
                    f"{service} shows small, flat, unchanging cost over time — a common sign "
                    f"of an idle or forgotten resource (e.g., a test instance nobody shut down). "
                    f"Confirm it's still in active use, or terminate it."
                ),
            })

    return recommendations


if __name__ == "__main__":
    df = pd.read_csv("data/aws_costs.csv")
    recs = generate_recommendations(df)
    print(f"Generated {len(recs)} recommendations:\n")
    for r in recs:
        print(f"[{r['severity']}] {r['service']} — {r['title']}")
        print(f"   {r['detail']}\n")
