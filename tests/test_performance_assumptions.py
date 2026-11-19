import csv
import json
from pathlib import Path

import pytest


FILES = [
    "results/cost-comparison.csv",
    "results/serverless-comparison.csv",
    "results/utilization-sensitivity.csv",
    "results/model-cost-comparison.csv"
]


@pytest.mark.parametrize("filename", FILES)
def test_assumption_provenance(filename):
    with open(filename) as f:
        rows = list(csv.DictReader(f))

    assert rows

    for row in rows:
        assert row["throughput_source"]
        assert row["throughput_confidence"] == "unverified"
        assert row["performance_status"] == "unmeasured"


def test_latency_not_fabricated():
    config = json.loads(
        Path("configs/workloads/performance-assumptions.json").read_text()
    )

    assert config["latency"]["ttft_ms"] is None
    assert config["latency"]["inter_token_latency_ms"] is None
    assert config["latency"]["p95_latency_ms"] is None


def test_assumption_matrix():
    with open("results/performance-assumptions.csv") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 75
    assert all(r["hardware_calibrated"] == "False" for r in rows)
    assert all(r["latency_status"] == "unmeasured" for r in rows)
