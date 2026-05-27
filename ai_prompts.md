# AI Prompts Used

I used ChatGPT Codex inside VS Code to help with parts of this assignment.
Below are the prompts I used during the session.

## Understanding the data
I opened both CSV files and ran df.head() and df.info() on both.
Then asked Codex:

"I have two CSV files for a SaaS analytics assignment. 
customers has customer_id, signup_date, country. 
subscriptions has customer_id, start_date, end_date, plan, monthly_price.
end_date is empty for active subscriptions. monthly_price is stored as string.
There is a typo in plan column - baisc instead of basic.
One country value is missing.
Help me write an ingest module that loads both files, converts dates and 
monthly_price to correct types and validates required columns exist."

## Writing the metrics
After ingest was working, I asked:

"Write me 3 metric functions for MRR, churn and cohort retention.
MRR should sum active subscription prices per calendar month.
Churn should flag customers who didn't re-subscribe within 30 days.
Cohort retention should check if customers are still active 3 months 
after signup."

## Writing tests
Once metrics were done I asked:

"Write pytest tests for these 3 functions covering basic cases,
edge cases like re-subscribing within 30 days and subscription ending 
exactly on the 3 month boundary."

## General help
Used Codex throughout for small things like fixing imports, 
checking pandas syntax and cleaning up code structure.

## AI Usage Log

AI tools were used during development to help with:

- Checking edge cases for churn and retention calculations
- Improving README/documentation wording
- Getting ideas for unit test cases
- Reviewing CLI flow and validation handling

All implementation decisions, debugging, testing, and final verification were done manually.