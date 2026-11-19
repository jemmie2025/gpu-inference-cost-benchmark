import csv
from datetime import date

import pytest


FILES = [
    "configs/providers/pricing.csv",
    "results/cost-comparison.csv",
    "results/serverless-comparison.csv",
    "results/utilization-sensitivity.csv",
    "results/model-cost-comparison.csv"
]


@pytest.mark.parametrize("filename", FILES)
def test_pricing_provenance(filename):
    with open(filename) as f:
        rows = list(csv.DictReader(f))

    assert rows, f"Empty dataset: {filename}"

    for row in rows:
        captured = date.fromisoformat(
            row["price_captured_at"]
        )

        assert captured <= date.today()
        assert row["price_source_url"].startswith("https://")
        assert row["price_status"] in (
            "published", "secondary_source"
        )
