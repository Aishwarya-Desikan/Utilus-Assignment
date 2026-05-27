import pandas as pd

from src.metrics import calculate_churn, calculate_cohort_retention, calculate_mrr


def test_calculate_mrr_basic_case() -> None:
    subscriptions = pd.DataFrame(
        {
            "customer_id": ["cust_1"],
            "start_date": pd.to_datetime(["2024-01-10"]),
            "end_date": pd.to_datetime([None]),
            "monthly_price": [100.0],
            "plan": ["basic"],
        }
    )

    assert calculate_mrr(subscriptions)["2024-01"] == 100.0


def test_calculate_mrr_excludes_subscription_ended_before_month() -> None:
    subscriptions = pd.DataFrame(
        {
            "customer_id": ["cust_1", "cust_2"],
            "start_date": pd.to_datetime(["2024-01-01", "2024-02-01"]),
            "end_date": pd.to_datetime(["2024-01-31", None]),
            "monthly_price": [100.0, 50.0],
            "plan": ["basic", "basic"],
        }
    )

    assert calculate_mrr(subscriptions)["2024-02"] == 50.0


def test_calculate_churn_basic_case() -> None:
    subscriptions = pd.DataFrame(
        {
            "customer_id": ["cust_1"],
            "start_date": pd.to_datetime(["2024-01-01"]),
            "end_date": pd.to_datetime(["2024-01-31"]),
            "monthly_price": [100.0],
            "plan": ["basic"],
        }
    )

    assert calculate_churn(subscriptions) == {"2024-01": 1}


def test_calculate_churn_excludes_resubscribe_within_30_days() -> None:
    subscriptions = pd.DataFrame(
        {
            "customer_id": ["cust_1", "cust_1"],
            "start_date": pd.to_datetime(["2024-01-01", "2024-02-15"]),
            "end_date": pd.to_datetime(["2024-01-31", None]),
            "monthly_price": [100.0, 150.0],
            "plan": ["basic", "pro"],
        }
    )

    assert calculate_churn(subscriptions) == {}


def test_calculate_cohort_retention_basic_case() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": ["cust_1"],
            "signup_date": pd.to_datetime(["2024-01-15"]),
            "country": ["US"],
        }
    )
    subscriptions = pd.DataFrame(
        {
            "customer_id": ["cust_1"],
            "start_date": pd.to_datetime(["2024-01-15"]),
            "end_date": pd.to_datetime([None]),
            "monthly_price": [100.0],
            "plan": ["basic"],
        }
    )

    assert calculate_cohort_retention(customers, subscriptions) == [
        {
            "cohort_month": "2024-01",
            "cohort_size": 1,
            "active_after_3_months": 1,
            "retention_rate_3m": 1.0,
        }
    ]


def test_calculate_cohort_retention_not_retained() -> None:
    customers = pd.DataFrame(
        {
            "customer_id": ["cust_1"],
            "signup_date": pd.to_datetime(["2024-01-15"]),
            "country": ["US"],
        }
    )
    subscriptions = pd.DataFrame(
        {
            "customer_id": ["cust_1"],
            "start_date": pd.to_datetime(["2024-01-15"]),
            "end_date": pd.to_datetime(["2024-03-31"]),
            "monthly_price": [100.0],
            "plan": ["basic"],
        }
    )

    assert calculate_cohort_retention(customers, subscriptions) == [
        {
            "cohort_month": "2024-01",
            "cohort_size": 1,
            "active_after_3_months": 0,
            "retention_rate_3m": 0.0,
        }
    ]
