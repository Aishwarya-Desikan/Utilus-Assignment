"""JSON report generation for subscription analytics."""

import json
from pathlib import Path
from typing import Any


def generate_report(
    mrr: dict[str, float],
    churn: dict[str, int],
    cohort: list[dict[str, Any]],
    output_path: str | Path,
) -> dict[str, Any]:
    """Combine metrics into a JSON report and write it to disk.

    Args:
        mrr: Monthly recurring revenue keyed by month in YYYY-MM format.
        churn: Monthly churned customer counts keyed by month in YYYY-MM format.
        cohort: Signup cohort retention records.
        output_path: Destination path for the JSON report.

    Returns:
        The combined report dictionary that was written to output_path.
    """
    report: dict[str, Any] = {
        "monthly_mrr": mrr,
        "monthly_churn": churn,
        "cohort_retention": cohort,
    }

    output_file = Path(output_path)
    output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return report
