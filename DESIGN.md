# Design

This is a small Python CLI tool that takes two CSV files — customers and 
subscriptions — and produces a JSON report with three metrics: MRR, churn, 
and cohort retention.

## How the code is structured

- `src/ingest.py` — reads and validates the CSV files. Handles bad dates, 
  missing columns and type conversions.
- `src/metrics.py` — all the business logic lives here. One function per metric.
- `src/report.py` — takes the metric results and writes them to a JSON file.
- `main.py` — the CLI entry point. Run it with the two CSV paths and output path.
- `tests/test_metrics.py` — pytest tests covering the core logic and edge cases.

## How the business rules work

MRR — for each calendar month, add up the monthly_price of every subscription 
that was active in that month. Active means it started before the month ended 
and either has no end_date or ended after the month started.

Churn — a customer is churned if their subscription ended and they didn't start 
a new one within 30 days. Counted in the month the subscription ended.

Cohort retention — customers are grouped by the month they signed up. Three months 
later we check if they still have an active subscription. That gives us the 
retention rate per cohort.

## How to add a new metric

Add a new function in `src/metrics.py`, call it in `main.py`, and add the result 
to the report dict in `src/report.py`. Add tests for it in `tests/`. That's it.

## Assumptions and tradeoffs

- Bad dates are dropped with a warning instead of crashing.
- monthly_price is treated as a full month charge regardless of active days.
- Churn and cohort logic loops row by row — fine for this dataset size but 
  would need optimising for large scale data.
- Assumed one active subscription per customer at a time as stated.