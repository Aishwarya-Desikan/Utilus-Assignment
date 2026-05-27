"""CLI entry point for generating SaaS subscription analytics reports."""

from pathlib import Path

import typer

from src.ingest import load_customers, load_subscriptions
from src.metrics import calculate_churn, calculate_cohort_retention, calculate_mrr
from src.report import generate_report

app = typer.Typer(add_completion=False)


@app.command()
def main(
    customers_path: Path,
    subscriptions_path: Path,
    output_path: Path,
) -> None:
    """Generate a JSON analytics report from customers and subscriptions CSVs."""
    try:
        customers = load_customers(customers_path)
        subscriptions = load_subscriptions(subscriptions_path)

        mrr = calculate_mrr(subscriptions)
        churn = calculate_churn(subscriptions)
        cohort = calculate_cohort_retention(customers, subscriptions)

        generate_report(mrr, churn, cohort, output_path)
    except ValueError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Report written to {output_path}")


if __name__ == "__main__":
    app()
