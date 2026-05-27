"""CSV ingestion helpers for the analytics CLI."""

from pathlib import Path
from typing import Iterable

import pandas as pd


CUSTOMER_REQUIRED_COLUMNS = {"customer_id", "signup_date", "country"}
SUBSCRIPTION_REQUIRED_COLUMNS = {
    "customer_id",
    "start_date",
    "end_date",
    "monthly_price",
    "plan",
}


def load_customers(path: str | Path) -> pd.DataFrame:
    """Load and validate a customers CSV file.

    Args:
        path: Path to a CSV with customer_id, signup_date, and country columns.

    Returns:
        A pandas DataFrame with signup_date parsed as datetime64.

    Raises:
        ValueError: If required columns are missing or signup_date cannot be parsed.
    """
    customers = pd.read_csv(path)
    _validate_required_columns(customers.columns, CUSTOMER_REQUIRED_COLUMNS, "customers")
    customers["signup_date"] = _parse_date_column(customers, "signup_date", "customers")
    return customers


def load_subscriptions(path: str | Path) -> pd.DataFrame:
    """Load and validate a subscriptions CSV file.

    Args:
        path: Path to a CSV with customer_id, start_date, end_date, monthly_price,
            and plan columns.

    Returns:
        A pandas DataFrame with start_date and end_date parsed as datetime64. Blank
        end_date values are preserved as NaT for active subscriptions.

    Raises:
        ValueError: If required columns are missing or date columns cannot be parsed.
    """
    subscriptions = pd.read_csv(path)
    _validate_required_columns(
        subscriptions.columns,
        SUBSCRIPTION_REQUIRED_COLUMNS,
        "subscriptions",
    )
    subscriptions["start_date"] = _parse_date_column(
        subscriptions,
        "start_date",
        "subscriptions",
    )
    subscriptions["end_date"] = _parse_date_column(
        subscriptions,
        "end_date",
        "subscriptions",
        allow_blank=True,
    )
    subscriptions["monthly_price"] = pd.to_numeric(
    subscriptions["monthly_price"], errors="coerce"
)
    return subscriptions


def _validate_required_columns(
    actual_columns: Iterable[str],
    required_columns: set[str],
    dataset_name: str,
) -> None:
    missing_columns = sorted(required_columns - set(actual_columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns in {dataset_name}.csv: {missing}")


def _parse_date_column(
    data: pd.DataFrame,
    column: str,
    dataset_name: str,
    *,
    allow_blank: bool = False,
) -> pd.Series:
    original_values = data[column]
    parsed_values = pd.to_datetime(original_values, errors="coerce")

    if allow_blank:
        blank_mask = original_values.isna() | original_values.astype(str).str.strip().eq("")
    else:
        blank_mask = pd.Series(False, index=original_values.index)

    invalid_mask = parsed_values.isna() & ~blank_mask
    if invalid_mask.any():
        invalid_examples = original_values[invalid_mask].astype(str).head(3).tolist()
        examples = ", ".join(invalid_examples)
        raise ValueError(
            f"Invalid dates in {dataset_name}.csv column '{column}': {examples}"
        )

    return parsed_values
