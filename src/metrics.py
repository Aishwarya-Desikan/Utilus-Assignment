"""Business metric calculations for subscription analytics."""

from typing import Any

import pandas as pd


def calculate_mrr(subscriptions: pd.DataFrame) -> dict[str, float]:
    """Calculate monthly recurring revenue for each calendar month.

    A subscription is active in a month when its start_date is on or before the
    month end and its end_date is either missing or on or after the month start.

    Args:
        subscriptions: DataFrame with start_date, end_date, and monthly_price
            columns.

    Returns:
        A dictionary mapping month strings in YYYY-MM format to MRR values.
    """
    if subscriptions.empty:
        return {}

    start_dates = pd.to_datetime(subscriptions["start_date"])
    end_dates = pd.to_datetime(subscriptions["end_date"])
    first_month = start_dates.min().to_period("M").to_timestamp()

    latest_end_date = end_dates.dropna().max()
    if pd.isna(latest_end_date):
        last_month = start_dates.max().to_period("M").to_timestamp()
    else:
        last_month = max(start_dates.max(), latest_end_date).to_period("M").to_timestamp()

    monthly_mrr: dict[str, float] = {}
    for month_start in pd.date_range(first_month, last_month, freq="MS"):
        month_end = month_start + pd.offsets.MonthEnd(0)
        active_mask = (start_dates <= month_end) & (
            end_dates.isna() | (end_dates >= month_start)
        )
        monthly_mrr[month_start.strftime("%Y-%m")] = float(
            subscriptions.loc[active_mask, "monthly_price"].sum()
        )

    return monthly_mrr


def calculate_churn(subscriptions: pd.DataFrame) -> dict[str, int]:
    """Calculate churned customer counts by subscription end month.

    A customer is counted as churned when a subscription has an end_date and the
    customer has no new subscription starting within 30 days after that end_date.

    Args:
        subscriptions: DataFrame with customer_id, start_date, and end_date
            columns.

    Returns:
        A dictionary mapping month strings in YYYY-MM format to churned counts.
    """
    ended_subscriptions = subscriptions[subscriptions["end_date"].notna()].copy()
    if ended_subscriptions.empty:
        return {}

    started = subscriptions[["customer_id", "start_date"]].copy()
    started["start_date"] = pd.to_datetime(started["start_date"])
    ended_subscriptions["end_date"] = pd.to_datetime(ended_subscriptions["end_date"])

    churned_months: list[str] = []
    for subscription in ended_subscriptions.to_dict("records"):
        customer_id = subscription["customer_id"]
        end_date = subscription["end_date"]
        renewal_window_end = end_date + pd.Timedelta(days=30)
        new_subscription_mask = (
            (started["customer_id"] == customer_id)
            & (started["start_date"] > end_date)
            & (started["start_date"] <= renewal_window_end)
        )

        if not new_subscription_mask.any():
            churned_months.append(end_date.strftime("%Y-%m"))

    if not churned_months:
        return {}

    churn_counts = pd.Series(churned_months).value_counts().sort_index()
    return {month: int(count) for month, count in churn_counts.items()}


def calculate_cohort_retention(
    customers: pd.DataFrame,
    subscriptions: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Calculate signup cohorts with three-month retention.

    Customers are grouped by signup month. A customer is retained when they have
    at least one active subscription exactly three months after their signup_date.

    Args:
        customers: DataFrame with customer_id and signup_date columns.
        subscriptions: DataFrame with customer_id, start_date, and end_date
            columns.

    Returns:
        A list of cohort dictionaries containing cohort_month, cohort_size,
        active_after_3_months, and retention_rate_3m.
    """
    if customers.empty:
        return []

    customers = customers.copy()
    subscriptions = subscriptions.copy()
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])
    subscriptions["start_date"] = pd.to_datetime(subscriptions["start_date"])
    subscriptions["end_date"] = pd.to_datetime(subscriptions["end_date"])
    customers["cohort_month"] = customers["signup_date"].dt.strftime("%Y-%m")

    cohorts: list[dict[str, Any]] = []
    for cohort_month, cohort_customers in customers.groupby("cohort_month", sort=True):
        active_after_3_months = 0

        for customer in cohort_customers.to_dict("records"):
            customer_id = customer["customer_id"]
            retention_date = customer["signup_date"] + pd.DateOffset(months=3)
            active_subscription_mask = (
                (subscriptions["customer_id"] == customer_id)
                & (subscriptions["start_date"] <= retention_date)
                & (
                    subscriptions["end_date"].isna()
                    | (subscriptions["end_date"] >= retention_date)
                )
            )
            if active_subscription_mask.any():
                active_after_3_months += 1

        cohort_size = int(len(cohort_customers))
        cohorts.append(
            {
                "cohort_month": cohort_month,
                "cohort_size": cohort_size,
                "active_after_3_months": int(active_after_3_months),
                "retention_rate_3m": (
                    float(active_after_3_months / cohort_size) if cohort_size else 0.0
                ),
            }
        )

    return cohorts
