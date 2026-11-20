import csv
from pathlib import Path

import pytest

from src.pricing_normalization import normalize


def pricing_rows():
    with Path("configs/providers/pricing.csv").open() as handle:
        return list(csv.DictReader(handle))


def test_all_six_providers_normalized():
    rows = pricing_rows()
    assert len(rows) == 12
    assert len({r["provider"] for r in rows}) == 6


def test_strict_regional_comparison_requires_evidence():
    for row in pricing_rows():
        result = normalize(row)

        if result["normalization_status"] == "strict_regional_eligible":
            assert row["regional_price_status"] == "regional_published"
            assert row["region"] != "unspecified"
            assert row["price_status"] == "published"
            assert row["cost_scope"] == "instance"
            assert row["billing"] != "serverless"


def test_unconfirmed_regions_not_strictly_ranked():
    for row in pricing_rows():
        result = normalize(row)
        if row["region"] == "unspecified":
            assert result["normalization_status"] != "strict_regional_eligible"


def test_modal_gpu_only_not_complete_instance_price():
    row = next(r for r in pricing_rows() if r["provider"] == "Modal")
    result = normalize(row)

    assert result["normalization_status"] == "excluded"


def test_secondary_aws_prices_not_independently_verified():
    for row in pricing_rows():
        if row["provider"] == "AWS":
            assert normalize(row)["normalization_status"] != "strict_regional_eligible"


def test_invalid_hourly_rate_rejected():
    row = pricing_rows()[0].copy()
    row["usd_per_hour"] = "-1"

    with pytest.raises(ValueError):
        normalize(row)


def test_normalized_report_contains_all_providers():
    with Path("results/normalized-pricing.csv").open() as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 12
    assert len({r["provider"] for r in rows}) == 6
    assert all(r["normalization_status"] for r in rows)
