# Utilus Python Assignment

## Approach

I split the code into separate modules — ingest, metrics, and report — 
so each part has one job. The CLI in main.py just wires them together.
Metrics are self contained functions so adding a new one is straightforward.
I focused on getting the business logic correct first then added 
validation and tests around the core functions.

## How to Run

```bash
pip install -r requirements.txt
python main.py data/customers.csv data/subscriptions.csv output.json
```

## How to Run Tests

```bash
pytest -v
```

## Assumptions

- Empty end_date means the subscription is still active.
- monthly_price is treated as a full month charge regardless of active days.
- Churn is counted in the month the subscription ended.
- Re-subscribing within 30 days means the customer is not churned.
- One missing country in customers.csv is noted but not blocking.
- Plan typo "baisc" is logged as a warning and not treated as an error.
- Cohort retention checks if customer has any active subscription 
  exactly 3 months after signup.
- Malformed dates are dropped with a warning to allow processing to continue.

## AI Tools Used

See ai_prompts.md for the full log.