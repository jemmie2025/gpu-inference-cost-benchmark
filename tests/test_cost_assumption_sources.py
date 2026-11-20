import csv
import json
from pathlib import Path

import pytest


CONFIG = json.loads(
    Path("configs/workloads/performance-assumptions.json").read_text()
)


@pytest.mark.parametrize("key,expected", [
    ("infrastructure_overhead", [0.0, 0.10, 0.20]),
    ("cold_start", [0, 5, 15, 30]),
])
def test_assumption_sources(key, expected):
    assumption = CONFIG[key]

    assert assumption["scenarios"] == expected
    assert assumption["source"]
    assert assumption["supporting_source_url"].startswith("https://")
    assert assumption["provider_calibrated"] is False
    assert assumption["confidence"] == "unverified"


@pytest.mark.parametrize("filename,prefix", [
    ("results/cost-comparison.csv", "overhead"),
    ("results/serverless-comparison.csv", "cold_start"),
])
def test_report_assumption_provenance(filename, prefix):
    with open(filename) as f:
        rows = list(csv.DictReader(f))

    assert rows

    for row in rows:
        assert row[f"{prefix}_source"]
        assert row[f"{prefix}_source_url"].startswith("https://")


def test_cold_start_upper_bound_not_guaranteed():
    assert CONFIG["cold_start"]["upper_bound_guaranteed"] is False
