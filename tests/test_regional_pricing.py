import csv

import pytest


FILES = [
    "configs/providers/pricing.csv",
    "results/cost-comparison.csv",
    "results/serverless-comparison.csv",
    "results/utilization-sensitivity.csv",
    "results/model-cost-comparison.csv"
]


@pytest.mark.parametrize("filename", FILES)
def test_regional_pricing_metadata(filename):
    with open(filename) as f:
        rows = list(csv.DictReader(f))

    assert rows

    for row in rows:
        assert row["region"]
        assert row["target_market"] == "US"
        assert row["regional_price_status"]
        assert row["regional_source_url"].startswith("https://")

        if row["regional_ranking_eligible"] == "true":
            assert row["regional_price_status"] == "regional_published"
            assert row["price_status"] == "published"
            assert row["region"] != "unspecified"


def test_all_providers_covered():
    with open("configs/providers/pricing.csv") as f:
        rows = list(csv.DictReader(f))

    assert {r["provider"] for r in rows} == {
        "AWS", "GCP", "Lambda", "RunPod",
        "Modal", "Replicate"
    }


def test_unconfirmed_regions_excluded():
    with open("configs/providers/pricing.csv") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        if row["region"] == "unspecified":
            assert row["regional_ranking_eligible"] == "false"
