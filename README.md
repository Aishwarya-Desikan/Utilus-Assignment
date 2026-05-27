## Assumptions

- Empty end_date means the subscription is still active.
- monthly_price is treated as a full month charge regardless of 
  active days.
- Churn is counted in the month the subscription ended.
- Re-subscribing within 30 days means the customer is not churned.
- One missing country in customers.csv is noted but not blocking.
- Plan typo "baisc" is logged as a warning and not treated as error.
- Cohort retention checks if customer has any active subscription 
  exactly 3 months after signup.
- Malformed dates cause the tool to fail with a clear message.